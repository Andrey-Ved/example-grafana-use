import logging

from os import path

from aioprometheus import Registry
from pydantic_settings import BaseSettings, SettingsConfigDict
from sys import stdout


logging.basicConfig(
    level=logging.INFO,
    stream=stdout,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',  # noqa
    datefmt='%H:%M:%S',
)


root_path = path.dirname(
    path.dirname(
        path.abspath(__file__)
    )
)

env_file = root_path + path.sep + 'configs' + path.sep + '.env'


class Settings(BaseSettings):
    api_port: int
    http_requests_inflight_max: int

    model_config = SettingsConfigDict(
        env_file=env_file,
        extra='ignore',
        env_file_encoding='utf-8',
    )


config = Settings()

aioprometheus_registry = Registry()
