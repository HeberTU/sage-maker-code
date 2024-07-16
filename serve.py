"""This module implements the score service.

It starts nginx and gunicorn with the correct configurations and then simply
waits until gunicorn exits.

The flask server is specified to be the app object in wsgi.py

We set the following parameters:

Parameter                Environment Variable              Default Value
---------                --------------------              -------------
number of workers        MODEL_SERVER_WORKERS              the number of CPUs
timeout                  MODEL_SERVER_TIMEOUT              60 seconds
"""
import multiprocessing
import os
import signal
import subprocess
import sys

from fraud.utils import get_logger

logger = get_logger()

logger.info("Starting score service")

cpu_count = multiprocessing.cpu_count()

model_server_timeout = os.environ.get("MODEL_SERVER_TIMEOUT", 60)
model_server_workers = int(os.environ.get("MODEL_SERVER_WORKERS", cpu_count))


def sigterm_handler(nginx_pid: int, gunicorn_pid: int) -> None:
    """Terminate nginx and gunicorn process.

    Args:
        nginx_pid: nginx pid number.
        gunicorn_pid: gunicorn pid number.

    Returns:
        None.
    """
    try:
        os.kill(nginx_pid, signal.SIGQUIT)
    except OSError:
        pass
    try:
        os.kill(gunicorn_pid, signal.SIGTERM)
    except OSError:
        pass

    sys.exit(0)


def start_server():
    """Start score server."""
    logger.info(
        "Starting the inference server with {} workers.".format(
            model_server_workers
        )
    )

    # link the log streams to stdout/err so they will be logged to the
    # container logs
    subprocess.check_call(
        ["ln", "-sf", "/dev/stdout", "/var/log/nginx/access.log"]
    )
    subprocess.check_call(
        ["ln", "-sf", "/dev/stderr", "/var/log/nginx/error.log"]
    )

    nginx = subprocess.Popen(
        ["nginx", "-c", "/opt/program/fraud/config/nginx.conf"]
    )
    gunicorn = subprocess.Popen(
        [
            "gunicorn",
            "--timeout",
            str(model_server_timeout),
            "-k",
            "sync",
            "-b",
            "unix:/tmp/gunicorn.sock",
            "-w",
            str(model_server_workers),
            "fraud.entrypoints.wsgi:app",
        ]
    )

    signal.signal(
        signal.SIGTERM,
        lambda a, b: sigterm_handler(
            nginx_pid=nginx.pid, gunicorn_pid=gunicorn.pid
        ),
    )

    # If either subprocess exits, so do we.
    pids = set([nginx.pid, gunicorn.pid])
    while True:
        pid, _ = os.wait()
        if pid in pids:
            break

    sigterm_handler(nginx.pid, gunicorn.pid)
    logger.info("Inference server exiting")


if __name__ == "__main__":
    start_server()
