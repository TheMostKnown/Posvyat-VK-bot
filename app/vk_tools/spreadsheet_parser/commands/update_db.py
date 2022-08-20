import json
from typing import List

from sqlalchemy.orm import Session

from app.vk_tools.spreadsheet_parser.spreadsheet_parser import get_data
from app.create_db import Sendings


def update_sendings(
        session: Session,
        sending_names: List[str],
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

    sendings = session.query(Sendings).filter(Sendings.mail_name in sending_names)

    for sending in sendings:

        for row in sendings_sheet:
            name = row[0]

            if name == sending.mail_name:
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

                sending.group_num = group_num
                sending.send_time = send_time
                sending.text = text
                sending.pics = json.dumps(pics)
                sending.video = json.dumps(video)
                sending.reposts = json.dumps(reposts)
                sending.docs = json.dumps(docs)

    session.commit()


def delete_sendings(
        session: Session,
        sending_names: List[str]
) -> None:

    for sending in session.query(Sendings).all():
        if sending.mail_name in sending_names:
            session.delete(sending)

    session.commit()
