import os

from pydantic import BaseSettings, BaseModel, Field
from typing import List, Tuple
from caf_logger import logger as caflogger
from pydantic.env_settings import SettingsSourceCallable

from . import logging_codes

logger = caflogger.get_logger('whpa_cdp_postgres.config')

class PostgresLibSettings(BaseSettings):
    username: str = 'postgres'
    password: str = ''
    hostport: str = 'localhost:5432'
    database: str = 'defaultdb'

    class Config:
        env_file: str = os.getenv('WHPA_CDP_POSTGRES_CONFIG_FILE', default='/var/app/config/postgres.env')
        secrets_dir: str = os.getenv('WHPA_CDP_POSTGRES_SECRETS', default='/var/app/config/secrets')
        env_prefix: str = "POSTGRES_LIB_"
