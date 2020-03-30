import requests 
from bs4 import BeautifulSoup
class City():
    def __init__(self, name, id):
        self.name = name
        self.id = id
    def __str__(self):
        return self.name.split('%')[0]
    def getLinks(self):
        url = 'http://www.classifiedads.com/search.php?'
        links = []
        for x in range(1,70):
            r = requests.get(url, params = {'cid':'299','lid':self.id,'lname':self.name,'page':x})
            content = r.text
            soup = BeautifulSoup(content, 'html.parser')
            for div in soup.findAll('div', class_='resultitem'):
                link = div.find('a')['href']
                if link not in links:
                    links.append(link)
                    print('New link from', str(self), link)
        return links