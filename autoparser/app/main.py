import logging
import schedule

import vk_api
from sqlalchemy.orm import Session

from ..app.create_db import get_session, engine
from ..app.config import settings
from ..app.create_db import UpdateTimer
from ..app.google.spreadsheet_parser.commands.export_to_db import get_init_data


# connecting to db
session = get_session(engine)
# connecting vk
vk = vk_api.VkApi(token=settings.VK_TOKEN).get_api()

# configure logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


PARSER_SLEEP_TIME = 2


def update_timer(session: Session) -> None:
    timer = session.query(UpdateTimer).first()

    if timer:
        PARSER_SLEEP_TIME = timer.update_timer


def start_parsing():
    get_init_data(
        vk=vk,
        session=session,
        spreadsheet_id=settings.GOOGLE_TABLE_ID,
        creds_file_name=settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
        token_file_name=settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH
    ) 
    update_timer(session)
    logger.info('AutoParser has started')


schedule.every(PARSER_SLEEP_TIME).minutes.do(start_parsing())
