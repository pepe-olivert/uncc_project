import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

# api key with limited access
API_KEY = '22a808fd-7dd1-412a-9f92-5ae5a25d0778'

fc_links = []
urls_NG = []
for i in range (1, 5):
    url = f"https://trustcheck.dailytrust.com/category/fact-check/politics/page/{i}/"
    urls_NG.append(url)

for url in urls_NG:
    url = url
    aux = []
    response = requests.get(url='https://proxy.scrapeops.io/v1/',
                            params={'api_key': API_KEY,
                                    'url': url,
                                    'render_js': True})
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    soup_html = soup.find('div', class_='jeg_cat_content row')
    thumbnails = soup_html.find_all('div', class_='jeg_thumb')
    for i in thumbnails:
        if i.text.strip() == 'Fact Check':
            a_tag = i.find('a')
            link = a_tag.get('href')
            if link.startswith('https://trustcheck.dailytrust.com/') and link not in aux:
                aux.append(link)
    fc_links = fc_links + aux

print(len(fc_links))
print('\n')
for i in fc_links:
    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))

with open("dailytrust_fc_links.txt", "w") as output:
    for url in fc_links:
        output.write(str(url))
        output.write('\n')
