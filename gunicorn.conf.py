import multiprocessing
import os

# Network & timeouts
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:80")
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", 5))
timeout = int(os.getenv("GUNICORN_TIMEOUT", 120))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", 30))

# Logging
loglevel = os.getenv("LOG_LEVEL", "info")
capture_output = True
enable_stdio_inheritance = True
accesslog = "-"
errorlog = "-"
access_log_format = '[GUNICORN] %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s'

# Concurrency
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")
threads = int(os.getenv("GUNICORN_THREADS", multiprocessing.cpu_count() * 2))
backlog = int(os.getenv("GUNICORN_BACKLOG", 2048))
worker_tmp_dir = "/dev/shm"


# Memory leak protection
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", 1000))
max_requests_jitter = int(os.getenv("GUNICORN_JITTER", 50))

# Security limits
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190


# App & environment
chdir = "/code"
wsgi_app = "website.wsgi:application"
raw_env = [
    f"DJANGO_SETTINGS_MODULE={os.getenv('DJANGO_SETTINGS_MODULE', 'website.settings.production')}",
]

wsgi_app = "website.wsgi:application"
proc_name = "website"
pidfile = "/var/run/website.pid"

if os.getenv("DEBUG") == "True":
    reload = True
    reload_engine = "auto"
    reload_extra_files = ["pyproject.toml", "uv.lock"]
