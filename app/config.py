import os

from pydantic import BaseSettings
from typing import Optional

dir_name = os.path.dirname(__file__)


class Settings(BaseSettings):
    PROJECT_NAME: str = 'POSVYAT_VK'
    DIR_NAME: str = os.path.dirname(__file__)

    VK_TOKEN: Optional[str]
    VK_GROUP_ID: Optional[int]
    TECH_SUPPORT_VK_ID: Optional[int]

    DB_PATH: Optional[str]

    GOOGLE_TABLE_ID: Optional[str]

    GOOGLE_FOLDER_ID: Optional[str]
    GOOGLE_CREDS_PATH: Optional[str]
    GOOGLE_TOKEN_PATH: Optional[str]

    DELAY: Optional[float]

    class Config:
        env_prefix = 'POSVYAT_VK_'
        env_file = f'{dir_name}/secrets/.env'
        env_file_encoding = 'utf-8'
        fields = {
            'VK_TOKEN': {'env': 'VK_TOKEN'},
            'VK_GROUP_ID': {'env': 'VK_GROUP_ID'},
            'TECH_SUPPORT_VK_ID': {'env': 'TECH_SUPPORT_VK_ID'},
            'DB_PATH': {'env': 'DB_PATH'},
            'TEST_GOOGLE_TABLE_ID': {'env': 'TEST_GOOGLE_TABLE_ID'},
            'GOOGLE_TABLE_ID': {'env': 'GOOGLE_TABLE_ID'},
            'GOOGLE_FOLDER_ID': {'env': 'GOOGLE_FOLDER_ID'},
            'GOOGLE_CREDS_PATH': {'env': 'GOOGLE_CREDS_PATH'},
            'GOOGLE_TOKEN_PATH': {'env': 'GOOGLE_TOKEN_PATH'},
            'DELAY': {'env': 'DELAY'}
        }


settings = Settings()
