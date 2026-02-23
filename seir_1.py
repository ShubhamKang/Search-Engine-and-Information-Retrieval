import sys
import urllib.request
from bs4 import BeautifulSoup


def fetching_page(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req)
    return page.read()


def printing_title(page):
    if page.title:
        print(page.title.text.strip())
        print("\n")
    else:
        print("Tittle not available for this link")
        print("\n")


def printing_body_text(page):
    if page.body:
        body_content = page.body
        text_parts = body_content.stripped_strings
        body_text = " ".join(text_parts)
        print(body_text)
        print("\n")
    else:
        print("There is not body text for this link")
        print("\n")


def printing_links(page):
    links = page.find_all('a')

    for i in range(len(links)):   
        href = links[i].get('href')
        if href is not None and href != "":
            print(href)
            print("\n")

if len(sys.argv) < 2:
    print("Kindly enter the url in command line")
    sys.exit()
else:
    url = sys.argv[1]

try:
    html_content = fetching_page(url)
    web_page_data = BeautifulSoup(html_content, 'html.parser')

    printing_title(web_page_data)
    printing_body_text(web_page_data)
    printing_links(web_page_data)

except Exception as e:
    print("Error occured while scrapping", e)