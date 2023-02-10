from bs4 import BeautifulSoup
import requests
import numpy as np
import os
import pandas as pd
import re
import time
import datetime as DT
import matplotlib.pyplot as plt

def get_file_list_from_dir(datadir):
    all_files = os.listdir(os.path.abspath(datadir))
    data_files = list(filter(lambda file: file.endswith('.txt'), all_files))
    return data_files

Months = {
    'января' : '01',
    'февраля' : '02',
    'марта' : '03',
    'апреля' : '04',
    'мая' : '05',
    'июня' : '06',
    'июля' : '07',
    'августа' : '08',
    'сентября' : '09',
    'октября' : '10',
    'ноября' : '11',
    'декабря' : '12'
}

df_news = pd.read_csv('/content/drive/MyDrive/NLP/Time of news.csv')
df = pd.read_csv('/content/drive/MyDrive/NLP/GAZP_220101_221231.txt',sep=" ")

new_df = df['<DATE>'].str.split('/',expand=True)
df['<DAY>']=new_df[0]
df['<MONTH>']=new_df[1]

year=2022
start_date = DT.datetime(year, 1, 1)
end_date = DT.datetime(year, 12, 31)
days = pd.date_range(
    min(start_date, end_date),
    max(start_date, end_date)
).strftime('%d.%m.%Y').tolist()

new_df_news = df_news['Time'].str.split(' ',expand=True)
df_news['Day']=new_df_news[0]
df_news['Month']=new_df_news[1]
df_news['Time']=new_df_news[3]
df_news['Month']=df_news['Month'].map(Months)
df_news['Day']=df_news['Day'].str.zfill(2)
df_news['Text']=np.nan
for i in range(len(days)):
  name_news = get_file_list_from_dir('/content/drive/MyDrive/NLP/' + days[i])   # get the name of the files              
  for j in range(len(name_news)):
    name_str = str(name_news[j]).replace('.txt','')
    try:
      rslt_df = df_news.loc[df_news['Name of news'] == name_str]
      with open('/content/drive/MyDrive/NLP/' + days[i] + '/' + name_str + '.txt') as file:
        txt = str(file.readlines())
        txt = txt.replace('\\n', '')
        txt = re.sub(r'[^\w\s]', '', txt)
      df_news.loc[int(rslt_df.index[0]), 'Text'] = txt                          # adding the news text to the dataset
    except:
      pass

Time = df_news['Time'].str.split(':',expand=True)
Time = Time.astype(str)
Time_f=Time[0]
Time_s=Time[1]
df_news['Hour'] = Time_f
df_news['Minute'] = Time_s
df_news['New_index'] = df_news['Month'] + df_news['Day'] + df_news['Hour'] + df_news['Minute']
df_news = df_news.set_index('New_index')                                        # creating unique indexes based on date and time



df_price=df.drop(columns = ['<DATE>', '<TICKER>', '<PER>',	'<OPEN>',	'<HIGH>',	'<LOW>','<VOL>'])
Time = df_price['<TIME>'].str.split(':',expand=True)
Time = Time.astype(str)
Time_f=Time[0]
Time_s=Time[1]
df_price['<HOUR>'] = Time_f
df_price['<MINUTE>'] = Time_s
df_price['<NEW_INDEX>'] = df_price['<MONTH>'] + df_price['<DAY>'] + df_price['<HOUR>'] + df_price['<MINUTE>']
df_price = df_price.set_index('<NEW_INDEX>')


df_pr_sh=df_price.shift(-180)
test_df = pd.merge(df_news, df_price, left_index=True, right_index=True)
test_df_n = pd.merge(test_df, df_pr_sh, left_index=True, right_index=True)
test_df_n = test_df_n.drop(columns=['<DAY>_x', '<MONTH>_x', '<HOUR>_x', '<MINUTE>_x',
                                    '<DAY>_y', '<MONTH>_y', '<HOUR>_y', '<MINUTE>_y',
                                    'Hour', 'Minute'])                          # concatenate the necessary tables and remove unnecessary columns
test_df_n.rename(columns = {'<TIME>_x':'Closing time', '<CLOSE>_x':'Close',
                            '<TIME>_y':'Time in 3 hours', '<CLOSE>_y':'Closing in 3 hours'}, inplace = True )
test_df_n=test_df_n.dropna()
test_df_n['Change'] = test_df_n['Closing in 3 hours'] - test_df_n['Close']
test_df_n['Class'] = 'Good'
test_df_n.loc[test_df_n['Change']<0, 'Class'] = 'Bad'
test_df_n=test_df_n.drop(columns=['Unnamed: 0'])                                
test_df_n=test_df_n.reset_index()
test_df_n.to_csv('/content/drive/MyDrive/Finally_table')
