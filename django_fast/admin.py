from django.contrib import admin

from .models import CacheExplorer
from .views import CacheExplorerView


@admin.register(CacheExplorer)
class CacheExplorerAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        view = CacheExplorerView.as_view()
        return view(request)

    def has_add_permission(self, request):
        return False  # Disable the "Add" button

    def has_change_permission(self, request, obj=None):
        return False  # Disable the "Change" button

    def has_delete_permission(self, request, obj=None):
        return False  # Disable the "Delete" button

    def get_queryset(self, request):
        """Prevent database queries by returning an empty queryset."""
        return super().get_queryset(request).none()