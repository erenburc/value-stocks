import yfinance as yf
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import drive_connection
import update_bq_close_price


gauth = GoogleAuth()
drive = GoogleDrive(gauth)


df = pd.read_excel('Yahoo Ticker Symbols - September 2017.xlsx',index_col = False,header=3)

df = df[["Ticker","Name","Category Name","Country"]]
df = df.loc[df['Country'] == 'Turkey']

result_df_close = pd.DataFrame()

for i in df["Ticker"]:
  try:
    company_tickers = yf.Ticker(i)
    company_tickers = company_tickers.history() # Sadece close değerini alır.
    company_tickers = company_tickers.reset_index() # Index olan date'i kolon yapar.
    company_tickers['Ticker']=i # Yeni Ticker kolonu açılır.
    result_df_close = pd.concat([result_df_close, company_tickers])
  except:
    continue

result_df_close['Date'] = result_df_close['Date'].astype(str).apply(lambda x: x.replace("\r"," "))


print(result_df_close)

result_df_close.to_csv("close_price.txt", index=False, sep='\t')


drive_connection.upload_to_drive('close_price.txt')
update_bq_close_price.update_close_price()



