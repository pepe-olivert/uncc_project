import requests
from bs4 import BeautifulSoup
import time
from langdetect import detect

def is_english(text):
    try:
        lang = detect(text)
        if lang == 'en':
            return True
        else:
            return False
    except:
        return False

start_time = time.time()

fc_links = []
pages_NG = []
for i in range (1, 5):
    page = f"https://newsverifierafrica.com/category/reports/page/{i}/"
    pages_NG.append(page)
    
for page in pages_NG:
    url = page
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    aux = [] # lista auxiliar para reducir el coste temporal de buscar en la lista a continuación
    links = soup.find_all("h4", {"class": "entry-title title"})
    for link in links:
        link = str(link).split('href=')[1][1:].split('">')[0]
        if is_english(link.split("/")[:-1][-1]) and not link in aux:
            aux.append(link)
    fc_links = fc_links + aux
    
print(len(fc_links))
print('\n')
for i in fc_links:
    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))