from typing import cast

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from .models import CacheExplorer, RequestProfile
from .views import CacheExplorerView


@admin.register(RequestProfile)
class RequestProfileAdmin(admin.ModelAdmin):
    list_display = ("method", "path", "status_code", "user", "duration_ms", "start_time")
    list_filter = ("method", "status_code")
    search_fields = ("path", "user__username")


@admin.register(CacheExplorer)
class CacheExplorerAdmin(admin.ModelAdmin):
    def changelist_view(self, request: HttpRequest, extra_context: dict[str, object] | None = None) -> HttpResponse:
        del extra_context
        view = CacheExplorerView.as_view()
        return cast(HttpResponse, view(request))

    def has_add_permission(self, request: HttpRequest) -> bool:
        del request
        return False  # Disable the "Add" button

    def has_change_permission(self, request: HttpRequest, obj: CacheExplorer | None = None) -> bool:
        del request, obj
        return False  # Disable the "Change" button

    def has_delete_permission(self, request: HttpRequest, obj: CacheExplorer | None = None) -> bool:
        del request, obj
        return False  # Disable the "Delete" button

    def get_queryset(self, request: HttpRequest) -> QuerySet[CacheExplorer]:
        """Prevent database queries by returning an empty queryset."""
        return super().get_queryset(request).none()
