from asyncio import sleep
from fastapi import APIRouter, Response, status
from random import choice, randint


router = APIRouter()


@router.get("/code-2xx")
async def random_2xx(response: Response):
    response.status_code = choice(
        [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
        ]
    )
    return response


@router.get("/code-4xx")
async def random_4xx(response: Response):
    response.status_code = choice(
        [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_429_TOO_MANY_REQUESTS,
        ]
    )


@router.get("/code-5xx")
async def random_5xx(response: Response):
    response.status_code = choice(
        [
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            status.HTTP_501_NOT_IMPLEMENTED,
            status.HTTP_503_SERVICE_UNAVAILABLE,
            status.HTTP_504_GATEWAY_TIMEOUT,
        ]
    )


async def random_delay_ms(delay_ms: int):
    await sleep(
        randint(1, delay_ms) / 1000
    )


@router.get("/ms-{ms}")
async def with_delay(ms: int, response: Response):
    await random_delay_ms(ms)
    await random_2xx(response)
