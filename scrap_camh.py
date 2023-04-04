import requests
from bs4 import BeautifulSoup
import csv
import lxml
import pandas as pd
import re


url = 'https://covid19.camhx.ca/mod/forum/view.php?id=1'


response = requests.get(url)
html = response.text
#print(html)

# 解析HTML代码，提取出需要的信息
soup = BeautifulSoup(html, 'lxml')

# lists to store data
links_list = []
title_list = []
author_list = []
content_list = []
utc_list = []

# 子网页list
question_list = []
child_author_list = []
child_links_list = []
child_title_list = []

# Find主论坛的Title和URL
# get links and title
for k in soup.find_all('a', class_=re.compile("w-100")):
    links_list.append(k.get('href'))
    title_list.append(k.get('aria-label'))

# get author, utc
for k in soup.find_all('td', class_ ="author align-middle fit-content limit-width px-3"):
    for j in k.find_all('div', class_ ="mb-1 line-height-3 text-truncate"):
        author_list.append(j.get_text())

print(utc_list)

# 子网页
i = 0
for i in range(len(links_list)):
    child_response = requests.get(links_list[i])
    child_html = child_response.text
    soup = BeautifulSoup(child_html, 'lxml')
    for k in soup.find_all('div', class_=re.compile("firstpost")):
        for j in k.find_all ('div', id=re.compile("post-content"), class_=re.compile("post-content")):
            content_list.append(j.get_text())
    # FIND
    for k in soup.find_all('div', id=re.compile("post-content"), class_=re.compile("post-content")):
        question_list.append(k.get_text())
        # 给子表赋Title及Link
        child_links_list.append(links_list[i])
        child_title_list.append(title_list[i])

    for j in soup.find_all('a', href=re.compile("user")):
        child_author_list.append(j.get_text())


    utc = soup.find('time')
    utc_list.append(utc.get('datetime'))
    #print(utc_list)

    #print(question_list[i])
    i += 1

#print(content_list)
#test_df = pd.DataFrame({'Content': content_list})
#print(test_df)
#test_df.to_csv('test.csv')


#load data to csv
df = pd.DataFrame({'Titles':title_list, 'Links':links_list,'Post_Time': utc_list, 'Author': author_list, 'Content': content_list })
#print(df)
#df2 = pd.DataFrame({'Author':child_author_list,'Title': child_title_list,'Links': child_links_list,'Questions':question_list})
#print(df2)
df.to_csv('camh_data.csv')
#df2.to_csv('ChildPage_Answer.csv')
print('Done')