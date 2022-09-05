import json
import logging

import vk_api.vk_api
from sqlalchemy.orm import Session

from app.vk_tools.google.spreadsheet_parser.spreadsheet_parser import get_data
from app.create_db import Sendings, Orgs, Groups, Command, Guests, Info, Notifications, Missing
from app.vk_tools.utils.make_domain import make_domain
from app.vk_tools.utils.upload import upload_photo, upload_pdf_doc
from app.vk_events.send_message import send_message


def get_init_data(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str,
) -> None:
    # Подключение логов
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    spreadsheet = get_data(
        spreadsheet_id,
        creds_file_name,
        token_file_name
    )


    # getting info about notifications
    notification_sheet = spreadsheet['Notifications']

    for i in range(1, len(notification_sheet)):
        group_num = int(notification_sheet[i][0])
        desc = notification_sheet[i][1]

        if group_num is not None:
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

    session.commit()

    # getting info about guests' groups
    groups_sheet = spreadsheet['Levels']

    for i in range(1, len(groups_sheet)):
        group_num = int(groups_sheet[i][0])
        group_info = groups_sheet[i][1]

        if group_num is not None:

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

    session.commit()

    # getting info about commands for calling
    commands_sheet = spreadsheet['Commands']

    for i in range(1, len(commands_sheet)):
        name = commands_sheet[i][0]
        arguments = commands_sheet[i][1]
        desc = commands_sheet[i][2]
        admin = True if commands_sheet[i][3] == '1' else False

        if name is not None:

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

    session.commit()

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

        if name is not None:

            pic_ids = []
            if pics:
                pics_json = f'[{pics}]'

                for pic in json.loads(pics_json):
                    pic_id = upload_photo(
                        vk=vk,
                        photo_id=pic,
                        image_file_path=f'./app/vk_tools/google/spreadsheet_parser/attachments/{pic}.png'
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
                        doc_file_path=f'./app/vk_tools/google/spreadsheet_parser/attachments/{doc}.pdf'
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

    session.commit()

    # getting info about users with admin rights
    organizers_sheet = spreadsheet['Organizers']

    for i in range(1, len(organizers_sheet)):
        chat_id = int(organizers_sheet[i][0])
        surname = organizers_sheet[i][1]
        name = organizers_sheet[i][2]
        patronymic = organizers_sheet[i][3]
        vk_link = make_domain(organizers_sheet[i][4])
        groups = organizers_sheet[i][5]

        if chat_id is not None:

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

    session.commit()

    # getting info about participants
    guests_sheet = spreadsheet['Guests']

    for i in range(1, len(guests_sheet)):
        surname = guests_sheet[i][0]
        name = guests_sheet[i][1]
        patronymic = guests_sheet[i][2]
        phone_number = guests_sheet[i][22]
        tag = guests_sheet[i][24]
        vk_link = make_domain(guests_sheet[i][23])

        if vk_link is not None:

            guest = session.query(Guests).filter_by(vk_link=vk_link).first()

            if guest:
                guest.surname = surname
                guest.name = name
                guest.patronymic = patronymic
                guest.phone_number = phone_number
                guest.tag = tag

                groups = json.loads(f'[{guests_sheet[i][30]}]') if guests_sheet[i][30] else None
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

    session.commit()

    info_sheet = spreadsheet['Info']

    for i in range (1, len(info_sheet)):
        info_question = info_sheet[i][0]
        info_answer = info_sheet[i][1]

        if info_question is not None:

            info_button = session.query(Info).filter_by(question=info_question).first()

            if info_button:
                info_button.answer = info_answer
            else:
                session.add(
                    Info(
                        question=info_question,
                        answer=info_answer
                    )
                )


    session.commit()


    missing_sheet = spreadsheet['Missing']

    for i in range (1, len(missing_sheet)):
        missing_button = missing_sheet[i][0]
        missing_answer = missing_sheet[i][1]

        if missing_button is not None:

            missed = session.query(Missing).filter_by(button=missing_button).first()

            if missed:
                missed.answer = missing_answer
            else:
                session.add(
                    Missing(
                        button=missing_button,
                        answer=missing_answer
                    )
                )


    session.commit()
