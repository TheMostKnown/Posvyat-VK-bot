import json

from sqlalchemy.orm import Session

from app.vk_tools.spreadsheet_parser.spreadsheet_parser import get_data
from app.create_db import Sendings, Orgs, Groups, Command, Guests


def get_init_data(
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str,
) -> None:

    spreadsheet = get_data(
        spreadsheet_id,
        creds_file_name,
        token_file_name
    )

    groups_sheet = spreadsheet['Levels']
    existing_groups = [group.group_info for group in session.query(Groups).all()]

    for i in range(1, len(groups_sheet)):
        group_info = groups_sheet[i][1]

        if group_info not in existing_groups:
            group_num = groups_sheet[i][0]
            print(group_num)

            session.add(
                Groups(
                    group_num=group_num,
                    group_info=group_info
                )
            )

    commands_sheet = spreadsheet['Commands']
    existing_commands = [command.name for command in session.query(Command).all()]

    for i in range(1, len(commands_sheet)):
        name = commands_sheet[i][0]
        print(name)

        if name not in existing_commands:
            arguments = commands_sheet[i][1]
            desc = commands_sheet[i][2]
            admin = True if commands_sheet[i][3] == '1' else False

            session.add(
                Command(
                    name=name,
                    arguments=arguments,
                    desc=desc,
                    admin=admin
                )
            )

    sendings_sheet = spreadsheet['Sendings']
    existing_sengings = [sending.mail_name for sending in session.query(Sendings).all()]

    for i in range(1, len(sendings_sheet)):
        name = sendings_sheet[i][0]
        print(name)

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

    organizers_sheet = spreadsheet['Organizers']
    existing_organizers = [organizer.chat_id for organizer in session.query(Orgs).all()]

    for i in range(1, len(organizers_sheet)):
        chat_id = organizers_sheet[i][0]
        print(chat_id)

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

    guests_sheet = spreadsheet['Guests']
    existing_guests = [guest.chat_id for guest in session.query(Guests).all()]

    for i in range(1, len(guests_sheet)):
        chat_id = guests_sheet[i][0]
        print(chat_id)

        if chat_id not in existing_guests:
            surname = guests_sheet[i][1]
            name = guests_sheet[i][2]
            patronymic = guests_sheet[i][3]
            phone_number = guests_sheet[i][4]
            tag = guests_sheet[i][5]
            vk_link = guests_sheet[i][6]
            groups = guests_sheet[i][7]
            texts = guests_sheet[i][8]

            session.add(
                Guests(
                    chat_id=chat_id,
                    surname=surname,
                    name=name,
                    patronymic=patronymic,
                    phone_number=phone_number,
                    tag=tag,
                    vk_link=vk_link,
                    groups=f'[{groups}]',
                    texts=f'[{texts}]'
                )
            )

    session.commit()
