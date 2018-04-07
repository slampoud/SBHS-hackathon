import os

begin = "QGC WPL 110\n";
begin += "0\t1\t3\t112\t1\t0\t0\t0\t0\t0\t0\t1\n";
begin += "1\t0\t3\t211\t0\t0\t0\t0\t0\t0\t0\t1\n";
begin += "2\t0\t3\t22\t0\t0\t0\t0\t0.0\t0.0\t20.0\t1\n";

file =  open("WaypointTest.txt","r")
output = open("waypoints.txt","w")
coords = []
line_num = 3

output.write(begin)


for line in file:
    coords.append(line.strip().split(','))

file.close()

for x in range(len(coords)):
    output.write(str(line_num) + "\t0\t3\t16\t0\t0\t0\t0\t" + coords[x][0] + "\t" + coords[x][1] + "\t7.0\t1\n")
    line_num += 1

output.write(str(line_num) + "\t0\t3\t21\t0\t0\t0\t0\t" + coords[len(coords)-1][0] +"\t" + coords[len(coords)-1][1] + "\t0\t1\n")
line_num += 1
output.write(str(line_num) + "\t0\t3\t211\t1\t0\t0\t0\t0\t0\t0\t1\n")

output.close()

os.rename("waypoints.txt","waypoints.waypoints")    

