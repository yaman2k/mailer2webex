#import needed modules/objects
import requests
import json
import os
from dotenv import load_dotenv

#load .env 
load_dotenv()

#define additional variables
CREATE_SPACE_URL = 'https://webexapis.com/v1/rooms'
CREATE_TEAM_URL = 'https://webexapis.com/v1/teams'
ADD_TO_SPACE_URL = 'https://webexapis.com/v1/memberships'
ADD_TO_TEAM_URL = 'https://webexapis.com/v1/team/memberships'
WEBEX_ACCESS_TOKEN = os.environ.get("WEBEX_ACCESS_TOKEN")

#define function that will create a Webex Space
def webex_create_space(room_title):
  headers = {
    'Authorization': 'Bearer ' + WEBEX_ACCESS_TOKEN, 
    'Content-type':'application/json'
  }

  post_data = {
    'title' : room_title
  }

  response = requests.post(CREATE_SPACE_URL, json=post_data, headers=headers)

  if response.status_code == 200:
    # Message JSON
    message = response.json()
    #print("JSON data:", message)

  else:
    print(response)
    
  return (message['id'])


#define function that will add members to Webex Room/Space 
def webex_room_addon(room_title, userid):

  roomid = webex_create_space(room_title)
  email = userid + "@cisco.com"

  headers = {'Authorization': 'Bearer ' + WEBEX_ACCESS_TOKEN,
          'Content-type': 'application/json'}
  post_data = {'roomId': roomid,
            'personEmail': email}

  response = requests.post(ADD_TO_SPACE_URL, json=post_data, headers=headers)

  if response.status_code == 200:
      # Message JSON
      message = response.json()
      #print("JSON data:", message)
  else:
      print(response.status_code)
  
  return response.status_code



#define function that will create a Webex TEAM
def webex_create_team(team_name):
  headers = {
    'Authorization': 'Bearer ' + WEBEX_ACCESS_TOKEN, 
    'Content-type':'application/json'
  }

  post_data = {
    'name' : team_name
  }

  response = requests.post(CREATE_TEAM_URL, json=post_data, headers=headers)

  if response.status_code == 200:
    # Message JSON
    message = response.json()
    #test: print("JSON data:", message)

  else:
    print(response)
    
  return (message['id'])




#define function that will add members to Webex TEAM 
def webex_team_addon(team_name, userid):    

  teamid = webex_create_team(team_name)
  email = userid + "@cisco.com"

  headers = {'Authorization': 'Bearer ' + WEBEX_ACCESS_TOKEN,
          'Content-type': 'application/json'}
  post_data = {'teamId': teamid,
            'personEmail': email}
  
  response = requests.post(ADD_TO_TEAM_URL, json=post_data, headers=headers)

  if response.status_code == 200:
      # Message JSON
      message = response.json()
      #test: print("JSON data:", message)

  else:
      print(response.status_code)
  
  return response

