
import yfinance as yf
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import drive_connection


gauth = GoogleAuth()
drive = GoogleDrive(gauth)


df = pd.read_excel('Yahoo Ticker Symbols - September 2017.xlsx',index_col = False,header=3)

df = df[["Ticker","Name","Category Name","Country"]]
df = df.loc[df['Country'] == 'Turkey']



result_df_shares = pd.DataFrame()

for i in df["Ticker"]:
  try:
    company_tickers = yf.Ticker(i).get_shares_full() # Hisse senedi adetleri alınır.
    company_tickers = company_tickers.reset_index() # Index olan date'i kolon yapar.
    company_tickers['Ticker']=i # Yeni Ticker kolonu açılır.
    result_df_shares = pd.concat([result_df_shares, company_tickers])

  except:
    continue

result_df_shares.rename(columns = {'index':'Date', result_df_shares.columns[1]:'shares_count'} , inplace=True)
print(result_df_shares)

result_df_shares.to_csv("share_count.txt", index=False, sep='\t')

drive_connection.upload_to_drive('share_count.txt')