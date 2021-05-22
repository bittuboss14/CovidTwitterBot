#importing necessary libraries and files
from utility import *
import re
import string

#error message for when location is not found
ERROR = "Please check your tweet , and retweet"


#creating a set of stopwords
stop_words = set(stopwords)

#this method is used to clean the text and return the cleaned text
def text_preproc(x):
  #converting to lower case
  x = x.lower()

  #removinf stopwords
  x = ' '.join([word for word in x.split(' ') if word not in stop_words])
  
  #removing unicode characters
  x = x.encode('ascii', 'ignore').decode()
  
  #removing urls example - http://abc.com
  x = re.sub(r'https*\S+', ' ', x)
  
  #removing mentions example- @xyz @abc
  x = re.sub(r'@\S+', ' ', x)

  #removing hashtags example- #xyz #abc
  x = re.sub(r'#\S+', ' ', x)

  #removing ticks and the next character example- "Api's" is converted to "Api"
  x = re.sub(r'\'\w+', '', x)

  #removing punctuations 
  x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x)

  #removing numbers
  x = re.sub(r'\w*\d+\w*', '', x)

  #removing overspacing example - "  what      to" -> " what to"
  x = re.sub(r'\s{2,}', ' ', x)

  #returning the cleaned text
  return x

#method to find the location if not present then return error message
def findLocation(location):
  trigger = False
  #searching for the location among districts
  for district in districts:
    if district in location:
      trigger = True
      #returning location and variable "1" to tell that location is found among districts
      return district,1

  #searching for the location among states
  for state in states:
    if state in location:
      trigger = True
      #returning location and variable "2" to tell that location is found among states
      return state,2

  #if location is not found returning error message
  if(trigger == False):
    #returning error message and variable "0" to tell that location is not found 
    return ERROR,0
