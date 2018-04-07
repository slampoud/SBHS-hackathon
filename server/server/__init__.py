
from flask import Flask, session, Blueprint, send_from_directory, render_template, send_file, url_for, abort, redirect, request, make_response
import routing

from uuid import UUID


print("Setting up...")
application = Flask(__name__)


@application.route("/", methods=["POST", "GET"])
def slack_response():
    
    command =  request.form.get("command")
    
    text = request.form.get("text")

    locations = get_your_loc_burrito_loc(text)
    
    uuid = routing.write_file_between(locations)
    
    return "File available at: fortnightdesigns.com/file/" + uuid
    

#text in the format <your location>@<burrito location>
#Each location can be lat,lng or address
def get_your_loc_burrito_loc(text):
    return text.split("@")


@application.route("/file/<i>")
def return_file(i):
    try:
        print(i)
        uuid = UUID(hex=i, version=4)
        print(uuid)
        return send_from_directory("WaypointFiles", str(uuid))
    except Exception as e:
        print(e)
        return "Incorrect UUID"


if __name__ == "__main__":
    application.run()
    print("Ready")
