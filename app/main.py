import threading

from app import bot
from app.vk_tools.google.spreadsheet_parser import autoparser
from app.create_db import engine, create_tables
from app.config import settings

if __name__ == '__main__':
    create_tables(engine)

    bot_thread = threading.Thread(target=bot.start)
    bot_thread.start()

    autoparser_thread = threading.Thread(
        target=autoparser.start_auto_parsing,
        args=(
            bot.vk,
            bot.session,
            settings.GOOGLE_TABLE_ID,
            settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
            settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH
        )
    )
    autoparser_thread.start()
