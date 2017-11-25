#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 21:30:06 2017

@author: maha
"""

import requests
from functools import reduce
import re
import pandas as pd
import unidecode
import glob

#Import des données


# fichier à charger

files = ["depa2012","depa2013"]
path = "/path/fichiers"

#comment faire pour 
# glob.glob('path/*.s) retourne liste de fichier avec exstension *.xls

# pd.concat (concatène 2x df, Attention aux index!)
#df['colonne'].upper().str.contains
#df2 = df[~a]  a est une df boolean  ~est not ~@
#DF2['colonne']=DF2['colonne'].str.extract('((\dAB]+)-(.*)'])) -> df.str.split('-',1) renvoie une copie
#dropna ( utiliser l'attribut subset pour ) ex. dropna(subset=['col1','col2'#])])