import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

fc_links = []
pages_NG = []
for i in range (1, 15):
    page = f"https://www.politifact.com/search/factcheck/?page={i}&q=nigeria/"
    pages_NG.append(page)
    
for page in pages_NG:
    url = page
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    aux = [] # lista auxiliar para reducir el coste temporal de buscar en la lista a continuación
    links = soup.find_all("div", {"class": "c-textgroup__title"})
    prefix = 'https://www.politifact.com'
    for link in links:
        link = str(link).split('href=')[1][1:].split('>')[0][:-1]
        try:
            if link.startswith('/factchecks'):
                link = ''.join([prefix,str(link)])
                if link not in aux:
                    aux.append(link)
        except AttributeError: 
            pass
    fc_links = fc_links + aux

print(len(fc_links))
print('\n')
for i in fc_links:
    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))