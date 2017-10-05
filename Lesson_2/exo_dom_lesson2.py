import requests
from bs4 import BeautifulSoup
import unidecode


URL = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
share_class_pp = "c-sharebox__stats-number"

YEARS = ['2010', '2011', '2012', '2013', '2014', '2015']
INDEX_CIT=[1,4,10,13]
INDEX_EUR=[0,3,9,12]
LABELS=["TOTAL A"," TOTAL B","TOTAL C","TOTAL D"]

# getSoupObjectForYear retourne l'objet BeautifulSoup object associé aux resultat
# des comptes de Paris de l'année passée en paramètre"""

def getSoupObjectForYear(year='2010'):

    url = URL + str(year)
    return getSoupFromURL(url, 'get')


# getSoupFromURL retourne l'objet BeautifulSoup object associé a l'url donnée
# en paramètre en appliquant la methode 'get ou 'post'

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




def extractFigure(row):
    
    return(int("".join(unidecode.unidecode(row).strip().split())))

def processDataYear(datalist):
   
    figures_CIT=[extractFigure(datalist[i].get_text()) for i in INDEX_CIT]
    figures_EUR=[extractFigure(datalist[i].get_text()) for i in INDEX_EUR]
    return zip(LABELS,figures_CIT,figures_EUR)
    
def getDataFromParisAccounts():
    
    
    resultDataList = {x: "" for x in YEARS}
    for year in YEARS:
        dataFromUrl = getSoupObjectForYear(URL + year).select(".montantpetit.G")
        resultDataList[year]= list(processDataYear(dataFromUrl))
        
    return resultDataList

dataresult = getDataFromParisAccounts();
for elem in dataresult:
    print(elem)
    print(dataresult.get(elem))

