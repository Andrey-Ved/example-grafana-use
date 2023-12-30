from fastapi import Request, FastAPI
from aioprometheus import (
    Registry,
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
            registry: Registry,
            requests_inflight_max: int,
    ):
        super().__init__(app)

        self.http_requests_total = Counter(
            'http_requests_total',
            'http requests total',
            registry=registry,
        )
        self.http_requests_current = Gauge(
            'http_requests_inflight_current',
            'http requests inflight current',
            registry=registry,
        )
        self.http_requests_inflight_max = Gauge(
            'http_requests_inflight_max',
            'http requests inflight max',
            registry=registry,
        )

        self.http_requests_inflight_max.set({'type': 'config'}, requests_inflight_max)

        self.http_requests_duration_historgram = Histogram(
            'http_request_duration_seconds_historgram',
            'http request duration seconds historgram',
            registry=registry,
            buckets=(0.1, 0.2, 0.25, 0.5, 1.0)
        )
        self.http_requests_duration_summary = Summary(
            'http_request_duration_seconds_summary',
            'http request duration seconds summary',
            registry=registry,
            invariants=[(0.99, 0.01), (0.95, 0.01), (0.5, 0.05)]
        )

    async def dispatch(self, request: Request, call_next):
        now = time()

        self.http_requests_current.inc({'type': 'instant'})
        response = await call_next(request)

        elapsed_seconds = time() - now
        pattern = request.url.path
        method = request.method
        status = response.status_code

        self.http_requests_total.inc(
            {'pattern': pattern, 'method': method, 'status': status},
        )
        self.http_requests_duration_historgram.observe(
            {'pattern': pattern, 'method': method},
            elapsed_seconds,
        )
        self.http_requests_duration_summary.observe(
            {'pattern': pattern, 'method': method},
            elapsed_seconds,
        )

        self.http_requests_current.dec({'type': 'instant'})
        return response
