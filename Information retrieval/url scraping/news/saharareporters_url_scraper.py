import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

news_links = []
pages_NG = []
for i in range (0, 44):
    page = f"https://saharareporters.com/articles?f[0]=article_topics%3A33288&page={i}/"
    pages_NG.append(page)
    
for page in pages_NG:
    url = page
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    aux = [] # lista auxiliar para reducir el coste temporal de buscar en la lista a continuación
    prefix = 'https://saharareporters.com'
    links = soup.find_all("div", {"class": "card-content"})
    for link in links:
        if 'election' in link.text.lower(): # we get only those with tag 'Elections'
            for i in link.find_all("h2", {"class": "title is-3"}):
                suffix = str(i).split('href=')[1].split('"')[1]
                link = ''.join([prefix,str(suffix)])
                if link not in aux:
                    aux.append(link)
    news_links = news_links + aux

for i in news_links:
    print(i)
print('\n')
print(len(news_links))
print('\n')
print("--- %s seconds ---" % (time.time() - start_time))