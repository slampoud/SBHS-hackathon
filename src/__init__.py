from flask import Flask, session, Blueprint, Response, send_from_directory, render_template, send_file, url_for, abort, redirect, request, make_response
import FileGenerator
from time import time
import json
from uuid import UUID
import math
import geopy
import geopy.distance

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
    
    re['attachments'] = [{'image_url': "https://food.fnr.sndimg.com/content/dam/images/food/fullset/2013/2/14/0/FNK_breakfast-burrito_s4x3.jpg.rend.hgtvcom.616.462.suffix/1382542427230.jpeg"}]

    re['unfurl_media'] = True
    re['unfurl_links'] = True
    
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
    loc = where_my_burrit_at(burrito['coords'], timePassed)

    size = "500x400"
    center = "" + str(loc[0]) + "," + str(loc[1])
    zoom = str(17)
    apiKey = FileGenerator.API_KEY
    
    params = "size=" + size + "&center=" + center + "&zoom=" + zoom + "&key=" + apiKey + "&markers=|" + center

    re = {}
    re["response_type"] = "in_channel"

    if timePassed > 0:
        re["text"] = "Your burrit left " + str(timePassed) + " seconds ago!" + "https://maps.googleapis.com/maps/api/staticmap?" + params
    else:
        re["text"] = "Your burrit isn't gone yet! It should be outta here in " + str(-timePassed) + " seconds!" + "https://maps.googleapis.com/maps/api/staticmap?" + params
    
    re['attachments'] = [{'image_url': "https://maps.googleapis.com/maps/api/staticmap?" + params}] 

    re['unfurl_media'] = True
    re['unfurl_links'] = True
    print(re) 
    return Response(json.dumps(re), mimetype="application/json")

def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(float(pointA[0]))

    lat2 = math.radians(float(pointB[0]))

    diffLong = math.radians(float(pointB[1]) - float(pointA[1]))

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def where_my_burrit_at(coords, time_passed):
    from geopy.distance import vincenty
    time_passed -= 22
    if time_passed < 0:
        return coords[0]
    distance_left = time_passed * 5
    start = (coords[0][0], coords[0][1])
    finish = (coords[1][0], coords[1][1])
    step_length = vincenty(start, finish).meters
    counter = 1
    while step_length < distance_left and counter + 1 < len(coords):
        distance_left -= step_length
        start = (coords[counter][0], coords[counter][1])
        finish = (coords[counter + 1][0], coords[counter + 1][1])
        step_length = vincenty(start, finish).meters
        counter += 1
    if counter + 1 == len(coords):
        return coords[-1]
    start = geopy.Point(coords[counter - 1][0], coords[counter - 1][1])

    d = geopy.distance.VincentyDistance(meters=distance_left)

    print(counter)
    print(coords)
    print(coords[counter - 1])
    print(coords[counter])

    b = calculate_initial_compass_bearing((coords[counter - 1][0], coords[counter - 1][1]), (coords[counter][0], coords[counter][1]))
    
    v = d.destination(point=start, bearing=b)

    return [v.latitude, v.longitude]

if __name__ == "__main__":
    application.run()
    print("Ready")

