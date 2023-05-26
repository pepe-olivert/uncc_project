import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

fc_links = []
pages_NG = []
for i in range (1, 7):
    page = f"https://leadstories.com/cgi-bin/mt/mt-search.fcgi?search=nigeria&IncludeBlogs=1&blog_id=1&limit=10&page={i}/"
    pages_NG.append(page)
    
for page in pages_NG:
    url = page
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    aux = [] # lista auxiliar para reducir el coste temporal de buscar en la lista a continuación
    links = soup.find_all("article", {"class": "mod-default-article"})
    for link in links:
        link = str(link).split('href=')[1][1:].split('itemprop')[0]
        if not link in aux:
            aux.append(link)
    fc_links = fc_links + aux
    
print(len(fc_links))
print('\n')
for i in fc_links:
    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))