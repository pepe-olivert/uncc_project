import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

fc_links = []
url = 'https://punchng.com/topics/2023-elections/#!'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')
links = [a_tag.get('href') for a_tag in soup.find_all('a')]
for link in links:
    if link not in fc_links and link.startswith('https://punchng.com/') and not link.startswith('https://punchng.com/topics') and len(link)>45:
        fc_links.append(link)
        #print(link)

print(len(fc_links))

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))