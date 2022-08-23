import os

from pydantic import BaseSettings
from typing import Optional

dir_name = os.path.dirname(__file__)


class Settings(BaseSettings):
    PROJECT_NAME: str = 'POSVYAT_VK'
    DIR_NAME: str = os.path.dirname(__file__)

    VK_TOKEN = 'vk1.a.Ub7uzvptyDIlozKlujVQJ5Ul9UxYdA__5fyPlBUhVSmVblrQiJdm3FHb2wnM2CikSlOUHqPZiIHngltKUXBouHtZf_2WZzhMWvUAFpfuTTTS4MPU1NzcW3y6oqTjbIkIyHWEOle3AQ2vYReRiLG8qBxmbedv4HC7aj3QXTHCGXnu9kGj5--H-JLgypG9YbIJ'
    TECH_SUPPORT_VK_ID: Optional[str]

    DB_PATH = 'postgresql+psycopg2://postgres:admin@db/postgres'

    GOOGLE_TABLE_ID_ORGS: Optional[str]
    GOOGLE_TABLE_ID_SENDINGS: Optional[str]

    GOOGLE_FOLDER_ID: Optional[str]
    GOOGLE_CREDS_PATH: Optional[str]
    GOOGLE_TOKEN_PATH: Optional[str]

    DELAY: Optional[str]

    class Config:
        env_prefix = 'POSVYAT_VK_'
        env_file = f'{dir_name}\secrets\.env'
        env_file_encoding = 'utf-8'
        fields = {
            'TECH_SUPPORT_VK_ID': {'env': 'TECH_SUPPORT_VK_ID'},
            'VK_TOKEN': {'env': 'VK_TOKEN'},
            'DB_PATH': {'env': 'DB_PATH'},
            'GOOGLE_TABLE_ID_ORGS': {'env': 'GOOGLE_TABLE_ID_ORGS'},
            'GOOGLE_TABLE_ID_SENDINGS': {'env': 'GOOGLE_TABLE_ID_SENDINGS'},
            'GOOGLE_FOLDER_ID': {'env': 'GOOGLE_FOLDER_ID'},
            'GOOGLE_CREDS_PATH': {'env': 'GOOGLE_CREDS_PATH'},
            'GOOGLE_TOKEN_PATH': {'env': 'GOOGLE_TOKEN_PATH'}
        }


settings = Settings()
