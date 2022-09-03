import json
import logging
import re

import vk_api.vk_api
from sqlalchemy.orm import Session

from app.google.spreadsheet_parser.spreadsheet_parser import get_data
from app.create_db import Sendings, Orgs, Groups, Command, Guests, Info, UpdateTimer, Notifications
from app.utils.upload import upload_photo, upload_pdf_doc
from app.send_message import send_message


def make_domain(link: str) -> str:
    domain = re.sub(r'[@*]?|(.*vk.com/)', '', link.lower())

    return domain


def get_init_data(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str,
) -> None:
    # Подключение логов
    logger = logging.getLogger(__name__)

    spreadsheet = get_data(
        spreadsheet_id,
        creds_file_name,
        token_file_name
    )

    # getting autoparser timer
    timer_sheet = spreadsheet['Timer']

    timer = session.query(UpdateTimer).first()

    if timer:
        timer.update_timer = int(timer_sheet[0][0])
    else:
        session.add(
            UpdateTimer(update_timer=int(timer_sheet[0][0]))
        )

    # getting info about notifications
    notification_sheet = spreadsheet['Notifications']

    for i in range(1, len(notification_sheet)):
        group_num = int(notification_sheet[i][0])
        desc = notification_sheet[i][1]

        notification = session.query(Notifications).filter_by(group_num=group_num).first()

        if notification:
            notification.desc = desc
        else:
            session.add(
                Notifications(
                    group_num=group_num,
                    desc=desc
                )
            )

    # getting info about guests' groups
    groups_sheet = spreadsheet['Levels']

    for i in range(1, len(groups_sheet)):
        group_num = int(groups_sheet[i][0])
        group_info = groups_sheet[i][1]

        group = session.query(Groups).filter_by(group_num=group_num).first()

        if group:
            group.group_info = group_info
        else:
            session.add(
                Groups(
                    group_num=group_num,
                    group_info=group_info
                )
            )

    # getting info about commands for calling
    commands_sheet = spreadsheet['Commands']

    for i in range(1, len(commands_sheet)):
        name = commands_sheet[i][0]
        arguments = commands_sheet[i][1]
        desc = commands_sheet[i][2]
        admin = True if commands_sheet[i][3] == '1' else False

        command = session.query(Command).filter_by(name=name).first()

        if command:
            command.arguments = arguments
            command.desc = desc
            command.admin = admin
        else:
            session.add(
                Command(
                    name=name,
                    arguments=arguments,
                    desc=desc,
                    admin=admin
                )
            )

    # getting info about mailings
    sendings_sheet = spreadsheet['Sendings']

    for i in range(1, len(sendings_sheet)):
        name = sendings_sheet[i][0]
        text = sendings_sheet[i][1]
        groups = sendings_sheet[i][2]
        send_time = sendings_sheet[i][3]
        pics = sendings_sheet[i][4]
        video = sendings_sheet[i][5]
        reposts = sendings_sheet[i][6]
        docs = sendings_sheet[i][7]

        pic_ids = []
        if pics:
            pics_json = f'[{pics}]'

            for pic in json.loads(pics_json):
                pic_id = upload_photo(
                    vk=vk,
                    photo_id=pic,
                    image_file_path=f'./app/google/spreadsheet_parser/attachments/{pic}.png'
                )

                if len(pic_id) != 0:
                    pic_ids.append(pic_id)

        logger.info(f'Pics: {pic_ids}')

        doc_ids = []
        if docs:
            docs_json = f'[{docs}]'

            for doc in json.loads(docs_json):
                doc_id = upload_pdf_doc(
                    vk=vk,
                    doc_id=doc,
                    doc_file_path=f'./app/google/spreadsheet_parser/attachments/{doc}.pdf'

                )

                if len(doc_id) != 0:
                    doc_ids.append(doc_id)

        logger.info(f'Docs: {doc_ids}')

        sending = session.query(Sendings).filter_by(mail_name=name).first()

        if sending:
            sending.send_time = send_time
            sending.groups = groups
            sending.text = text
            sending.pics = json.dumps(pic_ids) if len(pic_ids) > 0 else '[]'
            sending.video = f'[{video}]' if video else '[]'
            sending.reposts = f'[{reposts}]' if reposts else '[]'
            sending.docs = json.dumps(doc_ids) if docs else '[]'
        else:
            session.add(
                Sendings(
                    mail_name=name,
                    send_time=send_time,
                    groups=groups,
                    text=text,
                    pics=json.dumps(pic_ids) if len(pic_ids) > 0 else '[]',
                    video=f'[{video}]' if video else '[]',
                    reposts=f'[{reposts}]' if reposts else '[]',
                    docs=json.dumps(doc_ids) if docs else '[]'
                )
            )

    # getting info about users with admin rights
    organizers_sheet = spreadsheet['Organizers']

    for i in range(1, len(organizers_sheet)):
        chat_id = int(organizers_sheet[i][0])
        surname = organizers_sheet[i][1]
        name = organizers_sheet[i][2]
        patronymic = organizers_sheet[i][3]
        vk_link = make_domain(organizers_sheet[i][4])
        groups = organizers_sheet[i][5]

        organizer = session.query(Orgs).filter_by(chat_id=chat_id).first()

        if organizer:
            organizer.surname = surname
            organizer.name = name
            organizer.patronymic = patronymic
            organizer.vk_link = vk_link
            organizer.groups = groups
        else:
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

    # getting info about participants
    guests_sheet = spreadsheet['Guests']

    for i in range(1, len(guests_sheet)):
        surname = guests_sheet[i][0]
        name = guests_sheet[i][1]
        patronymic = guests_sheet[i][2]
        phone_number = guests_sheet[i][3]
        tag = guests_sheet[i][4]
        vk_link = make_domain(guests_sheet[i][5])

        guest = session.query(Guests).filter_by(vk_link=vk_link).first()

        if guest:
            guest.surname = surname
            guest.name = name
            guest.patronymic = patronymic
            guest.phone_number = phone_number
            guest.tag = tag

            groups = json.loads(f'[{guests_sheet[i][6]}]') if guests_sheet[i][6] else None
            existing_groups = json.loads(guest.groups)

            text = ''

            if groups and len(groups) > len(existing_groups):
                guest.groups = f'[{guests_sheet[i][6]}]'

                # если есть новые группы -> нужно отправить уведомление об этом
                for group in groups:
                    if group not in existing_groups:
                        info = session.query(Notifications).filter_by(group_num=int(group)).first()

                        if info:
                            text += f'{info.desc}\n'

                if len(text) != 0:
                    send_message(
                        vk=vk,
                        chat_id=guest.chat_id,
                        text=text
                    )

    info_sheet = spreadsheet['Info']
    existing_info = [information.question for information in session.query(Info).all()]

    for i in range (1, len(info_sheet)):

        info_question = info_sheet[i][0]

        if info_question not in existing_info:
            info_answer = info_sheet[i][1]

            session.add(
                Info(
                    question=info_question,
                    answer=info_answer
                )
            )


    session.commit()
