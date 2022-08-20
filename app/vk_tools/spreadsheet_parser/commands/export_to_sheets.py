from vk_api.bot_longpoll import VkBotEvent
import vk_api
from typing import List, Optional
from sqlalchemy.orm import Session
from validate_email import validate_email
from datetime import datetime

from app.create_db import Sendings, Guests, Orgs, Groups
from app.vk_tools.spreadsheet_parser.spreadsheet_parser import Spreadsheet
import update_sheet
from app.vk_events.send_message import send_message


# args = [email]
def sendings_from_db(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of creating a spreadsheet with data from the Sending table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """
    params = {}
    if args:
        if not validate_email(args[0]):
            return 9
        params['email'] = args[0]

    spreadsheet = Spreadsheet()
    spreadsheet.create(title=f'Имеющиеся в БД рассылки на {datetime.now()}',
                       sheet_title='Sendings')

    if params:
        spreadsheet.share_with_email_for_writing(params['email'])
    else:
        spreadsheet.share_with_anybody_for_writing()

    update_sheet.sending_cells(spreadsheet, session.query(Sendings))

    chat_id = event.message['from_id'] if event.message \
        else event.object['user_id']

    send_message(
        vk=vk,
        chat_id=chat_id,
        text=spreadsheet.get_sheet_url()
    )

    session.commit()
    return 0


# args = [email]
def guest_from_db(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of creating a spreadsheet with data from the Guest table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """
    params = {}
    if args:
        if not validate_email(args[0]):
            return 9
        params['email'] = args[0]

    spreadsheet = Spreadsheet()
    spreadsheet.create(title=f'Имеющиеся в БД гости на {datetime.now()}',
                       sheet_title='Guests')

    if params:
        spreadsheet.share_with_email_for_writing(params['email'])
    else:
        spreadsheet.share_with_anybody_for_writing()

    update_sheet.guest_cells(spreadsheet, session.query(Guests))

    chat_id = event.message['from_id'] if event.message \
        else event.object['user_id']

    send_message(
        vk=vk,
        chat_id=chat_id,
        text=spreadsheet.get_sheet_url()
    )

    session.commit()
    return 0


# args = [email]
def organizers_from_db(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of creating a spreadsheet with data from the Orgs table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """
    params = {}
    if args:
        if not validate_email(args[0]):
            return 9
        params['email'] = args[0]

    spreadsheet = Spreadsheet()
    spreadsheet.create(title=f'Имеющиеся в БД организаторы на {datetime.now()}',
                       sheet_title='Orgs')

    if params:
        spreadsheet.share_with_email_for_writing(params['email'])
    else:
        spreadsheet.share_with_anybody_for_writing()

    update_sheet.organizer_cells(spreadsheet, session.query(Guests))

    chat_id = event.message['from_id'] if event.message \
        else event.object['user_id']

    send_message(
        vk=vk,
        chat_id=chat_id,
        text=spreadsheet.get_sheet_url()
    )

    session.commit()
    return 0


# args = [email]
def groups_from_db(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of creating a spreadsheet with data from the Groups table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """
    params = {}
    if args:
        if not validate_email(args[0]):
            return 9
        params['email'] = args[0]

    spreadsheet = Spreadsheet()
    spreadsheet.create(title=f'Имеющиеся в БД группы на {datetime.now()}',
                       sheet_title='Groups')

    if params:
        spreadsheet.share_with_email_for_writing(params['email'])
    else:
        spreadsheet.share_with_anybody_for_writing()

    update_sheet.group_cells(spreadsheet, session.query(Groups))

    chat_id = event.message['from_id'] if event.message \
        else event.object['user_id']

    send_message(
        vk=vk,
        chat_id=chat_id,
        text=spreadsheet.get_sheet_url()
    )

    session.commit()
    return 0


# args = [email]
def all_from_db(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of creating a spreadsheet with data from all tables in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """
    params = {}
    if args:
        if not validate_email(args[0]):
            return 9
        params['email'] = args[0]

    spreadsheet = Spreadsheet()
    spreadsheet.create(title=f'Имеющиеся в БД данные на {datetime.now()}',
                       sheet_title='Guests')
    update_sheet.guest_cells(spreadsheet, session.query(Guests))

    spreadsheet.add_sheet(sheet_title='Orgs')
    update_sheet.organizer_cells(spreadsheet, session.query(Orgs))

    spreadsheet.add_sheet(sheet_title='Sendings')
    update_sheet.sending_cells(spreadsheet, session.query(Sendings))

    spreadsheet.add_sheet(sheet_title='Group')
    update_sheet.group_cells(spreadsheet, session.query(Groups))

    chat_id = event.message['from_id'] if event.message \
        else event.object['user_id']
    send_message(
        vk=vk,
        chat_id=chat_id,
        text=spreadsheet.get_spreadsheet_url()
    )

    session.commit()
    return 0
