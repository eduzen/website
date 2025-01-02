from django.conf import settings
from django.contrib import messages
from django.contrib.admin import site
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import caches
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from django_fast.services.cache.factory import get_cache_service


def check_cache_health(alias: str) -> str:
    try:
        cache = caches[alias]
        cache.set("redis_health_check", "ok", timeout=5)
        value = cache.get("redis_health_check")
        status = "🟢 Live" if value == "ok" else "🔴 Unavailable"
    except Exception as e:
        status = f"🔴 Error: {str(e)}"

    return status


@method_decorator(staff_member_required, name="dispatch")
class CacheExplorerView(View):
    template_name = "django_fast/cache_explorer.html"

    def get(self, request):
        # Admin-specific context
        admin_context = site.each_context(request)
        admin_context.update(
            {
                "title": "Cache Explorer",
                "breadcrumbs": [
                    {"name": "Home", "url": reverse("admin:index")},
                    {"name": "Cache Explorer", "url": ""},
                ],
            }
        )

        # Custom context for your view
        cache_settings = settings.CACHES
        status_dict = {
            alias: "🟢 Live" if get_cache_service(alias).ping() else "🔴 Unavailable" for alias in cache_settings.keys()
        }

        admin_context.update(
            {
                "cache_settings": cache_settings,
                "status": status_dict,
            }
        )
        return render(request, self.template_name, admin_context)


@method_decorator(staff_member_required, name="dispatch")
class CacheDetailView(View):
    template_name = "django_fast/cache_detail.html"

    def get(self, request, alias):
        cache_service = get_cache_service(alias)
        admin_context = site.each_context(request)
        admin_context.update(
            {
                "title": f"Cache Detail: {alias}",
                "breadcrumbs": [
                    {"name": "Home", "url": reverse("admin:index")},
                    {"name": "Cache Explorer", "url": reverse("cache_explorer")},
                    {"name": f"Cache Detail: {alias}", "url": ""},
                ],
            }
        )

        if not cache_service.ping():
            admin_context.update(
                {
                    "alias": alias,
                    "error": f"Cache alias '{alias}' is unreachable or not configured properly.",
                }
            )
            return render(request, self.template_name, admin_context)

        stats = cache_service.get_stats()

        admin_context.update(
            {
                "alias": alias,
                "stats": stats,
            }
        )
        return render(request, self.template_name, admin_context)

    def post(self, request, alias):
        cache_service = get_cache_service(alias)
        action = request.POST.get("action")

        if action == "clear":
            cache_service.clear_cache()
            messages.success(request, f"Cache '{alias}' cleared successfully.")
        elif action == "ping":
            if cache_service.ping():
                messages.success(request, f"Cache '{alias}' is alive.")
            else:
                messages.error(request, f"Cache '{alias}' is unreachable.")
        # Add more elifs for new actions

        return redirect("cache_detail", alias=alias)
