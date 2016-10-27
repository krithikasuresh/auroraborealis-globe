
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
import requests
import json
import re


# In[2]:

r = requests.get("http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt")


# In[3]:

soup = BeautifulSoup(r.text, 'lxml')


# In[4]:

text = soup.find('p').text


# In[5]:

regex = r" +"
lines = text.split('\n')


# In[6]:

i = 0
while True:
    if lines[i].strip()[0] != "#":
        break
    i += 1
    


# In[7]:

data_lines = lines[i:-1]
data = list(map(lambda x: re.split(regex, x)[1:], data_lines))

print len(data)


# In[8]:

#checks if there are any sets that aren't 1024 values long (so shouldn't show anything)
for i in data:
    if len(i) != 1024:
        print(i)
        print(len(i))
        break


# In[9]:

#latitude inc, longitude inc, points array to hold data
lat_inc = 0.3515625
long_inc = 0.32846715
points = []


# In[10]:

for i, group in enumerate(data):
    for j in group:
        points.append((-90 + lat_inc*i, 0, j))
print points[2:5]
print len(points)/1024


# In[11]:

mult = 0
#hold the correctly formatted array of data 
new_points = []
for i, p in enumerate(points):
    if i and i % 1024 == 0:
        mult = 0
    new_points.append([p[0], -180 + long_inc*mult, p[2]])
    mult += 1

print new_points[1:10]
print len(new_points)/1024
print new_points[1][2]


# In[12]:

zeros = 0
nothing = 0
count = 0
clean_data = []

for i, p in enumerate(new_points):
    if i and i % 1024 == 0:
        mult = 0
    if float(p[2]) > 5:
        clean_data.append([int(p[0]), int(p[1]), float(p[2])])
    else:
        zeros += 1
    mult += 1


#for i in range(len(new_points)):
 #   if float(new_points[i][2]) > 0:
#      if (int(new_points[i][1]) != int(new_points[i+1][1])):
   #         if i % 2 == 0:
    #            clean_data = clean_data + [int(new_points[i][0]), int(new_points[i][1]), (float(new_points[i][2])/100)]
    #else:
     #   zeros += 1
        #print new_points[i][2]

print zeros
#print nothing
#print nothing + zeros
print ((len(clean_data) + zeros))/1024
#print len(clean_data) + zeros
print len(clean_data)


# In[18]:

cleaner_data = []
for i in range(len(clean_data)):
    if i % 5 == 0:
        cleaner_data = cleaner_data + [clean_data[i][0], clean_data[i][1], (clean_data[i][2]/100)]

final_data = [["Aurora Borealis View Prediction", cleaner_data]]

print len(cleaner_data)
print len(final_data)


# In[17]:

with open('cleanAuroraData.json', 'w') as outfile:
    json.dump(final_data, outfile)


# In[ ]:




# In[ ]:



