import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

fc_links = []
pages_NG = []
for i in range (0, 59):
    page = f"https://factcheck.afp.com/list/all/all/all/38558/19?page={i}"
    pages_NG.append(page)

aux = []
for page in pages_NG:
    url = page
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.find_all('div'):
        par_split = str(i).split('\n')
        for index,line in enumerate(par_split):
            if line.startswith('<div class="card">'):
                href = par_split[index+1]
                aux.append(href.split('"',1)[1][1:-2])

    prefix='https://factcheck.afp.com/'

    for link in aux:
        try:
            if link.startswith('doc.afp.com'):
                link = ''.join([prefix,str(link)])
                if link not in fc_links:
                    fc_links.append(link)
        except AttributeError: 
            pass

print(len(fc_links))
#print('\n')
#for i in fc_links:
#    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))