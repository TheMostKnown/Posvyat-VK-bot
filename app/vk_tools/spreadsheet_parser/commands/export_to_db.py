import json

from sqlalchemy.orm import Session

from app.vk_tools.spreadsheet_parser.spreadsheet_parser import get_data
from app.create_db import Sendings, Orgs, Groups, Command


def get_commands(
    session: Session,
    spreadsheet_id: str,
    creds_file_name: str,
    token_file_name: str,
    sheet_name: str
) -> None:

    commands_sheet = get_data(
        spreadsheet_id,
        creds_file_name,
        token_file_name
    )[sheet_name]

    existing_commands = [command.name for command in session.query(Command).all()]

    for i in range(1, len(commands_sheet)):
        name = commands_sheet[i][0]

        if name not in existing_commands:
            arguments = commands_sheet[i][1]
            desc = commands_sheet[i][2]
            admin = True if commands_sheet[i][3] == 'True' else False

            session.add(
                Command(
                    name=name,
                    arguments=arguments,
                    desc=desc,
                    admin=admin
                )
            )

    session.commit()


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

    existing_organizers = [organizer.chat_id for organizer in session.query(Orgs).all()]

    for i in range(1, len(organizers_sheet)):
        chat_id = organizers_sheet[i][0]

        if chat_id not in existing_organizers:
            surname = organizers_sheet[i][1]
            name = organizers_sheet[i][2]
            patronymic = organizers_sheet[i][3]
            vk_link = organizers_sheet[i][4]
            groups = organizers_sheet[i][5]

            session.add(
                Orgs(
                    chat_id=chat_id,
                    name=name,
                    surname=surname,
                    patronymic=patronymic,
                    vk_link=vk_link,
                    groups=f'[{groups}]'
                )
            )

    session.commit()
