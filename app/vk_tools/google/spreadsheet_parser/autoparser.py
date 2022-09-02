import logging

import schedule
import vk_api.vk_api
from sqlalchemy.orm import Session

from app.create_db import UpdateTimer
from app.vk_tools.google.spreadsheet_parser.commands.export_to_db import get_init_data

# Подключение логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# interval between spreadsheet check
PARSER_SLEEP_TIME = 1


def start_auto_parsing(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str,
) -> None:

    schedule.every(PARSER_SLEEP_TIME).minutes.do(
        perform_parsing,
        *(vk, session, spreadsheet_id, creds_file_name, token_file_name)
    )


def perform_parsing(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str
) -> None:
    get_init_data(
        vk=vk,
        session=session,
        spreadsheet_id=spreadsheet_id,
        creds_file_name=creds_file_name,
        token_file_name=token_file_name
    )
    update_timer(session)
    logger.info('AutoParser has started')


def update_timer(session: Session) -> None:
    timer = session.query(UpdateTimer).first()

    if timer:
        PARSER_SLEEP_TIME = timer.update_timer
