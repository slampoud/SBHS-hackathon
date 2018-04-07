API_KEY = "AIzaSyD_9P1-rMHgIgFGtltvzk3a-RMLMvFguxs"

import urllib2
import urllib


#import geocoder

our_location = { "lat": 34.429769, "lng" :-119.694592}

#geocoder.ip("me").latlng
def burrito(me, burrito):

    #burrito_place = urllib.quote_plus("Lito's Mexican Restaurant Santa Barbara, CA")
    burrito_place = urllib.quote_plus(burrito)

    where_we_are = urllib.quote_plus(me)

    text = urllib2.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin=" + burrito_place + "&destination=" + where_we_are + "&key=" + API_KEY).read()

    print(text)

    import json

    organized_data = json.loads(text)


    raw_steps = organized_data["routes"][0]["legs"][0]["steps"]

    steps = []

    steps.append(raw_steps[0]["start_location"])

    #for step in raw_steps:
    #   steps.append(step["end_location"])
    #    print(step)

    steps.append(our_location)


    lines = []

    for step in steps:
        lines.append(str(step["lat"]) + "," + str(step["lng"]))



    with open("output", "w") as out:
        out.writelines(lines)


    return lines



print(burrito("Santa Barbara High School Santa Barbara, CA","Lito's Mexican Restaurant Santa Barbara, CA"))
