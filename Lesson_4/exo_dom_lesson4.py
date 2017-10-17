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


URL_ROOT = 'https://www.leboncoin.fr/voitures/offres/'
URL_PART = '/?q=renault%20zoe&f=p'
URL_PRO =  '?q=renault%20zoe&f=c'

URL_MODEL_ROOT = 'https://www.lacentrale.fr/cote-voitures-renault-zoe-'
URL_COTE_ROOT = 'https://www.lacentrale.fr/cote-auto-renault-zoe'

MODEL_COTES = ['intens+charge+rapide']

REGIONS=['ile_de_france','aquitaine','provence_alpes_cote_d_azur']
ANNEES = ['2012','2013','2014','2015','2016','2017']
SUFFIX = '.html'

#MODEL_LIST2= getModelFromLaCentrale()
MODEL_LIST =['INTENS','INTENS','LIFE','ZEN']

MODEL_COTES2= {'INTENS': 'intens+charge+rapide',
               'INTENSE':'intens+charge+rapide',
               'LIFE': 'life+charge+rapide',
               'ZEN': 'zen+charge+rapide'
               }

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

# The function that extract the properties of Zoe cars from Leboncoin
# this fill the dataframe with car version, car Km, car price, car description, car "cote" and the type of the seller
    
def getCarProperties():
    # Build url based on regions
    URLS_sub1 = [URL_ROOT + region for region in REGIONS]
    
    # Build url based on type of seller ( proprietaire/professionnel)
    URLS  = [url_sub1 + URL_PART for url_sub1 in URLS_sub1] + \
                [url_sub1 + URL_PRO for url_sub1 in URLS_sub1]
    
    columnNames=["version","annee","kilometrage","prix","telephone","proprietaire","phone","description","region"]
       
    carRows = []
    for rootUrl in URLS:
        
        subUrls = getsubUrls(rootUrl)
        
        
        proprietaire = 'Professionnel' if rootUrl.endswith('c') else 'Particulier'
        telephone =''
        version=''
        
        for url in subUrls:
            print(url)
            soupCar = getSoupFromURL("http:"+ url)
            price = soupCar.find_all(class_= "item_price clearfix")[0].\
            find(class_="value").getText().strip()
            price = unidecode.unidecode(price).strip()
            price = int(re.sub(r"\s+","", price.strip('EUR').strip(' '), flags=re.UNICODE))
            re.I
            kilometrage = int("".join(re.findall("([0-9 ]+) ?km", str(soupCar.find_all(class_= "value")),\
                                                 re.I)[0].strip().split()))
            annee =  soupCar.find_all(class_= "value",itemprop="releaseDate")[0].getText().strip()
            
            description = soupCar.find_all(class_= "value",itemprop="description")[0].getText()
            Intense_Found = len(re.findall("(intenses)",str(description).lower()))!=0
            
            carRow = {'version': version,'annee':annee,\
                          'kilometrage':kilometrage,'prix':price,'telephone':telephone,\
                          'proprietaire':proprietaire,'region':"", 'description':description}
            
            carRows.append(carRow)
               
    #print(carRows)
    df = pd.DataFrame(carRows,columns=columnNames)
    df['phone'] = df['description'].apply(extract_phoneNumber)
    df['model']= df['description'].apply(extract_model)
    print('Start Extracting cotes...')
    df['cote'] = df.apply(lambda x: extract_cote(x['annee'], x['model']), axis=1)
    print('Extracting terminated.')
   # df.apply(f, axis=1)
    return(df)


# Function that extract the "cote" from Lacentrale based on the model end the year
    
def extract_cote(x,y):
    
    year= str(x)
    soup = getSoupFromURL(URL_COTE_ROOT + '-'+MODEL_COTES2.get(str(y),'intens+charge+rapide')+'-'+year+SUFFIX)
    cote = int("".join(unidecode.unidecode(soup.find(class_='jsRefinedQuot').getText()).split()))
    
    return cote



# Function that extract the "model" from the description of the car based on the provided model list
def extract_model(x):
     
    for model in MODEL_LIST:
         
          res = re.search( r'(.*) ' + model + ' (.*?) .*',x,re.M|re.I)     
          if res!= None : 
              return model #'INTENS CHARGE RAPIDE'
          
    else: return 
    
#Function that extract the "Telephone number" from the description 
def extract_phoneNumber(x):
      
    res = re.findall(r'((?:\+33\s|0)[1-9](?:[\s.-]*\d{2}){4})',x,re.I)
    
    if len(res)!=0 : 
        return res[0] 
          
    else: return 
# Function that extract the list of car models from Lacentrale
def getModelFromLaCentrale():
    
    modelList = {}
     
    for annee in ANNEES:
        url= URL_MODEL_ROOT+ "-"+ annee +"-" + SUFFIX 
        modelList[annee]=  [model.getText(url) for model in getSoupFromURL(url).\
                      find(id='listing_quot').find_all('h3')]
         
    print(modelList)
    return modelList

# Display the cars with price > argus Cote 
df_car = getCarProperties()
df_expensive = df_car[df_car['prix'] > df_car['cote']]
print(" The list of the cars for which the price is superior than Argus rating regardless of Km:\n" ,\
      df_expensive[['model','annee','kilometrage','prix','cote','proprietaire','phone']])