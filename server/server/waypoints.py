from uuid import uuid4

"""
Locations is an array of [lat, lng] numbers

Creates a random UUID

Creates a waypoint file going along the locations

Writes file to /WaypointFiles/uuid

Returns uuid

"""
def make_waypoint_file(locations):
    uuid = uuid4()
    
    with open("WaypointFiles/"+str(uuid), "w") as f:
        for location in locations:
            f.write(str(location))


    return str(uuid)
