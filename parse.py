import csv
import json
lines = csv.reader(open("fireball.csv", "rb"))
data = []  

for lat, lon, val in lines:
    if "S" in lat:
        lat = lat.replace("S", "")
        lat = -float(lat)
    else:
        lat = lat.replace("N", "")
    
    if "W" in lon:
        lon = lon.replace("W", "")
        lon = -float(lon)
    else:
        lon = lon.replace("E", "")
    
    data = data + [lat, lon, val]

output = [
    ["Fireballs", data]
]

with open('fireballdata.json', 'w') as outfile:
    json.dump(output, outfile)
print json.dumps(output)

#min max, difference 