import json

from sqlalchemy.orm import Session

from app.vk_tools.spreadsheet_parser.spreadsheet_parser import get_data
from app.create_db import Sendings, Orgs


def get_sendings(
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str,
        sheet_name: str
) -> None:

    sendings_sheet = get_data(
        spreadsheet_id,
        creds_file_name,
        token_file_name
    )[sheet_name]

    for row in sendings_sheet:
        name = row[0]
        group_num = row[1]
        send_time = row[2]
        text = row[3]
        pics = list()
        video = list()
        reposts = list()
        docs = list()

        if row[4]:
            pics.append(row[4])
        if row[5]:
            pics.append(row[5])
        if row[6]:
            video.append(row[6])
        if row[7]:
            reposts.append(row[7])
        if row[8]:
            docs.append(row[8])
        if row[9]:
            docs.append(row[9])

        session.add(
            Sendings(
                mail_name=name,
                send_time=send_time,
                group_num=group_num,
                text=text,
                pics=json.dumps(pics),
                video=json.dumps(video),
                reposts=json.dumps(reposts),
                docs=json.dumps(docs)
            )
        )

    session.commit()


def get_organizers(
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str,
        sheet_name: str
) -> None:

    organizers_sheet = get_data(
        spreadsheet_id,
        creds_file_name,
        token_file_name
    )[sheet_name]

    for row in organizers_sheet:
        chat_id = row[0]
        name = row[1]
        surname = row[2]
        patronymic = row[3]
        vk_link = row[4]
        group = row[5]

        session.add(
            Orgs(
                id=chat_id,
                name=name,
                surname=surname,
                patronymic=patronymic,
                vk_org_link=vk_link,
                group=group
            )
        )

    session.commit()
