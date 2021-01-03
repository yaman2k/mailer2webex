#import needed modules/objects
import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
from mailer_request import mailer_members
from webex_request import webex_room_addon, webex_team_addon
from multiprocessing import Process


#ability to find .env file
load_dotenv()

#intialize Flask app
app = Flask(__name__)

#Read MONGODB_URI and connect to MongoDB called mailer
client = MongoClient(os.environ.get("MONGODB_URI"))
app.db = client.mailer


# Route all HTTP requests using this decorator
@app.route("/", methods=["GET","POST"])
def index():
        #initialize variables
        formatted_date=""
        mailer_feedback="none"
        webex_feedback = "none"
        entry_title = "none"
        user_count = "N/A"
        mailer_status_code = ""

        #Collect user submitted entries from web GUI and insert into MongoDB
        if request.method == "POST":
                entry_userid = request.form.get("userid")
                entry_title = request.form.get("title")
                entry_mailer = request.form.get("mailer")
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                
                #send request over to mailer function to retrieve members
                try:
                    mailer_status_code, user_data, user_count = mailer_members(entry_mailer)
                except:
                    webex_feedback = "warning"

                #send feedback to web GUI that operation is successful
                if mailer_status_code==200:
                    mailer_feedback= "success"
                    for user in user_data['members']:
                        a= Process(target=webex_room_addon,args=(entry_title,user))
                        a.start()
                    webex_feedback = "success"
                else:
                    mailer_feedback="error"

                
                #save records to database
                try:
                    app.db.submissions.insert({"userid":entry_userid,"mailer":entry_mailer,"space title": entry_title,"date":formatted_date})
                except:
                    webex_feedback = "warning"




        return render_template("index.html",formatted_date=formatted_date,mailer_feedback=mailer_feedback,webex_feedback=webex_feedback,title=entry_title,user_count=user_count)

