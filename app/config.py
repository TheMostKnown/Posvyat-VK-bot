import os

from pydantic import BaseSettings
from typing import Optional

dir_name = os.path.dirname(__file__)


class Settings(BaseSettings):
    PROJECT_NAME: str = 'POSVYAT_VK'
    DIR_NAME: str = os.path.dirname(__file__)

    VK_TOKEN: Optional[str]

    GOOGLE_TABLE_ID: Optional[str]
    GOOGLE_CREDS_PATH: Optional[str]
    GOOGLE_TOKEN_PATH: Optional[str]

    DB_PATH: Optional[str]

    class Config:
        env_prefix = 'POSVYAT_VK_'
        env_file = f'{dir_name}\secrets\.env'
        env_file_encoding = 'utf-8'
        fields = {
            'GOOGLE_TABLE_ID': {'env': 'GOOGLE_TABLE_ID'},
            'GOOGLE_CREDS_PATH': {'env': 'GOOGLE_CREDS_PATH'},
            'GOOGLE_TOKEN_PATH': {'env': 'GOOGLE_TOKEN_PATH'}
        }


settings = Settings()
