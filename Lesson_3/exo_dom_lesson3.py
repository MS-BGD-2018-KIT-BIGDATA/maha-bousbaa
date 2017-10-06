import requests
from bs4 import BeautifulSoup
from functools import reduce

from pygithub3 import Github

URL = 'https://gist.githubusercontent.com/paulmillr/2657075/raw/e522ae257f83cb921d4a63d2e5fde4c6065b2fa2/active.md'

f = open("pwd.txt","r") 

username = "mbousbaa"
password = f.readline().strip()
gh = Github(username, password)


def getMeanStars(username):
    
    star_counts = []
    mean = 0.0
  
    repos = gh.get_user(username).get_repos('all')
    star_counts = [repo.stargazers_count for repo in repos]
    return reduce(lambda x, y: x + y, star_counts) / len(star_counts)
  

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

# classe qui définit les objets user contributeur Git
class Contributor:
  
    def __init__(self,name = "",ranking ="",contributors=0,location="",meanRepoStars=0):
        self.name = name
        self.ranking = ranking
        self.contributors = contributors
        self.location = location
        self.meanRepoStars=0
    
    def printme(self):
        print( "Name: "+ self.name + "; ranking: " + self.ranking + "; Stars: " + str(self.meanRepoStars))
    
  

# fonction qui renvoie la liste des contributeurs
# ( name, ranking, contributions,location)    
        
def getTopContributors(num):
    
    
    topGitHubContributors = []
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



TopContributors =  getTopContributors(10) 

for elem in TopContributors: 
    elem.meanRepoStars = getMeanStars(elem.name)
    elem.printme()

def getMean(contributor):
    return contributor.meanRepoStars

print("######################Sorted list ###############################")
      
topContributorsSorted = sorted(TopContributors, key=getMean)
for elem in topContributorsSorted: elem.printme()

#for elem in sorted(TopContributors , key = getMean):
 #    elem.printme()



        
    
    
    
    
  
       


