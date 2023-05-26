import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

fc_links = []
urls_NG = []
for i in range (1, 16):
    url = f"https://theinsight.com.ng/category/fact-check/page/{i}/"
    urls_NG.append(url)

for url in urls_NG:
    url = url
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('div', class_='entry-blog-listing clearfix')
    for i in images:
        categories = i.find('span', class_='category-meta-bg')
        if 'fact check' in categories.text.lower() and 'politics' in categories.text.lower():
            title = i.find('div', class_='blog-header')
            #print(title.text)
            link = i.find('h2', class_='entry-post-title').find('a').get('href')
            fc_links.append(link)
            #print(link)

print(len(fc_links))
#print('\n')
#for i in fc_links:
#    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))