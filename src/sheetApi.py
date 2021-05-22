#importing the necessary files

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

#error message for when location is wrong or not given in the tweet
ERROR = "Please check your tweet , and retweet"


#this methods takes in the location and where (district/state) and returns all the info of the location .If location is wrong it returns error message
def getCovidInfo(location , where):
    
    #accessing our spreadsheet and google drive api
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    #creating credentials to access out spreadsheet
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when we enable spreadsheet api
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    #authorizing the clientsheet
    client = gspread.authorize(creds)

    
     # Open the spreadhseet
    
    #when location is not found i.e where == 0 we return error message
    if where == 0:
        return ERROR;
    
    #when location is a district
    if where == 1:

        #creating an instance of district sheet
        dSheet = client.open("coronastatus").get_worksheet(1)

        #storing all data sheet data in a list
        districtData = dSheet.get_all_records()

        #converting list to a dataframe using pandas
        districtDf = pd.DataFrame.from_dict(districtData)

        #accessing the row with the given location
        row = districtDf.loc[districtDf['District'] == location]

        #creating a message if numbers are outdated
        outdated = "District-wise numbers are out-dated"

        #accessing district note
        district_note = row['District_Notes']

        #converting district note to string 
        district_note = district_note.to_string(index = False)

        #returning outdated text if data is outdated or unreported
        if(outdated in district_note):
            return "In {0} , {1} or unreported".format(location , outdated)

        
    #if the location is a state
    if where == 2:

        #creating an instance of state sheet
        sSheet = client.open("coronastatus").sheet1 

        #storing all data sheet data in a list
        stateData = sSheet.get_all_records() 

        #converting list to a dataframe using pandas
        stateDf = pd.DataFrame.from_dict(stateData)

        #accessing the row with the given location
        row = stateDf.loc[stateDf['State'] == location]
        

    #creating a list of hastags to add to the replying tweet
    hashtags = [ "#covid19"]

    
    #getting confirmed covid cases number of location and convering to string
    confirmed = row['Confirmed']
    confirmed = confirmed.to_string(index = False)

    #getting active covid cases number of location and convering to string
    active = row['Active']
    active = active.to_string(index = False)

    #getting recovered covid cases number of location and convering to string
    recover = row['Recovered']
    recover = recover.to_string(index = False)

    #when location is a state
    if where == 2 :
        #getting death number of location and convering to string
        deaths = row['Deaths']
        deaths = deaths.to_string(index = False)

        #getting the last time when data was updated and convering to string
        time = row['Last_Updated_Time']
        time = time.to_string(index = False)
        
        #creating a tweet using the all the state data found
        tweet = '{0} has Total {1} Confirmed Cases out of which {2} are recovered cases , {3} Active cases and {4} Deaths -- last updated at {5} IST . #{6} {7}'.format(location , confirmed , recover, active , deaths , time ,location, ' '.join(hashtags))
    

    #when location is a district
    if where == 1:
        #getting death number of location and convering to string
        deaths = row['Deceased']
        deaths = deaths.to_string(index = False)

        #creating a tweet using the all the district data found
        tweet = '{0} has Total {1} Confirmed Cases out of which {2} are recovered cases , {3} Active cases and {4} Deaths . #{5} {6}'.format(location , confirmed , recover, active , deaths ,location, ' '.join(hashtags))
    
    #returning the text to tweet to the user
    return tweet
