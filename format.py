# In[222]:

from bs4 import BeautifulSoup
import requests
import json
import re
import time

#timer to update cleanAuroraData.json file every hour
starttime=time.time()
while True:
    # In[223]:
    
    #get the data
    r = requests.get("http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt")


    # In[224]:
    #get the text
    soup = BeautifulSoup(r.text, 'lxml')


    # In[225]:
    #get from p tag
    text = soup.find('p').text


    # In[226]:
    #split lines and define regex
    regex = r" +"
    lines = text.split('\n')


    # In[227]:
    
    #get rid non data lines
    i = 0
    while True:
        if lines[i].strip()[0] != "#":
            break
        i += 1


    # In[228]:
    #split all the data values with regex
    data_lines = lines[i:-1]
    data = list(map(lambda x: re.split(regex, x)[1:], data_lines))


    # In[229]:

    #latitude inc, longitude inc, points array to hold data
    lat_inc = 0.3515625
    long_inc = 0.3515625
    points = []


    # In[230]:

    i = 0
    for i, group in enumerate(data):
        for j in group:
            points.append([-90 + lat_inc*i, 0, j])


    # In[231]:

    mult = 0
    #hold the correctly formatted array of data 
    new_points = []
    for i, p in enumerate(points):
        if i % 1024 == 0:
            mult = 0
        new_points.append([p[0], -180 + long_inc*mult, p[2]])
        mult += 1


    # In[232]:

    clean_data = []
    new_data = []
    mult = 0
    
    #clean out the smaller values of data and show every fourth value in order to reduce the amount of values shown for improved load time
    for i, p in enumerate(new_points):
        if i % 1024 == 0:
            mult = 0
        if float(p[2]) > 10:
            new_data.append([int(p[0]), int(p[1]), (float(p[2])/100)])
        mult += 1

    for i, p in enumerate(new_data):
        if i and i % 1024 == 0:
            mult = 0
        if mult % 4 == 0:
            clean_data.append([p[0], p[1], p[2]])
        mult += 1


    # In[233]:
    #completely finish formatting json
    cleaner_data = []
    for i in range(len(clean_data)):
        cleaner_data = cleaner_data + [clean_data[i][0], clean_data[i][1], clean_data[i][2]]

    final_data = [["Aurora Borealis View Prediction", cleaner_data]]


    # In[171]:

    with open('cleanAuroraData.json', 'w') as outfile:
        json.dump(final_data, outfile)
        
    time.sleep(3600.0 - ((time.time() - starttime) % 3600.0))

