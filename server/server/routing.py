"""
Start - string representing either lat,lng or address
End - string respresenting  either lat,lng or address

Returns array of [float, float] pairs representing [lat, lng], a list of locations that form a path from start to end
"""
def get_lat_lngs_between(start, end):
    
    return [[start, start], [end, end]]



