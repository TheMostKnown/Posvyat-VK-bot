from app.vk_tools.google.spreadsheet_parser.spreadsheet_parser import get_data


def get_guests_status(
        spreadsheet_id: str,
        sheet_name: str,
        vk_link_column: int,
        status_column: int
) -> dict:
    guests = dict()

    try:
        guest_sheet = get_data(spreadsheet_id)[sheet_name]

        for row in guest_sheet:

            if row[vk_link_column]:

                if row[status_column]:
                    guests[vk_link_column] = row[status_column]
                else:
                    guests[vk_link_column] = ''

    except AttributeError as e:
        print(f'{e}: No such key in spreadsheet')

    return guests
