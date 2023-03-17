import requests
from bs4 import BeautifulSoup
import csv
import lxml
import pandas as pd
import re


url4 = 'https://covid19.camhx.ca/mod/forum/view.php?id=1'


response = requests.get(url4)
html = response.text
#print(html)

# 解析HTML代码，提取出需要的信息
soup = BeautifulSoup(html, 'lxml')

# lists to store data
links_list = []
title_list = []

# 子网页list
question_list = []

# Find主论坛的Title和URL
for k in soup.find_all('a', class_=re.compile("w-100")):
    links_list.append(k.get('href'))
    title_list.append(k.get('aria-label'))

# 子网页
i = 0
for i in range(len(links_list)):
    child_response = requests.get(links_list[i])
    child_html = child_response.text
    soup = BeautifulSoup(child_html, 'lxml')
    # FIND
    for k in soup.find_all('div', id=re.compile("post-content"), class_=re.compile("post-content")):
        question_list.append(k.get_text())


    #print(question_list[i])
    i += 1


#print(question_list)

#load data to csv
df = pd.DataFrame({'Titles':title_list, 'Links':links_list})
#print(df)
df2 = pd.DataFrame({'Questions':question_list})
#print(df2)
df.to_csv('link.csv')
df2.to_csv('ChildPage_Answer.csv')
print('Done')