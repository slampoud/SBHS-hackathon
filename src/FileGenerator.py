import os
import json
import uuid

API_KEY = "AIzaSyD_9P1-rMHgIgFGtltvzk3a-RMLMvFguxs"
#import urllib2
import urllib
import urllib.request as urllib2


def burrito(me, burrito):
    # burrito_place = urllib.quote_plus("Lito's Mexican Restaurant Santa Barbara, CA")
    burrito_place = urllib.parse.quote_plus(burrito)

    where_we_are = urllib.parse.quote_plus(me)

    text = urllib2.urlopen(
        "https://maps.googleapis.com/maps/api/directions/json?origin=" + burrito_place + "&destination=" + where_we_are + "&key=" + API_KEY).read()
    conv_text = text.decode("utf-8")



    organized_data = json.loads(conv_text)

    raw_steps = organized_data["routes"][0]["legs"][0]["steps"]

    steps = []

    steps.append(raw_steps[0]["start_location"])

    for step in raw_steps:
       steps.append(step["end_location"])
    #    print(step)



    lines = []

    for step in steps:
        lines.append(str(step["lat"]) + "," + str(step["lng"]))


    return generateWaypoint(lines)
    


def generateWaypoint(coord_list):
    begin = "QGC WPL 110\n";
    begin += "0\t1\t3\t112\t1\t0\t0\t0\t0\t0\t0\t1\n";
    grab = "\t0\t3\t211\t0\t0\t0\t0\t0\t0\t0\t1\n";
    lift = "\t0\t3\t22\t0\t0\t0\t0\t0.0\t0.0\t20.0\t1\n";

    coords = []
    line_num = 3

    text = begin
    text += str(1) + grab
    text += str(2) + lift

    for coord in coord_list:
        coords.append(coord.split(','))

    for x in range(len(coords)):
        text += str(line_num) + "\t0\t3\t16\t0\t0\t0\t0\t" + coords[x][0] + "\t" + coords[x][1] + "\t7.0\t1\n"
        line_num += 1
        
    drop = "\t0\t3\t211\t1\t0\t0\t0\t0\t0\t0\t1\n"
    text += str(line_num) + drop
    line_num += 1

    for i in range(len(coords) - 2, -1, -1):
        text += str(line_num) + "\t0\t3\t16\t0\t0\t0\t0\t" + coords[x][0] + "\t" + coords[x][1] + "\t7.0\t1\n"
        line_num += 1

    return_to_start = "\t0\t3\t20\t0\t0\t0\t0\t0\t0\t0\t1\n"
    text += str(line_num) + return_to_start
    
    d = urllib.parse.urlencode(dict(text=text))
    response = urllib.request.urlopen("https://file.io", data=d.encode()).read().decode()
    print(response)
    

    ret = {}
    
    return json.loads(response)['link']
