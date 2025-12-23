import os
import multiprocessing

bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
workers = 1
threads = 2
timeout = 300
keepalive = 5
preload_app = False

def on_starting(server):
    """Called just before the master process is initialized."""
    print(f"Gunicorn starting on {bind}")

def when_ready(server):
    """Called just after the server is started."""
    print(f"Gunicorn ready and listening on {bind}")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    print("Gunicorn reloading...")

