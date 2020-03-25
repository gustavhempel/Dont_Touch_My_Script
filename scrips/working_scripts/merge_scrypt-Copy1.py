#!/usr/bin/env python
# coding: utf-8



# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress
from pprint import pprint
from api_keys import g_key




file = 'res/1_2.csv'
df = pd.read_csv(file)

file1 = 'res/3coord.csv'
df1 = pd.read_csv(file1)

file2 = 'res/4coord.csv'
df2 = pd.read_csv(file2)

file4 = 'res/5coord.csv'
df4 = pd.read_csv(file4)

file5 = 'res/6coord.csv'
df5 = pd.read_csv(file5)

file6 = 'res/7coord.csv'
df6 = pd.read_csv(file6)

file7 = 'res/8coord.csv'
df7 = pd.read_csv(file7)

file8 = 'res/9coord.csv'
df8 = pd.read_csv(file8)

file9 = 'res/10coord.csv'
df9 = pd.read_csv(file9)


new_df = pd.concat([df,df1,df2,df4,df5,df6,df7,df8,df9], join='outer')
new_df.head()
new_df = new_df.drop(columns=['Unnamed: 0','Unnamed: 0.1','Unnamed: 0.1.1','Unnamed: 0.1.1.1','region_2'])
new_df['year'] = new_df['title']

a = new_df['title'].count()

new_df['year'] = new_df['year'].str.extract('(\d+)')

new_df.to_csv('winedf2')


for index, row in new_df.iterrows():
    latitute = row['Lat']
    logintitude = row['Lng']
    print(f"Retrieving Results for {row['winery']}.")
    base_url =f'http://climateapi.scottpinkelman.com/api/v1/location/{latitute}/{logintitude}'
    response = requests.get(base_url)
    print(response.url)
    
    try:
        places_data = response.json()
        #print(places_data)
        results = places_data['return_values'][0]
        #print(results)
        zone = results['koppen_geiger_zone']
        zone_desc = results['zone_description']
        #print(zone)
        #print(zone_desc)
        new_df.loc[index, 'Climate Zone'] = zone
        new_df.loc[index, 'Climate Zone Desc.'] = zone_desc
        print(a)
        a= a-1
        
        
    except:
        print("Could not identify the Climate Zone.")


new_df.to_csv('winedf_loc_cz2.csv')







