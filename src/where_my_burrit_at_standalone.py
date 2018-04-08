def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

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
    start = geopy.Point(coords[counter - 1][0], coords[counter - 1][1])

    d = geopy.distance.VincentyDistance(meters=distance_left)

    b = calculate_initial_compass_bearing((coords[counter - 1][0], coords[counter - 1][1]), (coords[counter][0], coords[counter][1]))
    
    v = d.destination(point=start, bearing=b)

    return [v.latitude, v.longitude]
