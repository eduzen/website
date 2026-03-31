import datetime as dt
import time
from datetime import timedelta

from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from .models import RequestProfile


class ProfilerMiddleware(MiddlewareMixin):
    def process_view(
        self,
        request: HttpRequest,
        view_func: object,
        view_args: tuple[object, ...],
        view_kwargs: dict[str, object],
    ) -> None:
        """
        Called just before Django calls the view.
        Store both the wall-clock datetime and a high-resolution counter so we
        can record an accurate start_time and compute a precise duration.
        """
        del view_func, view_args, view_kwargs
        # Store per-request timing markers (dynamic attributes on HttpRequest).
        setattr(request, "_profile_start_dt", timezone.now())  # real wall-clock start
        setattr(request, "_profile_start_perf", time.perf_counter())  # high-res timer for duration

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """
        Called just after the view returns a response.
        Fix #11: previously both start_time and end_time were set to timezone.now()
        at response time, making neither field meaningful.  Now start_time is the
        datetime captured in process_view and end_time is derived from it plus the
        measured duration.
        """
        start_perf = getattr(request, "_profile_start_perf", None)
        start_dt = getattr(request, "_profile_start_dt", None)
        if not isinstance(start_perf, float) or not isinstance(start_dt, dt.datetime):
            return response  # short-circuited by another middleware

        path = request.path_info
        if path.startswith("/static/") or path.startswith("/admin/"):
            return response

        if path.startswith("/__reload__/") or path.startswith("/__debug__/"):
            return response

        duration_ms = (time.perf_counter() - start_perf) * 1000.0
        end_dt = start_dt + timedelta(milliseconds=duration_ms)

        user = request.user if request.user.is_authenticated else None

        RequestProfile.objects.create(
            method=request.method or "",
            path=path,
            status_code=response.status_code,
            user=user,
            start_time=start_dt,
            end_time=end_dt,
            duration_ms=duration_ms,
        )

        return response
