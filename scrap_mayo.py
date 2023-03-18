import requests
from bs4 import BeautifulSoup
import csv
import lxml
import pandas as pd
import re
import html5lib

url_part1 = 'https://connect.mayoclinic.org/group/post-covid-recovery-covid-19/?pg='
url_part2 = '#discussion-listview'

# header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# url list
url_list = []
for pn in range(1,30):
    url_list.append(url_part1 + str(pn) + url_part2)
#print(url_list)


# lists to store data
links_list = []
title_list = []
author_list = []
content_list = []

# get links and title
for i in range(len(url_list)):
    # 解析HTML代码，提取出需要的信息
    response = requests.get(url_list[i], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    for k in soup.find_all('div', class_ ="discussion-info-wrap"):
        for j in k.find_all('a', class_ ="discussion-title"):
            links_list.append(j.get('href'))
            title_list.append(j.get_text())

for i in range(len(links_list)):
    child_response = requests.get(links_list[i], headers=headers)
    soup = BeautifulSoup(child_response.content, 'html.parser')
    for k in soup.find_all('div', class_ ="chv4-author-meta"):
        for j in k.find_all('a', id=re.compile("ch-profile")):
            author_list.append(j.get_text())

    for m in soup.find_all('div', class_ = "discussion-content"):
        content = m.find('p')
        content_list.append(content.get_text())
            #print(content_list)



# Load to CSV
df = pd.DataFrame({'Titles':title_list, 'Links':links_list, 'Author': author_list, 'Content': content_list})
#print(df)
df.to_csv('mayo_data.csv')
print('Done')