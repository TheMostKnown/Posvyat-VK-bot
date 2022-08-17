from peewee import *
from sqlalchemy import *
import schedule
import sys
sys.path.append('../../')

# Не могу импортировать этот файл. Не понимаю в чем проблема
import create_db
from spreadsheet_parser import get_data

# interval between spreadsheet check
PARSER_SLEEP_TIME = 30


def add_info_to_db(
        spreadsheet_id: str,
        creds_file_name: str = 'credentials.json',
        token_file_name: str = 'token.json'
):
    table = get_data(spreadsheet_id, creds_file_name, token_file_name)

    for row in table:
        item = guests(
            surname = row[0],
            name = row[1],
            patronymic = row[2],
            phone_number = row[3],
            tag = row[4],
            vk_link = row[5],
            first_group = row[6],
            second_group = row[7],
            third_group = row[8],
            fourth_group = row[9],
            fifth_group = row[10],
            sixth_group = row[11],
            seventh_group = row[12],
            eighth_group = row[13],
            ninth_group = row[14],
            tenth_group = row[15],
            eleventh_grup = row[16],
            twelfth_group = row[17],
            thirteenth_group = row[18],
        )

        if (session.query(guests).filter(
            guests.surname == row[0]
        ).all is not None):
            i = session.query(guests).filter(
                guests.surname == row[0]
            ).first()
            i.surname = row[0]
            i.name = row[1]
            i.patronymic = row[2]
            i.phone_number = row[3]
            i.tag = row[4]
            i.vk_link = row[5]
            i.first_group = row[6]
            i.second_group = row[7]
            i.third_group = row[8]
            i.fourth_group = row[9]
            i.fifth_group = row[10]
            i.sixth_group = row[11]
            i.seventh_group = row[12]
            i.eighth_group = row[13]
            i.ninth_group = row[14]
            i.tenth_group = row[15]
            i.eleventh_grup = row[16]
            i.twelfth_group = row[17]
            i.thirteenth_group = row[18]
        else:
            session.add(item)

        session.commit()



def start_auto_parsing(
        spreadsheet_id: str,
        creds_file_name: str = 'credentials.json',
        token_file_name: str = 'token.json'
):
    schedule.every(PARSER_SLEEP_TIME).minutes.do(add_info_to_db(spreadsheet_id, creds_file_name, token_file_name))
