import uvicorn

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from api.definition import config, prometheus_registry
from api.middleware.metrics import HTTPMetric
from api.middleware.throttling import SimpleThrottling
from api.router import router


app = FastAPI()

app.include_router(router)


@app.get("/metrics")
def metrics() -> Response:
    return Response(
        generate_latest(prometheus_registry),
        media_type=CONTENT_TYPE_LATEST
    )


app.add_middleware(
    middleware_class=HTTPMetric,
    registry=prometheus_registry,
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
