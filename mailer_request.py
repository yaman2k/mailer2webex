import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

MAILER_TOKEN = os.environ.get("MAILER_TOKEN")
MAILER_BASE_URL = os.environ.get("MAILER_BASE_URL")

payload = {}
headers = {
  'Authorization': 'Basic ' + MAILER_TOKEN,
}

#function that would get the mailer name and retrieve the list of members
#it returns status code, mail members and members count
def mailer_members(mailer):
  response = requests.request("GET", MAILER_BASE_URL+mailer, headers=headers, data = payload)
  if response.status_code != 200:
    print("there's an error!")

  #save response in JSON format
  user_data = response.json()

  #check if API comes back with an error (dictionary message)
  if (isinstance(user_data['members'][0],dict)):
    response.status_code = 400

  #count members in the mailer to send back
  user_count = str(len(user_data['members']))

  
  return(response.status_code,user_data,user_count)

