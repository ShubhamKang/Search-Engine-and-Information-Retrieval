import sys
import urllib.request
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Kindly give the url in command line")
    sys.exit()

url = sys.argv[1]

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req)
    html_content = page.read()

    web_page_data = BeautifulSoup(html_content, 'html.parser')

    if web_page_data.title:
        print(web_page_data.title.text.strip())
    else:
        print("No Title Found")


    print("\n")


    if web_page_data.body:
        body_content = web_page_data.body
        text_parts = body_content.stripped_strings
        body_text = " ".join(text_parts)
        print(body_text)
    else:
        print("No Body Found")

    print("\n")



    links = web_page_data.find_all('a')
    
    for i in range(len(links)):
        href = links[i].get('href')
        if href is not None and href != "":
            print(href)
            print("\n")
        
except Exception as e:
    print("An error occurred:", e)