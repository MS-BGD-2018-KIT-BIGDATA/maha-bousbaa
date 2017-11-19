#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 21:30:06 2017

@author: maha
"""

import requests
from bs4 import BeautifulSoup
from functools import reduce
import re
import pandas as pd
import unidecode
import json


URL_LIST = 'https://open-medicaments.fr/api/v1/medicaments?query=ibuprofene'
URL_MEDIC= "https://www.open-medicaments.fr/api/v1/medicaments/"

SUFFIX = '.html'


MODEL_LIST =['INTENS','INTENS','LIFE','ZEN']

def getJsonFromUrl(url):
    
    res = requests.get(url)
    return json.loads(res.text)
    

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
    
def getsubUrls(url):
    
    soup = getSoupFromURL(url)
    listsubA = [subLi.find("a") for subLi in 
                soup.find_all('li',itemtype="http://schema.org/Offer")]
    subUrls = [subA['href'] for subA in listsubA ]
    
    print(subUrls)
    return subUrls


def getListLabo():
    
     listMed  = getJsonFromUrl(URL_LIST)
     
     for med in listMed:
          idMed = med['codeCIS']
          MedicamentRow = {'labo': med.get("denomination"),'traitement':"",\
                          'annee':"",'prix':"",'annee':"",\
                          'annee':"",'restriction':""}
          url = URL_MEDIC + str(idMed)
          medicament = getJsonFromUrl(url)
          print(medicament)
 
#df_med = getCarProperties()

#print(" The list of the cars for which the price is superior than Argus rating regardless of Km:\n" ,\
#      df_expensive[['model','annee','kilometrage','prix','cote','proprietaire','phone','region']])