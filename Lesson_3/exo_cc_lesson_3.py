#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:33:53 2017

@author: maha
"""



import requests
import json
from bs4 import BeautifulSoup
import functools
import time
from multiprocessing import Pool
import pandas as pd

url ='http://www.toutes-les-villes.com/villes-population.html'

MYKEY= "AIzaSyBrD4WYo3A--zMdL9awoPVPK2zl_zqtt2I"
def get_soup_from_url(url):
    
    page=requests.get(url);
    if (page.status_code == 200):
        return BeautifulSoup(page.content,'html.parser')
    else:
        return None
 

def get_distance(city1,city2):
    
    url= "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + city1 +"&destinations=" + city2+ '&key=AIzaSyBrD4WYo3A--zMdL9awoPVPK2zl_zqtt2I'    
      
  
    page = requests.get(url)
    
   
    json_obj = json.loads(page.content)
    
    
    distance = json_obj['rows'][0]['elements'][0]['distance']["value"]
    return distance

cities_distance  = [{'Paris': 'Lyon', 'Jan': 150, 'Feb': 200, 'Mar': 140},
         {'account': 'Alpha Co',  'Jan': 200, 'Feb': 210, 'Mar': 215},
         {'account': 'Blue Inc',  'Jan': 50,  'Feb': 90,  'Mar': 95 }]
df = pd.DataFrame(cities_distance)

def getSoupFromURL(url, method='get', data={}):

    try:
        if method == 'get':
            res = requests.get(url)
        elif method == 'post':
            res = requests.post(url, data=data)
        else:
            return None

        if(res.status_code != 200):
            print(
                "status code is invalid [%s] for url: %s", res.status_code, url)
            return None
        if res.status_code == 200:
            return BeautifulSoup(res.content, 'html.parser')
        else:
            return None
    except requests.exceptions.ConnectionError as e:
        print("HTTP connexion error or Invalid URL: %s", url)
        return None
 
    
def getTopCities(num):
     
    topcities = []
    soup = getSoupFromURL(URL).select("tbody > tr")[0:num]
    i=0
 
    for i in range(0,num):
        
        ranking = soup[i].find("th").get_text()
        subsoup_td = soup[i].select("td")
        name = subsoup_td[0].find("a").get_text()
        contributions = int(subsoup_td[1].get_text() )
        location = subsoup_td[2].get_text()
        topGitHubContributors.append(Contributor(name,ranking,contributions,location))
        i += 1
        
    return topGitHubContributors 


