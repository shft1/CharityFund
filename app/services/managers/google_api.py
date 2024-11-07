from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(
        wrapper_service: Aiogoogle
):
    time_now = datetime.now().strftime(FORMAT)
    methods_sheets_api = await wrapper_service.discover(
        'sheets', 'v4'
    )
    spreadsheets_body = {
        'properties': {'title': f'Отчёт на {time_now}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetId': 0,
                                   'sheetType': 'GRID',
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 10}}}]
    }
    response = await wrapper_service.as_account(
        methods_sheets_api.spreadsheets.create(json=spreadsheets_body)
    )
    spreadsheets_id = response['spreadsheetId']
    print(f'https://docs.google.com/spreadsheets/d/{spreadsheets_id}')
    return spreadsheets_id


async def set_user_permissions(
        wrapper_service: Aiogoogle,
        spreadsheet_id: str
):
    methods_drive_api = await wrapper_service.discover(
        'drive', 'v3'
    )
    permission_body = {'type': 'user',
                       'role': 'writer',
                       'emailAddress': settings.email}
    await wrapper_service.as_account(
        methods_drive_api.permissions.create(
            fileId=spreadsheet_id,
            json=permission_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        wrapper_service: Aiogoogle,
        projects: list[CharityProject],
        spreadsheet_id: str
):
    time_now = datetime.now().strftime(FORMAT)
    methods_sheets_api = await wrapper_service.discover(
        'sheets', 'v4'
    )
    table_value = [
        ['Отчет от', time_now],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        closing_time = str(project.close_date - project.create_date)
        table_value.append([project.name, closing_time, project.description])

    update_body = {'majorDimension': 'ROWS',
                   'values': table_value}

    await wrapper_service.as_account(
        methods_sheets_api.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
