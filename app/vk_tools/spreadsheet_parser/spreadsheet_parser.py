import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_creds(creds_file: str, token_file: str) -> Credentials:
    """
    Parameter:
        creds_file : str
            name of the file with saved credentials
        token_file : str
            name of the file with saved auth token
    Returns:
        credentials for authorization in google api
    """

    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
              'https://www.googleapis.com/auth/drive']

    creds = None

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds


def get_data(
        spreadsheet_id: str,
        creds_file_name: str = 'credentials.json',
        token_file_name: str = 'token.json'
) -> dict:
    """
    Parameter:
        spreadsheet_id : str
            id of google spreadsheet
        creds_file : str
            name of the file with saved credentials
        token_file : str
            name of the file with saved auth token
    Returns:
        dict: all sheets' data in lists
    """

    tables = dict()

    creds = get_creds(creds_file_name, token_file_name)

    service = build('sheets', 'v4', credentials=creds)

    request = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        includeGridData=True
    )
    response = request.execute()

    sheets = response['sheets']

    for sheet in sheets:
        sheet_title = sheet['properties']['title']

        tables[sheet_title] = []

        grid_data = sheet['data']

        for data in grid_data:
            if 'rowData' not in data.keys():
                continue

            rowData = data['rowData']

            for i, row in enumerate(rowData):

                if 'values' in row.keys():

                    for j, value in enumerate(row['values']):

                        if value and 'formatted_value' in value.keys():
                            row['values'][j] = value['formatted_value']
                        else:
                            row['values'][j] = None

                    tables[sheet_title].append(row['values'])

                else:
                    tables[sheet_title].append(None)

    return tables
