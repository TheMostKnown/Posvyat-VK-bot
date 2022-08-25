import json

from sqlalchemy.orm import Session

from app.vk_tools.spreadsheet_parser.spreadsheet_parser import get_data
from app.create_db import Sendings, Orgs, Groups


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

    existing_sengings = [sending.mail_name for sending in session.query(Sendings).all()]

    for i in range(1, len(sendings_sheet)):
        name = sendings_sheet[i][0]

        if name not in existing_sengings:

            text = sendings_sheet[i][1]
            groups = sendings_sheet[i][2]
            send_time = sendings_sheet[i][3]
            pics = sendings_sheet[i][4]
            video = sendings_sheet[i][5]
            reposts = sendings_sheet[i][6]
            docs = sendings_sheet[i][7]

            groups_json = ''
            if groups[0] != '!':
                groups_json = groups
            else:
                groups_from_db = session.query(Groups).all()
                not_selected_groups = json.loads(f'[{groups[1:]}]')

                for group in groups_from_db:
                    if group not in not_selected_groups:
                        groups_json += f'{group},'

            session.add(
                Sendings(
                    mail_name=name,
                    send_time=send_time,
                    groups=f'[{groups_json}]',
                    text=text,
                    pics=f'[{pics}]',
                    video=f'[{video}]',
                    reposts=f'[{reposts}]',
                    docs=f'[{docs}]'
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
