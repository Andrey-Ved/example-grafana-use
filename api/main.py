import uvicorn

from aioprometheus import render
from fastapi import FastAPI, Response, Header

from api.definition import config, aioprometheus_registry
from api.middleware.metrics import HTTPMetric
from api.middleware.throttling import SimpleThrottling
from api.router import router


app = FastAPI()

app.include_router(router)


@app.get("/metrics")
async def handle_metrics(
    accept: list[str] = Header(None),
) -> Response:
    content, http_headers = render(
        registry=aioprometheus_registry,
        accepts_headers=accept,
    )
    return Response(
        content=content,
        media_type=http_headers["Content-Type"]
    )


app.add_middleware(
    middleware_class=HTTPMetric,
    registry=aioprometheus_registry,  # prometheus_registry,
    requests_inflight_max=config.http_requests_inflight_max,
)


app.add_middleware(
    middleware_class=SimpleThrottling,
    requests_inflight_max=config.http_requests_inflight_max,
    bypass_endpoints=["/metrics", ],
)


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=config.api_port,
    )
