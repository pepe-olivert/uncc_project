import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

news_links = []
pages_NG = []
for i in range (0, 31):
    page = f"https://thenationonlineng.net/politics/page/{i}//"
    pages_NG.append(page)

API_KEY = 'e893b922-5982-42bb-aa4d-3f0f3abd84de'
for page in pages_NG:
    url = page
    response = requests.get(url='https://proxy.scrapeops.io/v1/', 
                        params={ 
                            'api_key': API_KEY, 
                            'url': url, 
                            'render_js': True
                        } 
                       )
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    aux = []
    for a_tag in soup.find_all("a"):
        href = a_tag.get('href')
        if not href in aux and href.startswith('https://thenationonlineng.net') and len(href)>55:
            aux.append(href)
    news_links = news_links + aux
    
for i in news_links:
    print(i)
print('\n')
print(len(news_links))

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))