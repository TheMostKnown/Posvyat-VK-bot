import json

from sqlalchemy.orm import Session

from app.vk_tools.google.spreadsheet_parser.spreadsheet_parser import get_data
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

        if name not in existing_sengings:

            text = sendings_sheet[i][1]
            groups_str = sendings_sheet[i][2]
            send_time = sendings_sheet[i][3]
            pics = sendings_sheet[i][4]
            video = sendings_sheet[i][5]
            reposts = sendings_sheet[i][6]
            docs = sendings_sheet[i][7]

            if groups_str[0] != '!':
                groups_json = f'[{groups_str}]'
            else:
                unwanted_groups = json.loads(f'[{groups_str[1:]}]')
                groups = session.query(Groups).filter(Groups.id not in unwanted_groups).all()
                groups_json = json.dumps(groups)

            session.add(
                Sendings(
                    mail_name=name,
                    send_time=send_time,
                    groups=groups_json,
                    text=text,
                    pics=f'[{pics}]' if pics else '[]',
                    video=f'[{video}]' if video else '[]',
                    reposts=f'[{reposts}]' if reposts else '[]',
                    docs=f'[{docs}]' if docs else '[]'
                )
            )

    organizers_sheet = spreadsheet['Organizers']
    existing_organizers = [organizer.chat_id for organizer in session.query(Orgs).all()]

    for i in range(1, len(organizers_sheet)):
        chat_id = int(organizers_sheet[i][0])

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
    existing_guests = session.query(Guests).all()

    for i in range(1, len(guests_sheet)):
        vk_link = guests_sheet[i][6]

        for guest in existing_guests:

            if vk_link == guest.vk_link:
                guest.surname = guests_sheet[i][0]
                guest.name = guests_sheet[i][1]
                guest.patronymic = guests_sheet[i][2]
                guest.phone_number = guests_sheet[i][3]
                guest.tag = guests_sheet[i][4]

                groups = json.loads(f'[{guests_sheet[i][6]}]') if guests_sheet[i][6] else None
                guest_groups = json.loads(guest.groups)

                if groups and len(groups) > len(guest_groups):
                    guest.groups = f'[{guests_sheet[i][6]}]'

    session.commit()
