from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class SimpleThrottling(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            requests_inflight_max: int,
            bypass_endpoints: list[str],
    ):
        super().__init__(app)

        self.requests_inflight_max = requests_inflight_max
        self.current_sec = 0
        self.requests_count = 0
        self.bypass_endpoints = bypass_endpoints

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.bypass_endpoints:
            return await call_next(request)

        now_sec = int(datetime.now().timestamp() // 1)

        if now_sec > self.current_sec:
            self.current_sec = now_sec
            self.requests_count = 0

        if self.requests_count < self.requests_inflight_max:
            self.requests_count += 1

            return await call_next(request)

        return JSONResponse(
                status_code=429,
                content={"detail": "Error: Too Many Requests"},
            )
