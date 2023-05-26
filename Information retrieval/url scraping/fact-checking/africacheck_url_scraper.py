import requests
from bs4 import BeautifulSoup
from langdetect import detect
import time

def is_english(text):
    try:
        lang = detect(text)
        if lang == 'en':
            return True
        else:
            return False
    except:
        return False

start_time = time.time()

fc_links = []
urls_NG = []
for i in range (0, 45):
    url = f"https://africacheck.org/fact-checks?field_country_value=NG&sort_bef_combine=created_DESC&page={i}"
    urls_NG.append(url)

for url in urls_NG:
    url = url
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    aux = [] # lista auxiliar para reducir el coste temporal de buscar en la lista a continuación
    links = [a_tag.get('href') for a_tag in soup.find_all('a')]
    prefix='https://africacheck.org/'
    for link in links:
        try:
            if link.startswith('/fact-checks'):
                link = ''.join([prefix,str(link)])
                if link not in aux and len(link)>65 and not '&page=' in link and is_english(link.split("/")[-1]):
                    aux.append(link)
        except AttributeError: 
            pass
    fc_links = fc_links + aux

print(len(fc_links))
print('\n')
for i in fc_links:
    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))

with open("file.txt", "w") as output:
    output.write(str(fc_links))