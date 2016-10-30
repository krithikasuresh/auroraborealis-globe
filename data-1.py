
# coding: utf-8

# In[210]:

from bs4 import BeautifulSoup
import requests
import json
import re
import time
starttime=time.time()
while True:
    print "tick"
    # In[211]:

    r = requests.get("http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt")


    # In[212]:

    soup = BeautifulSoup(r.text, 'lxml')


    # In[213]:

    text = soup.find('p').text


    # In[214]:

    regex = r" +"
    lines = text.split('\n')


    # In[215]:

    i = 0
    while True:
        if lines[i].strip()[0] != "#":
            break
        i += 1


    # In[216]:

    data_lines = lines[i:-1]
    data = list(map(lambda x: re.split(regex, x)[1:], data_lines))


    # In[217]:

    #latitude inc, longitude inc, points array to hold data
    lat_inc = 0.3515625
    long_inc = 0.3515625
    points = []


    # In[218]:

    i = 0
    for i, group in enumerate(data):
        for j in group:
            points.append([-90 + lat_inc*i, 0, j])
    print points[523270]
    print len(points)


    # In[219]:

    mult = 0
    #hold the correctly formatted array of data 
    new_points = []
    for i, p in enumerate(points):
        if i % 1024 == 0:
            mult = 0
        new_points.append([p[0], -180 + long_inc*mult, p[2]])
        mult += 1

    #print new_points[52480:]
    print mult
    print len(new_points)


    # In[220]:

    zeros = 0
    clean_data = []
    new_data = []
    mult = 0

    for i, p in enumerate(new_points):
        if i % 1024 == 0:
            mult = 0
        if float(p[2]) > 5:
            new_data.append([int(p[0]), int(p[1]), (float(p[2])/100)])
        else:
            zeros += 1
        mult += 1

    for i, p in enumerate(new_data):
        if i and i % 1024 == 0:
            mult = 0
        if mult % 5 == 0:
            clean_data.append([p[0], p[1], p[2]])
        mult += 1

    print len(clean_data)
    print len(new_data)


    # In[221]:

    cleaner_data = []
    for i in range(len(clean_data)):
        cleaner_data = cleaner_data + [clean_data[i][0], clean_data[i][1], clean_data[i][2]]

    final_data = [["Aurora Borealis View Prediction", cleaner_data]]

    print len(cleaner_data)
    print len(final_data)


    # In[171]:

    with open('cleanAuroraData.json', 'w') as outfile:
        json.dump(final_data, outfile)
        
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))