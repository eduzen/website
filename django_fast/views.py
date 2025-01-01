from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import caches
from django.shortcuts import render


def check_cache_health(alias: str) -> str:
    try:
        cache = caches[alias]
        cache.set("redis_health_check", "ok", timeout=5)
        value = cache.get("redis_health_check")
        status = "🟢 Live" if value == "ok" else "🔴 Unavailable"
    except Exception as e:
        status = f"🔴 Error: {str(e)}"

    return status


@staff_member_required
def cache_explorer(request):
    cache_settings = settings.CACHES
    status = {}

    status = {alias: check_cache_health(alias) for alias in cache_settings.keys()}

    return render(
        request,
        "django_fast/cache_explorer.html",
        {
            "cache_settings": cache_settings,
            "status": status,
        },
    )


@staff_member_required
def cache_detail(request, alias):
    cache = caches[alias]
    if not cache:
        return render(
            request,
            "django_fast/cache_detail.html",
            {
                "alias": alias,
                "error": f"Cache alias '{alias}' not found.",
            },
        )

    # Handle cache actions
    if request.method == "POST" and "clear_cache" in request.POST:
        cache.clear()
        messages.success(request, f"Cache '{alias}' cleared successfully.")
        return render(
            request,
            "django_fast/cache_detail.html",
            {
                "alias": alias,
                "stats": {"message": "Cache cleared successfully."},
            },
        )

    # Retrieve cache stats (if supported)
    stats = {}
    try:
        stats["keys"] = len(cache.keys("*"))  # Example for Redis
        stats["ttl"] = {key: cache.ttl(key) for key in cache.keys("*")[:5]}  # First 5 keys
    except AttributeError:
        stats["message"] = "Cache backend does not support stats."

    return render(
        request,
        "django_fast/cache_detail.html",
        {
            "alias": alias,
            "stats": stats,
        },
    )
