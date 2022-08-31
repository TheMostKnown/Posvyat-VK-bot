from googleapiclient.discovery import build

from app.config import settings
from app.vk_tools.google.get_creds import get_creds


def get_data(
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str
) -> dict:
    """Retrieves all non-empty rows from spreadsheet

    :param creds_file_name:
    :param spreadsheet_id: id of google spreadsheet
    :type spreadsheet_id: str

    :param creds_file_name: absolute path to the file with saved credentials
    :type creds_file_name: str

    :param token_file_name : absolute path to the file with saved auth token
    :type token_file_name: str

    :return: all sheets' data in lists
    :rtype: dict
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

            row_data = data['rowData']

            for i, row in enumerate(row_data):
                if 'values' in row.keys():
                    for j, value in enumerate(row['values']):
                        if value and 'formattedValue' in value.keys():
                            row['values'][j] = value['formattedValue']
                        else:
                            row['values'][j] = None

                    tables[sheet_title].append(row['values'])
                else:
                    tables[sheet_title].append(None)

    return tables


class SpreadsheetError(Exception):
    pass


class SpreadsheetNotSetError(SpreadsheetError):
    pass


class SheetNotSetError(SpreadsheetError):
    pass


class Spreadsheet:
    def __init__(self):
        self.credentials = get_creds(
            settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
            settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH
        )
        self.service = build('sheets', 'v4', credentials=self.credentials, cache_discovery=False)
        self.drive_service = build('drive', 'v3', credentials=self.credentials, cache_discovery=False)
        self.spreadsheet_id = None
        self.sheet_id = None
        self.sheet_title = None
        self.requests = []
        self.value_ranges = []
        self.folder_id = settings.GOOGLE_FOLDER_ID

    def create(self, title, sheet_title, rows=1000, cols=26, locale='ru_RU', time_zone='Europe/Moscow'):
        spreadsheet = self.service.spreadsheets().create(body={
            'properties': {'title': title, 'locale': locale, 'timeZone': time_zone},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                       'sheetId': 0,
                                       'title': sheet_title,
                                       'gridProperties': {'rowCount': rows, 'columnCount': cols}}}]
        }).execute()
        self.spreadsheet_id = spreadsheet['spreadsheetId']
        self.sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']
        self.sheet_title = spreadsheet['sheets'][0]['properties']['title']

        self.drive_service.files().update(fileId=self.spreadsheet_id,
                                          addParents=self.folder_id,
                                          removeParents='root').execute()

    def share(self, share_request_body):
        if self.spreadsheet_id is None:
            raise SpreadsheetNotSetError()
        if self.drive_service is None:
            self.drive_service = build('drive', 'v3', credentials=self.credentials, cache_discovery=False)
        share_res = self.drive_service.permissions().create(
            fileId=self.spreadsheet_id,
            body=share_request_body,
            fields='id'
        ).execute()

    def share_with_email_for_reading(self, email):
        self.share({'type': 'user', 'role': 'reader', 'emailAddress': email})

    def share_with_email_for_writing(self, email):
        self.share({'type': 'user', 'role': 'writer', 'emailAddress': email})

    def share_with_anybody_for_reading(self):
        self.share({'type': 'anyone', 'role': 'reader'})

    def share_with_anybody_for_writing(self):
        self.share({'type': 'anyone', 'role': 'writer'})

    def get_sheet_url(self):
        if self.spreadsheet_id is None:
            raise SpreadsheetNotSetError()
        if self.sheet_id is None:
            raise SheetNotSetError()
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet_id + '/edit#gid=' + str(self.sheet_id)

    def get_spreadsheet_url(self):
        if self.spreadsheet_id is None:
            raise SpreadsheetNotSetError()
        if self.sheet_id is None:
            raise SheetNotSetError()
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet_id + '/edit'

    # Sets current spreadsheet by id; set current sheet as first sheet of this spreadsheet
    def set_spreadsheet_by_id(self, spreadsheet_id):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        self.spreadsheet_id = spreadsheet['spreadsheetId']
        self.sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']
        self.sheet_title = spreadsheet['sheets'][0]['properties']['title']

    # spreadsheets.batchUpdate and spreadsheets.values.batchUpdate
    def run_prepared(self, value_input_option="USER_ENTERED"):
        if self.spreadsheet_id is None:
            raise SpreadsheetNotSetError()
        upd1_res = {'replies': []}
        upd2_res = {'responses': []}
        try:
            if len(self.requests) > 0:
                upd1_res = self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={"requests": self.requests}).execute()
            if len(self.value_ranges) > 0:
                upd2_res = self.service.spreadsheets().values().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={"valueInputOption": value_input_option, "data": self.value_ranges}
                ).execute()
        finally:
            self.requests = []
            self.value_ranges = []
        return upd1_res['replies'], upd2_res['responses']

    def prepare_add_sheet(self, sheet_title, rows=1000, cols=26):
        self.requests.append({"addSheet": {
            "properties": {
                "title": sheet_title,
                'gridProperties': {'rowCount': rows,
                                   'columnCount': cols}
            }
        }})

    # Adds new sheet to current spreadsheet, sets as current sheet and returns its id
    def add_sheet(self, sheet_title, rows=1000, cols=26):
        if self.spreadsheet_id is None:
            raise SpreadsheetNotSetError()
        self.prepare_add_sheet(sheet_title, rows, cols)
        added_sheet = self.run_prepared()[0][0]['addSheet']['properties']
        self.sheet_id = added_sheet['sheetId']
        self.sheet_title = added_sheet['title']
        return self.sheet_id

    # Converts string range to GridRange of current sheet; examples:
    # "A3:B4" -> {sheetId: id of current sheet, startRowIndex: 2, endRowIndex: 4, startColumnIndex: 0, endColumnIndex:2}
    # "A5:B"  -> {sheetId: id of current sheet, startRowIndex: 4, startColumnIndex: 0, endColumnIndex: 2}
    def to_grid_range(self, cells_range):
        if self.sheet_id is None:
            raise SheetNotSetError()
        if isinstance(cells_range, str):
            start_cell, end_cell = cells_range.split(":")[0:2]
            cells_range = {}
            range_az = range(ord('A'), ord('Z') + 1)
            if ord(start_cell[0]) in range_az:
                cells_range["startColumnIndex"] = ord(start_cell[0]) - ord('A')
                start_cell = start_cell[1:]
            if ord(end_cell[0]) in range_az:
                cells_range["endColumnIndex"] = ord(end_cell[0]) - ord('A') + 1
                end_cell = end_cell[1:]
            if len(start_cell) > 0:
                cells_range["startRowIndex"] = int(start_cell) - 1
            if len(end_cell) > 0:
                cells_range["endRowIndex"] = int(end_cell)
        cells_range["sheetId"] = self.sheet_id
        return cells_range

    def prepare_set_dimension_pixel_size(self, dimension, start_index, end_index, pixel_size):
        if self.sheet_id is None:
            raise SheetNotSetError()
        self.requests.append({"updateDimensionProperties": {
            "range": {"sheetId": self.sheet_id,
                      "dimension": dimension,
                      "startIndex": start_index,
                      "endIndex": end_index},
            "properties": {"pixelSize": pixel_size},
            "fields": "pixelSize"}})

    def prepare_set_columns_width(self, start_col, end_col, width):
        self.prepare_set_dimension_pixel_size("COLUMNS", start_col, end_col + 1, width)

    def prepare_set_column_width(self, col, width):
        self.prepare_set_columns_width(col, col, width)

    def prepare_set_rows_height(self, start_row, end_row, height):
        self.prepare_set_dimension_pixel_size("ROWS", start_row, end_row + 1, height)

    def prepare_set_row_height(self, row, height):
        self.prepare_set_rows_height(row, row, height)

    def prepare_set_values(self, cells_range, values, major_dimension="ROWS"):
        if self.sheet_title is None:
            raise SheetNotSetError()
        self.value_ranges.append({"range": self.sheet_title + "!" + cells_range,
                                  "majorDimension": major_dimension,
                                  "values": values})

    def prepare_merge_cells(self, cells_range, merge_type="MERGE_ALL"):
        self.requests.append({"mergeCells": {"range": self.to_grid_range(cells_range), "mergeType": merge_type}})

    # formatJSON should be dict with userEnteredFormat to be applied to each cell
    def prepare_set_cells_format(self, cells_range, format_json, fields="userEnteredFormat"):
        self.requests.append({"repeatCell": {"range": self.to_grid_range(cells_range),
                                             "cell": {"userEnteredFormat": format_json},
                                             "fields": fields}})

    # formatsJSON should be list of lists of dicts with userEnteredFormat for each cell in each row
    def prepare_set_cells_formats(self, cells_range, formats_json, fields="userEnteredFormat"):
        self.requests.append({"updateCells": {
            "range": self.to_grid_range(cells_range),
            "rows": [{
                "values": [{
                    "userEnteredFormat": cell_format
                } for cell_format in row_formats]
            } for row_formats in formats_json],
            "fields": fields
        }})
