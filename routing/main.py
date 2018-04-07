API_KEY = "AIzaSyD_9P1-rMHgIgFGtltvzk3a-RMLMvFguxs"

import urllib2

#import geocoder

our_location = { "lat": 34.429769, "lng" :-119.694592}

#geocoder.ip("me").latlng

burrito_place = "821+N+Milpas+ST+Santa+Barbara,+CA"

where_we_are = str(our_location["lat"]) + "," + str(our_location["lng"])


text = urllib2.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin=" + burrito_place + "&destination=" + where_we_are + "&key=" + API_KEY).read()

print(text)

import json

organized_data = json.loads(text)


raw_steps = organized_data["routes"][0]["legs"][0]["steps"]

steps = []

steps.append(raw_steps[0]["start_location"])

for step in raw_steps:
    steps.append(step["end_location"])
    print(step)

steps.append(our_location)


lines = []

for step in steps:
    lines.append(str(step["lat"]) + "," + str(step["lng"]) + "\n")



with open("output", "w") as out:
    out.writelines(lines)
