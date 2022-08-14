import schedule
from spreadsheet_parser import get_data

# interval between spreadsheet check
PARSER_SLEEP_TIME = 30


def start_auto_parsing(
        spreadsheet_id: str,
        creds_file_name: str = 'credentials.json',
        token_file_name: str = 'token.json'
):
    schedule.every(PARSER_SLEEP_TIME).minutes.do(get_data(spreadsheet_id, creds_file_name, token_file_name))
