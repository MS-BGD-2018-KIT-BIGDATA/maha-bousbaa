import requests
from bs4 import BeautifulSoup


url = 'https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-acer.html#_his_"

def getSoupFromURL(url, method='get', data={}):

  if method == 'get':
    res = requests.get(url)
  elif method == 'post':
    res = requests.post(url, data=data)
  else:
    return None

  if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup
  else:
    return None

def getAmounts(url):
  soup = getSoupFromURL(url)
  if soup:
     return  soup
 
      

  else:
    0


