from fastapi import Request, FastAPI
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    Summary,
)
from starlette.middleware.base import BaseHTTPMiddleware
from time import time


class HTTPMetric(BaseHTTPMiddleware):
    def __init__(
            self,
            app: FastAPI,
            registry: CollectorRegistry,
            requests_inflight_max: int,
    ):
        super().__init__(app)

        self.http_requests_total = Counter(
            'http_requests_total',
            '',
            labelnames=["pattern", "method", "status"],
            registry=registry,
        )
        self.http_requests_current = Gauge(
            'http_requests_inflight_current',
            '',
            registry=registry,
        )
        self.http_requests_inflight_max = Gauge(
            'http_requests_inflight_max',
            '',
            registry=registry,
        )

        self.http_requests_inflight_max.set(requests_inflight_max)

        self.http_requests_duration_historgram = Histogram(
            'http_request_duration_seconds_historgram',
            '',
            labelnames=["pattern", "method"],
            registry=registry,
            buckets=(0.1, 0.2, 0.25, 0.5, 1.0)
        )
        self.http_requests_duration_summary = Summary(
            'http_request_duration_seconds_summary',
            '',
            labelnames=["pattern", "method"],
            registry=registry,
        )

    async def dispatch(self, request: Request, call_next):
        now = time()

        self.http_requests_current.inc()
        response = await call_next(request)

        elapsed_seconds = time() - now
        pattern = request.url.path
        method = request.method
        status = response.status_code

        self.http_requests_total \
            .labels(pattern, method, status).inc()
        self.http_requests_duration_historgram \
            .labels(pattern, method).observe(elapsed_seconds)
        self.http_requests_duration_summary \
            .labels(pattern, method).observe(elapsed_seconds)

        self.http_requests_current.dec()
        return response
