
from flask import Flask, session, Blueprint, send_from_directory, render_template, send_file, url_for, abort, redirect, request, make_response
import FileGenerator

from uuid import UUID


burritos = []
burritoCount = 0

print("Setting up...")
application = Flask(__name__)


@application.route("/", methods=["POST", "GET"])
def slack_response():
    
    command =  request.form.get("command")
    
    text = request.form.get("text")
    
    print("Recieved command: ", command, text)
    
    locations = get_your_loc_burrito_loc(text)
    
    burritoInfo = FileGenerator.burrito(locations[0], locations[1])
    
    return burritoInfo['link']
    

#text in the format <your location>@<burrito location>
#Each location can be lat,lng or address
def get_your_loc_burrito_loc(text):
    return text.split("@")


@application.route("/status/", methods=["POST", "GET"])
def get_status():
    command = request.form.get("command")
    text = request.form.get("text")
    

if __name__ == "__main__":
    application.run()
    print("Ready")
