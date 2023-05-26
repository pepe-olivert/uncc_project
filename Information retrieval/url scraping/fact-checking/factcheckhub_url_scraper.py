import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

# api key with limited access
API_KEY = '22a808fd-7dd1-412a-9f92-5ae5a25d0778'

fc_links = []
urls_NG = []
for i in range (1, 4):
    url = f"https://factcheckhub.com/tag/nigerian-fact-checkers-coalition/page/{i}/"
    urls_NG.append(url)
    
for i in range (1, 14):
    url = f"https://factcheckhub.com/category/elections/page/{i}/"
    urls_NG.append(url)

for url in urls_NG:
    url = url
    response = requests.get(url='https://proxy.scrapeops.io/v1/',
                            params={'api_key': API_KEY,
                                    'url': url,
                                    'render_js': True})
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    aux = []
    links_html = soup.find_all('h2', class_='entry-title')
    for i in links_html:
        link_raw = str(i)
        link = link_raw.split('href=')[1][1:].split('"')[0]
        if link not in aux:
            aux.append(link)
    fc_links = fc_links + aux

print(len(fc_links))
print('\n')
for i in fc_links:
    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))

with open("factcheckhub_fc_links.txt", "w") as output:
    output.write(str(fc_links))