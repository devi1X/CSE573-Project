import requests
from bs4 import BeautifulSoup
import csv
import lxml
import pandas as pd
import re

# lists to store data
links_list = []
title_list = []
author_list = []
content_list = []
utc_list = []
url_list = []

# get all url
url_part1 = 'https://www.medhelp.org/forums/COVID19/show/2203?page='
for i in range(1,46):
    url_list.append(url_part1+str(i))
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
links_header = 'https://www.medhelp.org'

for i in range(len(url_list)):
    # 解析HTML代码，提取出需要的信息
    response = requests.get(url_list[i], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    for k in soup.find_all('div', class_= 'subj_entry'):
        title_and_link = k.find('h2', class_='subj_title')
        title = title_and_link.find('a')
        title_list.append(title.get_text())
        links_list.append(links_header + title.get('href'))
        author = k.find('div', class_='username')
        author_name = author.find('a')
        author_list.append(author_name.get_text())

for i in range(len(links_list)):
    response = requests.get(links_list[i], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('div', class_='mh_vit_card')
    # get post time
    utc = content.find('time')
    utc_list.append(utc.get('datetime'))
    # get content text
    text = content.find('div', class_='subj_body')
    content_list.append(text.get_text())
    #print(content_list[i])


# Load to CSV
df = pd.DataFrame({'Titles':title_list, 'Links':links_list,'Post_Time': utc_list, 'Author': author_list, 'Content': content_list})
#print(df)
df.to_csv('medhelp_data.csv')
print('Done')