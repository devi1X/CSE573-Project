import requests
from bs4 import BeautifulSoup
import csv
import lxml
import pandas as pd
import re

url_list = []
url_part1 = 'https://patient.info/forums/discuss/browse/coronavirus-covid-19--4541?page='
url_part2 = '#group-discussions'

url = 'https://patient.info/forums/discuss/coronavirus-covid-19-information-advice-and-surveillance-733106'

for i in range(0,17):
    url_list.append(url_part1+str(i)+url_part2)
#print(url_list)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
links_header = 'https://patient.info'


#print(soup)

# lists to store data
links_list = []
title_list = []
author_list = []
content_list = []

# scrap data
# scrap links, title
for i in range(len(url_list)):
    response = requests.get(url_list[i], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    for k in soup.find_all('article', class_="post thread"):
        title_and_link = k.find('h3', class_="post__title")
        title = title_and_link.find('a')
        title_list.append(title.get_text())
        links_list.append(links_header+title.get('href'))
        author = k.find('div', class_="post__actions post__user grid")
        author_name = author.find('a')
        author_list.append(author_name.get_text())

# scrap content
for i in range(len(links_list)):
    response = requests.get(links_list[i], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('div', id="post_content", class_="post__content")
    input = content.find('input')
    content_list.append(input.get('value'))
    #print(content_list)

# Load to CSV
df = pd.DataFrame({'Titles':title_list, 'Links':links_list, 'Author': author_list, 'Content': content_list})
#print(df)
df.to_csv('patient_data.csv')
print('Done')