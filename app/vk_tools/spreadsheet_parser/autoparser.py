import json

import schedule
from sqlalchemy.orm import Session

from app.create_db import Guests
from spreadsheet_parser import get_data

# interval between spreadsheet check
PARSER_SLEEP_TIME = 30


def add_info_to_db(
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str,
) -> None:
    table = get_data(spreadsheet_id, creds_file_name, token_file_name)

    for row in table:
        guest = session.query(Guests).filter_by(surname=row[0]).first()

        if guest:
            guest.surname = row[0]
            guest.name = row[1]
            guest.patronymic = row[2]
            guest.phone_number = row[3]
            guest.tag = row[4]
            guest.vk_link = row[5]
            guest.groups = f'[{row[6]}]'
        else:
            session.add(Guests(
                surname=row[0],
                name=row[1],
                patronymic=row[2],
                phone_number=row[3],
                tag=row[4],
                vk_link=row[5],
                groups=f'[{row[6]}]'
            ))

        session.commit()


def start_auto_parsing(
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str,
) -> None:
    schedule.every(PARSER_SLEEP_TIME).minutes.do(
        add_info_to_db(
            session=session,
            spreadsheet_id=spreadsheet_id,
            creds_file_name=creds_file_name,
            token_file_name=token_file_name
        )
    )
