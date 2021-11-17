from __future__ import print_function
import os.path
from googleapiclient.discovery import build
import pandas as pd
from google.oauth2 import service_account


def senddata(data):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = "E:\СЬОПА НЕВЗ'ЄБЄННИЙ АЙТІШНИК!!!!!\Projects.2\CashBot\keys.json"

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    SAMPLE_SPREADSHEET_ID = '1yvblhiMNqW2oFxW0Osq-7ViUovNlIyoGVrnsu3Tw45Q'
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Main!A:G").execute()
    values = result.get('values', [])

    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Sec!A:C',
    valueInputOption="USER_ENTERED", body={"values": data})
    request.execute()   

