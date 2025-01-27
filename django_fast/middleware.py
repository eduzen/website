import time

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from .models import RequestProfile


class ProfilerMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        This method is called just before Django calls the view.
        We'll store the start time on the request object.
        """
        request._start_time = time.perf_counter()

    def process_response(self, request, response):
        """
        This method is called just after the view is called (and a response is generated).
        We'll calculate duration and store it in the DB.
        """
        if not hasattr(request, "_start_time"):
            return response  # some other middleware might short-circuit

        # We can skip static files, admin, etc. if we want
        path = request.path_info
        if path.startswith("/static/") or path.startswith("/admin/"):
            return response

        if path.startswith("/__reload__/") or path.startswith("/__debug__/"):
            return response

        # Gather info
        start_time = request._start_time
        end_time = time.perf_counter()
        duration = (end_time - start_time) * 1000.0  # ms

        user = request.user if request.user.is_authenticated else None

        # Save to database
        RequestProfile.objects.create(
            method=request.method,
            path=path,
            status_code=response.status_code,
            user=user,
            start_time=timezone.now(),
            end_time=timezone.now(),
            duration_ms=duration,
        )

        return response
