#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress
from pprint import pprint
from api_keys import g_key


# In[2]:


file = 'clean_wine_data.csv'


# In[3]:


df = pd.read_csv(file)


# In[4]:


df.head()


# In[ ]:


base_url = "https://maps.googleapis.com/maps/api/geocode/json"
keyword = 'Sweet Cheeks'

params = {"key": g_key,'address':keyword}
response = requests.get(base_url, params=params)
#print(response.url)
places_data = response.json()
places_data
for index, row in df.iterrows():
    target_coordinates = row['winery']
    params['address'] = target_coordinates
        
     #assemble url and make API request
    print(f"Retrieving Results for {row['winery']}.")
    response = requests.get(base_url, params=params)
    
    print(response.url)
    try:
        places_data = response.json()
        #print(places_data)
        results = places_data['results'][0]
        #print(results)
        location = results['geometry']['location']
        #print(location)
        lat = location['lat']
        #print(lat)
        lng = location['lng']
        #print(lng)
        df.loc[index, 'Lat'] = lat
        df.loc[index, 'Lng'] = lng
        
        
    except:
        
        try:
            target_coordinates = row['region_1']
            params['address'] = target_coordinates
        
             #assemble url and make API request
            print(f"Retrieving Results for {row['winery']}.")
            response = requests.get(base_url, params=params)
            places_data = response.json()
            #print(places_data)
            results = places_data['results'][0]
            #print(results)
            location = results['geometry']['location']
            #print(location)
            lat = location['lat']
            #print(lat)
            lng = location['lng']
            #print(lng)
            df.loc[index, 'Lat'] = lat
            df.loc[index, 'Lng'] = lng
            print('used region as search')
            
        except:
                
            print("Missing field/result... skipping.")
            


# In[ ]:


df.head()
df['heat weights'] = df['points']-80


# In[ ]:



#Don't drop, just take the rows where EPS is not NA:

df = df[df['Lat'].notna()]
df = df[df['Lng'].notna()]
df.to_csv('winedf_coord.csv')
df.head()


# In[ ]:


import gmaps
gmaps.configure(api_key=g_key)
locations = df[["Lat", "Lng"]].astype(float)
humidity = df["points"].astype(float)
fig = gmaps.figure()

heat_layer = gmaps.heatmap_layer(locations, weights=humidity, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = 1)

fig.add_layer(heat_layer)
fig


# In[ ]:





# In[ ]:




