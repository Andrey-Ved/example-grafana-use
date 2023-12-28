import logging

from os.path import dirname, sep, abspath
from pydantic_settings import BaseSettings, SettingsConfigDict


handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(
    logging.Formatter('%(asctime)s: %(message)s', datefmt='%H:%M:%S')  # noqa
)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

root_path = dirname(
    dirname(
        abspath(__file__)
    )
)

env_file = root_path + sep + 'configs' + sep + '.env'


class Settings(BaseSettings):
    api_port: int
    http_requests_successful_max: int
    http_requests_error_max: int

    model_config = SettingsConfigDict(
        env_file=env_file,
        extra='ignore',
        env_file_encoding='utf-8',
    )


config = Settings()
