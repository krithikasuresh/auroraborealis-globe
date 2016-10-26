import pandas as pd
from bs4 import BeautifulSoup
import requests
from functools import reduce
import json


r = requests.get("http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt")
soup = BeautifulSoup(r.text)

text = soup.find('p').text
lines = text.split('\n')

i = 0
while True:
    if lines[i].strip()[0] != "#":
        break
    i += 1

data_lines = lines[i:-1]
data = list(map(lambda x: x.split("   ")[1:], data_lines))


lat_inc = 0.3515625
points = []


for i, group in enumerate(data):
    for j in group:
        points.append((-90 + lat_inc*i, 0, j))


long_inc = 0.32846715

mult = 0
new_points = []
for i, p in enumerate(points):
    if i and i % 512 == 0:
        mult += 1
    new_points.append([p[0], -180 + long_inc*mult, p[2]])

new_points = [item for sublist in new_points for item in sublist]

with open('auroraborealisdata.json', 'w') as outfile:
    json.dump(new_points, outfile)
print json.dumps(new_points)





