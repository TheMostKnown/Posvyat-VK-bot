from typing import List

from app.create_db import Guests, Orgs, Groups, Sendings
from app.vk_tools.spreadsheet_parser.spreadsheet_parser import Spreadsheet


def sending_cells(spreadsheet: Spreadsheet, sendings: List[Sendings]):
    cells_range = f'A:F'
    spreadsheet.prepare_set_values(
        cells_range=cells_range,
        values=[['mail_name'] + [sending.mail_name for sending in sendings],
                ['text'] + [sending.text for sending in sendings],
                ['pics'] + [sending.pics for sending in sendings],
                ['video'] + [sending.video for sending in sendings],
                ['reposts'] + [sending.reposts for sending in sendings],
                ['docs'] + [sending.docs for sending in sendings],
                ['group_num'] + [str(sending.group_num) for sending in sendings],
                ['send_time'] + [sending.send_time.strftime("%d/%m/%Y %H:%M:%S") if sending.send_time
                                 else None for sending in sendings]],
        major_dimension='COLUMNS')

    spreadsheet.prepare_set_cells_format('A:F', {'wrapStrategy': 'WRAP',
                                                 'horizontalAlignment': 'CENTER',
                                                 'verticalAlignment': 'MIDDLE'})
    spreadsheet.prepare_set_cells_format('D:D', {'wrapStrategy': 'WRAP',
                                                 'horizontalAlignment': 'LEFT',
                                                 'verticalAlignment': 'MIDDLE'})
    spreadsheet.prepare_set_columns_width(0, 1, 50)
    spreadsheet.prepare_set_columns_width(2, 6, 150)
    spreadsheet.prepare_set_column_width(3, 380)
    spreadsheet.prepare_set_cells_format('F:F', {'wrapStrategy': 'WRAP',
                                                 'horizontalAlignment': 'CENTER',
                                                 'verticalAlignment': 'MIDDLE',
                                                 'numberFormat': {'type': 'DATE_TIME',
                                                                  'pattern': ''}})

    spreadsheet.run_prepared()


def guest_cells(spreadsheet: Spreadsheet, guests: List[Guests]):
    cells_range = f'A:I'
    spreadsheet.prepare_set_values(
        cells_range=cells_range,
        values=[['id'] + [str(guest.id) for guest in guests],
                ['vk_link'] + [guest.vk_link for guest in guests],
                ['tg_tag'] + [guest.tag for guest in guests],
                ['first_name'] + [guest.name for guest in guests],
                ['last_name'] + [guest.surname for guest in guests],
                ['patronymic'] + [guest.patronymic for guest in guests],
                ['group'] + [guest.groups for guest in guests],
                ['texts'] + [guest.texts for guest in guests]],
        major_dimension='COLUMNS')

    spreadsheet.prepare_set_cells_format('A:I', {'wrapStrategy': 'WRAP',
                                                 'horizontalAlignment': 'CENTER',
                                                 'verticalAlignment': 'MIDDLE'})
    spreadsheet.prepare_set_columns_width(0, 6, 100)
    spreadsheet.prepare_set_column_width(7, 380)
    spreadsheet.prepare_set_column_width(8, 150)
    spreadsheet.prepare_set_cells_format('I:I', {'wrapStrategy': 'WRAP',
                                                 'horizontalAlignment': 'CENTER',
                                                 'verticalAlignment': 'MIDDLE',
                                                 'numberFormat': {'type': 'DATE_TIME',
                                                                  'pattern': ''}})

    spreadsheet.run_prepared()


def organizer_cells(spreadsheet: Spreadsheet, orgs: List[Orgs]):
    cells_range = f'A:I'
    spreadsheet.prepare_set_values(
        cells_range=cells_range,
        values=[['id'] + [str(org.id) for org in orgs],
                ['vk_link'] + [org.vk_org_link for org in orgs],
                ['first_name'] + [org.name for org in orgs],
                ['last_name'] + [org.surname for org in orgs],
                ['patronymic'] + [org.patronymic for org in orgs],
                ['group'] + [org.groups for org in orgs]],
        major_dimension='COLUMNS')

    spreadsheet.prepare_set_cells_format('A:I', {'wrapStrategy': 'WRAP',
                                                 'horizontalAlignment': 'CENTER',
                                                 'verticalAlignment': 'MIDDLE'})
    spreadsheet.prepare_set_columns_width(0, 6, 100)
    spreadsheet.prepare_set_column_width(7, 380)
    spreadsheet.prepare_set_column_width(8, 150)
    spreadsheet.prepare_set_cells_format('I:I', {'wrapStrategy': 'WRAP',
                                                 'horizontalAlignment': 'CENTER',
                                                 'verticalAlignment': 'MIDDLE',
                                                 'numberFormat': {'type': 'DATE_TIME',
                                                                  'pattern': ''}})

    spreadsheet.run_prepared()


def group_cells(spreadsheet: Spreadsheet, groups: List[Groups]):
    cells_range = f'A:C'
    spreadsheet.prepare_set_values(
        cells_range=cells_range,
        values=[['group_num'] + [str(group.group_num) for group in groups],
                ['group_info'] + [group.group_info for group in groups]],
        major_dimension='COLUMNS')

    spreadsheet.prepare_set_cells_format('A:C', {'wrapStrategy': 'WRAP',
                                                 'horizontalAlignment': 'CENTER',
                                                 'verticalAlignment': 'MIDDLE'})
    spreadsheet.prepare_set_column_width(0, 100)
    spreadsheet.prepare_set_column_width(1, 350)
    spreadsheet.prepare_set_column_width(2, 150)
    spreadsheet.prepare_set_cells_format('C:C', {'wrapStrategy': 'WRAP',
                                                 'horizontalAlignment': 'CENTER',
                                                 'verticalAlignment': 'MIDDLE',
                                                 'numberFormat': {'type': 'DATE_TIME',
                                                                  'pattern': ''}})

    spreadsheet.run_prepared()
