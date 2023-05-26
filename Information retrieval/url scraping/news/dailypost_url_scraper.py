import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

news_links = []
url = 'https://dailypost.ng/politics/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
links = [a_tag.get('href') for a_tag in soup.find_all('a')]
for i in links:
    if i.startswith('https://dailypost.ng/20'):
        news_links.append(i)

for i in news_links:
    print(i)
print('\n')
print(len(news_links))

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))