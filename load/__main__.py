import aiohttp
import asyncio

from datetime import datetime
from load.definition import config, logger
from random import choice, shuffle


SUCCESSFUL_ENDPOINTS = [
    "/code-2xx",
    "/ms-200",
    "/ms-500",
    "/ms-1000",
]

ERROR_ENDPOINTS = [
    "/code-4xx",
    "/code-5xx",
]

API_NAME = 'api'
# API_NAME = '127.0.0.1'


async def main():
    logger.info('********* load started *********')
    current_sec = 1

    while True:
        now_sec = int(datetime.now().timestamp() // 1)

        if now_sec > current_sec:
            current_sec = now_sec
            endpoints_list = []

            logger.info(f'request second {now_sec}')

            for _ in range(config.http_requests_error_max):
                endpoints_list.append(
                    choice(ERROR_ENDPOINTS)
                )

            for _ in range(config.http_requests_successful_max):
                endpoints_list.append(
                    choice(SUCCESSFUL_ENDPOINTS)
                )

            shuffle(endpoints_list)

            try:
                async with aiohttp.ClientSession() as session:
                    works = []
                    for endpoint in endpoints_list:
                        url = f'http://{API_NAME}:{config.api_port}{endpoint}'  # noqa
                        works.append(asyncio.create_task(session.get(url)))

                    responses = await asyncio.gather(*works)
                    responses_text = [await r.text(encoding='UTF-8') for r in responses]
                    logger.info(f'responses from api {responses_text}')

            except (Exception, ):
                logger.info(f'failed request attempt')


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info('******** canceling tasks ********')

        def shutdown_exception_handler(loop, context):
            if "exception" not in context \
                    or not isinstance(context["exception"], asyncio.CancelledError):
                loop.default_exception_handler(context)

        event_loop.set_exception_handler(shutdown_exception_handler)

        tasks = asyncio.all_tasks(loop=event_loop)
        for task in tasks:
            task.add_done_callback(lambda t: event_loop.stop())
            task.cancel()

    finally:
        event_loop.run_until_complete(event_loop.shutdown_asyncgens())
        event_loop.close()
