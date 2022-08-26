from app import bot
from app.create_db import engine, create_tables

if __name__ == '__main__':
    create_tables(engine)
    bot.start()
