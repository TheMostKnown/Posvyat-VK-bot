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
            guest.chat_id = row[0]
            guest.surname = row[1]
            guest.name = row[2]
            guest.patronymic = row[3]
            guest.phone_number = row[4]
            guest.tag = row[5]
            guest.vk_link = row[6]
            guest.groups = f'[{row[7]}]'
        else:
            session.add(Guests(
                chat_id=row[0],
                surname=row[1],
                name=row[2],
                patronymic=row[3],
                phone_number=row[4],
                tag=row[5],
                vk_link=row[6],
                groups=f'[{row[7]}]'
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
