import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

fc_links = []

url = 'https://pesacheck.org/english/home'
result = requests.get(url)
src = result.content     
soup = BeautifulSoup(src, 'html.parser')

article_snippet_first = soup.find_all('div', class_='u-lineHeightBase postItem u-marginRight3')

"""
introducir código de selenium para hacer scroll
"""
article_snippets = soup.find_all('div', class_='col u-xs-marginBottom10 u-paddingLeft0 u-paddingRight0 u-paddingTop15 u-marginBottom30')

url_first = str(article_snippet_first[0]).split('href=')[1][1:].split('"')[0]
fc_links.append(url_first)

for snippet in article_snippets:
    url = str(snippet).split('href=')[1].split('"')[1]
    if url not in fc_links:
        fc_links.append(url)

print(len(fc_links))
#print('\n')
#for i in fc_links:
#    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))