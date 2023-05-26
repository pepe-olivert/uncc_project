import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

fc_links = []
urls_NG = []

for i in range (1, 13):
    url = f"https://factcheck.thecable.ng/page/{i}/"
    urls_NG.append(url)

for url in urls_NG:
    url = url
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    aux = []
    links = [a_tag.get('href') for a_tag in soup.find_all('a')]
    for i in links:
        try:
            if i.startswith('https://factcheck.thecable.ng/fact-check-') and i not in aux:
                aux.append(i)
        except:
            continue
    fc_links = fc_links + aux

print(len(fc_links))
print('\n')
for i in fc_links:
    print(i)

print('\n')
print("--- %s seconds ---" % (time.time() - start_time))

with open("thecable_fc_links.txt", "w") as output:
    for url in fc_links:
        output.write(str(url))
        output.write('\n')