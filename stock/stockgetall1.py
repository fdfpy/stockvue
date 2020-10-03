#-*- coding:utf-8 -*-


import controller.process
#import models.comdata
import models.comdata
import pandas as pd
import setting
import datetime

#print("#2")
#注意：「UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-6: ordinal not in range(128)」が出力されたら
#setting.CSV_DB_PATH_COLUMNSを更新したかを確認すること
stocknum_db = pd.read_csv(setting.CSV_DB_PATH, names=setting.CSV_DB_PATH_COLUMNS,encoding='utf8') #分析する銘柄一覧を取得
                          #CSV_DB_PATH = r'/home/stock/stockdata.csv'
#print("#2")

i=0
stocknum_db_len = int(len(stocknum_db['STOCK_NUM']))
#print("#3")
#print(stocknum_db_len)


#全銘柄のデータを取得する
#while i < stocknum_db_len:
while i < 1:
    #print(stocknum_db['STOCK_NUM'][i].split("\n")[0])
#銘柄番号9999のときは為替米ドル円を取得する
    if stocknum_db['STOCK_NUM'][i]==str(9999) :
        stocknum_db['STOCK_NUM'][i]='USDJPY\n'
    else:
        pass
    
    
    controller.process.allproc(stocknum_db['STOCK_NUM'][i].split("\n")[0],i,stocknum_db_len)
    i=i+1
    #print(stocknum_db['STOCK_NUM'][i].split("\n")[0])
    d = datetime.datetime.today()


#米国金利と原油価格のスクレイピングを行う
kakusyudat = models.comdata.CTRL(setting.CSV_KAKUSYUPATH)
kakusyudat.allproc()

print("## done ##")
