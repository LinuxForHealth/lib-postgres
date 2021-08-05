import os

from pydantic import BaseSettings

from . import logging_codes

class PostgresLibSettings(BaseSettings):
    username: str
    password: str
    hostport: str
    database: str

    class Config:
        env_file: str = os.getenv('WHPA_CDP_POSTGRES_CONFIG_FILE', default='/var/app/config/postgres.env')
        secrets_dir: str = os.getenv('WHPA_CDP_POSTGRES_SECRETS', default='/var/app/config/secrets')
        env_prefix: str = "POSTGRES_LIB_"
