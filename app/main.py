from app import bot
from app.vk_tools.google.spreadsheet_parser import autoparser
from app.create_db import engine, create_tables
from app.config import settings

if __name__ == '__main__':
    create_tables(engine)
    bot.start()
