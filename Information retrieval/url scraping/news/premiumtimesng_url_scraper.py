import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

news_links = []
url = 'https://www.premiumtimesng.com/2023-elections-presidential'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all("h3", {"class": "jeg_post_title"})
for link in links:
    link = str(link).split('href=')[1].split('>')[0][1:-1]
    if link not in news_links:
        news_links.append(link)

for i in news_links:
    print(i)
print('\n')
print(len(news_links))

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))