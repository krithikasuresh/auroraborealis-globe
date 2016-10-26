
# coding: utf-8

# In[4]:

import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import re


# In[5]:

r = requests.get("http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt")


# In[6]:

soup = BeautifulSoup(r.text, 'lxml')


# In[7]:

text = soup.find('p').text


# In[8]:

regex = r" +"
lines = text.split('\n')


# In[9]:

i = 0
while True:
    if lines[i].strip()[0] != "#":
        break
    i += 1
    


# In[10]:

data_lines = lines[i:-1]
data = list(map(lambda x: re.split(regex, x)[1:], data_lines))

print len(data)


# In[11]:

#checks if there are any sets that aren't 1024 values long (so shouldn't show anything)
for i in data:
    if len(i) != 1024:
        print(i)
        print(len(i))
        break


# In[12]:

#latitude inc, longitude inc, points array to hold data
lat_inc = 0.3515625
long_inc = 0.32846715
points = []


# In[13]:

for i, group in enumerate(data):
    for j in group:
        points.append((-90 + lat_inc*i, 0, j))
print points[314]


# In[14]:

mult = 0
#hold the correctly formatted array of data 
new_points = []
for i, p in enumerate(points):
    if i and i % 1024 == 0:
        mult = 0
    new_points.append([p[0], -180 + long_inc*mult, p[2]])
    mult += 1

print new_points[1]
print len(new_points)
print new_points[1][2]


# In[16]:

zeros = 0
nothing = 0
clean_data = []

for i in range(524288):
    if i % 3 == 0: 
        if float(new_points[i][2]) >  10:
            if int(new_points[i][1] != int(new_points[i+1][1])):
                if int(new_points[i][0] != int(new_points[i+1][0])):
                    clean_data = clean_data + [int(new_points[i][0]), int(new_points[i][1]), (float(new_points[i][2])/100)]
        else:
            zeros += 1

#print zeros
#print nothing
#print nothing + zeros
print len(clean_data)
#print len(clean_data) + zeros
#print clean_data


# In[15]:

final_data = [["Aurora Borealis View Prediction", clean_data]]


# In[16]:

with open('cleanAuroraData.json', 'w') as outfile:
    json.dump(final_data, outfile)

