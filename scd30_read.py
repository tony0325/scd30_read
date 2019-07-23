from __future__ import print_function
import pickle
import os.path
import os
import subprocess
import re
import datetime
import time
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1b1PhUtSRn5snNOJwITrghV3i8SzyDR1g-ByI8othweY'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'
T = 1 # Interval of reading

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
 #   sheet = service.spreadsheets()
 #   result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
 #                               range=SAMPLE_RANGE_NAME).execute()
 #   values = result.get('values', [])

 #   if not values:
 #       print('No data found.')
 #   else:
 #       print('Name, Major:')
 #       for row in values:
 #           # Print columns A and E, which correspond to indices 0 and 4.
 #           print('%s, %s' % (row[0], row[1]))
   
    while True:
        try:
            while True:
                cmd = ['sudo','python','/home/pi/SCD30/Raspi-Driver-SCD30/scd30-once.py'] 
                try:
                    out = subprocess.check_output(cmd)
                    split_out = re.split(' |\n',out)
                    time_now = str(datetime.datetime.now())
                    co2 = split_out[1]
                    temp = split_out[3]
                    humidity = split_out[5]
                except:
                    print('Return error!')
                
                values = [
                [
                    time_now, co2, temp, humidity
                ],
                # Additional rows ...
                ]
                body = {
                    'values': values
                }
                result = service.spreadsheets().values().append(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Class Data!A2',
                    valueInputOption='USER_ENTERED', body=body).execute()
                #print('{0} cells appended.'.format(result \
                #                            .get('updates') \
                #                            .get('updatedCells')))
                
                time.sleep(T)
        
        except IndexError:
            print("  Unable to read")
        except KeyboardInterrupt:
            print("  Exiting by user")
            sys.exit(0)

if __name__ == '__main__':
    main()
