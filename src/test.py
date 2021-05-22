import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

state = 'Delhi'

def getCovidInfo(state):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("coronastatus").sheet1  # Open the spreadhseet
    data = sheet.get_all_records()
    #pprint(data)
    df = pd.DataFrame.from_dict(data)
    #pprint(df)

    row = df.loc[df['State'] == state]
    #print(row)
    confirmed = row['Confirmed']
    confirmed = confirmed.to_string(index = False)

    #pprint(confirmed)

    active = row['Active']
    active = active.to_string(index = False)

    recover = row['Recovered']
    recover = recover.to_string(index = False)

    deaths = row['Deaths']
    deaths = deaths.to_string(index = False)

    time = row['Last_Updated_Time']
    time = time.to_string(index = False)

    

if __name__ == "__main__":
    State = 'Maharashtra'
    getCovidInfo(State)
    #confirmed, active , recover , deaths = getCovidInfo(State)
    #print(confirmed)
    #print(active)
    #print(recover)
    #print(deaths)

