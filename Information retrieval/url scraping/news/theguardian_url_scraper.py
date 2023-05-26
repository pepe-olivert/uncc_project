import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

url = 'https://guardian.ng/tag/nigeria-decides-2023/'
news,opinion = [],[]
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all("div", {"class": "item design-article"})
for link in links:
    url = str(link).split('href=')[1].split('>')[0][1:-1]
    if 'category' in url:
        pass
    elif 'opinion' in url: opinion.append(url)
    else: news.append(url)
print(opinion)
print(news)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))