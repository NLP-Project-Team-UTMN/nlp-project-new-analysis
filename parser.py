from bs4 import BeautifulSoup
import requests
import numpy as np
import os
import pandas as pd
import re
import time
import datetime as DT

def replacing_characters(data):
  replace = data.replace('/',' в ').replace('\\', '').replace('\r','').replace('\n','').replace('\t','').replace(' ', '_').replace('«','').replace('»','').replace('-','')
  return replace

year = 2022
allNews = []
count=0                                                                         # csv index counter
i = 0                                                                           # month counter

time_df = pd.DataFrame(columns=['Name of news', 'Time'])

Month = ['January','February','March',                                          
         'April','May','June','July',
         'August','September','October',
         'November','December']

start_date = DT.datetime(year, 1, 1)                                            # generation of all dates for the year
end_date = DT.datetime(year, 12, 31)
days = pd.date_range(
    min(start_date, end_date),
    max(start_date, end_date)
).strftime('%d.%m.%Y').tolist()

path_to_disk = r'/content/drive/MyDrive/NLP/'

for j in range(len(days)):
  if not os.path.isdir(path_to_disk + Month[i]):
    os.makedirs(path_to_disk + Month[i])
  if not os.path.isdir(path_to_disk + Month[i] + "/"+ days[j]):
    os.makedirs(path_to_disk + Month[i]+ "/" + days[j])
  page_day = requests.get('link to site'+days[j])
  soup_day = BeautifulSoup(page_day.text, "lxml")
  links = [] 
  other_areas_container = soup_day.find_all('div', class_='thumb')
  for other in other_areas_container:
    other_areas_container_texts = other.find_all('a', href=True)
    for other_areas_container_text in other_areas_container_texts:
      links.append(other_areas_container_text['href'])
  for p in range(len(links)):
    time.sleep(1)                                                               # request time limit
    url_news = links[p]
    page_news = requests.get(url_news)
    soup_news = BeautifulSoup(page_news.text, "lxml")
    title_news = replacing_characters(soup_news.title.text)
    allNews = soup_news.find('div', class_='articleBodyСlass').text
    t = re.sub('\t','', allNews)
    t = t.split('Автор', 1)[0]
    try:
      t = t.split('RU.', 1)[1]
    except:
      pass
    time_news = soup_news.time.text 
    time_df.at[count,'Name of news']=title_news
    time_df.at[count,'Time']=time_news
    count+=1
    try:
      if days[j]>days[j+1]:                                                     # comparison by unicode
        with open(path_to_disk + Month[i]+ "/"+ days[j] + "/" + str(title_news)+'.txt', "w+") as file:
          file.write(t)
        time_df.at[count,'Name of news']=title_news+'.txt'
        time_df.at[count,'Time']=time_news
        i+=1
        break
      else:
        with open(path_to_disk + Month[i]+ "/"+ days[j] + "/" + str(title_news)+'.txt', "w+") as file:
          file.write(t)
        time_df.at[count,'Name of news']=title_news+'.txt'
        time_df.at[count,'Time']=time_news
    except:
      try:
        with open(path_to_disk + Month[i]+ "/"+ days[j] + "/" + 'File_day_'+str(j)+'_news_'+str(p)+'.txt', "w+") as file:
          file.write(t)
        time_df.at[count,'Name of news']='File_day_'+str(j)+'_news_'+str(p)+'.txt'
        time_df.at[count,'Time']=time_news
      except:
        pass

time_df.to_csv("/content/drive/MyDrive/NLP/Time of news.csv")    
