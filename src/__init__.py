from flask import Flask, session, Blueprint, Response, send_from_directory, render_template, send_file, url_for, abort, redirect, request, make_response
import FileGenerator
from time import time
import json
from uuid import UUID


burritos = []
burritoCount = 0

print("Setting up...")
application = Flask(__name__)


@application.route("/", methods=["POST", "GET"])
def slack_response():
    
    global burritoCount
    global burritos

    command =  request.form.get("command") 
    text = request.form.get("text")
    burrito = {}
    burrito['id'] = burritoCount
    burrito['start_time'] = time() + 60
    
    print("Recieved command: ", command, text)
    
    locations = get_your_loc_burrito_loc(text)
    
    burritoInfo = FileGenerator.burrito(locations[0], locations[1])
    
    burrito['coords'] = burritoInfo['coords']
   
    burritos.append(burrito)
    burritoCount += 1

    re = {}

    re["response_type"] = "in_channel"
   
    re['text'] = "Burrit numbo " + str(burrito['id']) + " will be leaving " + locations[1] + " in 60 seconds. It will arrive at " + locations[0] + " Flight Waypoint file: " + burritoInfo['link']
    
    return Response(json.dumps(re), mimetype="application/json")

#text in the format <your location>@<burrito location>
#Each location can be lat,lng or address
def get_your_loc_burrito_loc(text):
    return text.split("@")


@application.route("/status", methods=["POST", "GET"])
def get_status():

    global burritos

    command = request.form.get("command")
    text = request.form.get("text")
    
    print("Recieved command: ", command, text)

    burrito = burritos[int(text)]
    timePassed = time() - burrito['start_time']
    #loc = where_my_burrito_at(timePassed, burrito['coords'])

    #size = "500x400"
    #center = "" + str(loc[0]) + "," + str(loc[1])
    #zoom = 15

    re = {}
    re["response_type"] = "in_channel"

    if timePassed > 0:
        re["text"] = "Your burrit left " + str(timePassed) + " seconds ago!"
    else:
        re["text"] = "Your burrit isn't gone yet! It should be outta here in " + str(-timePassed) + " seconds!"
    
    return Response(json.dumps(re), mimetype="application/json")

if __name__ == "__main__":
    application.run()
    print("Ready")
