import bot
import create_db

if __name__ == '__main__':
    create_db.check_existance()
    bot.start()

