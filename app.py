import os
import socket

from flask import Flask, Response, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    generate_latest,
)

app = Flask(__name__)

REQUESTS = Counter(
    "homelab_requests_total",
    "Number of application HTTP requests",
    ["endpoint", "status"],
)


@app.after_request
def count_requests(response):
    if request.endpoint not in {"health", "metrics"}:
        REQUESTS.labels(
            endpoint=request.endpoint or "unknown",
            status=str(response.status_code),
        ).inc()

    return response


@app.get("/")
def index():
    return {
        "message": "Hello from homelab!",
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "hostname": socket.gethostname(),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/error")
def simulated_error():
    return {"error": "Intentional training error"}, 500


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST,
    )