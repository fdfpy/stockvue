#-*- coding:utf-8 -*-
import controller.process
#import models.comdata
import pandas as pd
import setting
import datetime
import os

#Raspi Localで実行するときとDocker上で実行するときで各種パスをきりわけている。
path_w = setting.STOCKNUM_PATH if os.path.exists(setting.STOCKNUM_PATH) else setting.STOCKNUM_PATH_LOCAL
setting.CSV_KAKUSYUPATH=setting.CSV_KAKUSYUPATH if os.path.exists(setting.CSV_KAKUSYUPATH) else setting.CSV_KAKUSYUPATH_LOCAL

#print("#2")
#注意：「UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-6: ordinal not in range(128)」が出力されたら
#setting.CSV_DB_PATH_COLUMNSを更新したかを確認すること
stocknum_db = pd.read_csv(setting.CSV_DB_PATH if os.path.exists(setting.CSV_DB_PATH) else setting.CSV_DB_PATH_LOCAL,
                          names=setting.CSV_DB_PATH_COLUMNS,
                          encoding='utf8') #分析する銘柄一覧を取得
                          #CSV_DB_PATH = r'/home/stock/stockdata.csv'
#print("stocknum_db")
#print(stocknum_db)

i=0
stocknum_db_len = int(len(stocknum_db['STOCK_NUM']))
#print("#3")
#print(stocknum_db_len)

#株価データ取得に失敗した銘柄を記録するファイルを用意する
with open(setting.ERRFILE_PATH, mode='w') as f:
    pass
f.close()








stocknumbox=[]
#全銘柄のデータを取得する




while i < stocknum_db_len:
    #print(stocknum_db.iloc[i]['STOCK_NUM'].item())   
    #print(type(stocknum_db.iloc[i]['STOCK_NUM'].item()))  
    #print(stocknum_db.iloc[i]['STOCK_NUM'])  


    try:
        
            #if str(stocknum_db.iloc[i]['STOCK_NUM']).isnumeric()==True: #米国株取得不可回避コード
            #print(stocknum_db.iloc[i]['STOCK_NUM'])
        controller.process.allproc(stocknum_db.iloc[i]['STOCK_NUM'],i,stocknum_db_len) #stocknum_db.iloc[i]['STOCK_NUM'].item()はnumpy.int64をintに変更する
        #else:
            #pass    
    except Exception as e:

        with open(setting.ERRFILE_PATH, mode='a') as f:
            f.write(str(stocknum_db.iloc[i]['STOCK_NUM'])+',')
        f.close()    
   


    #print(stocknum_db['STOCK_NUM'][i].split("\n")[0])
    #stocknumbox.append(stocknum_db['STOCK_NUM'][i].split("\n")[0])
    stocknumbox.append(str(stocknum_db.iloc[i]['STOCK_NUM']))   
    #print(stocknumbox)

    #エラーログ取得のため、どこまで計算を算出したかを記録するコマンド。処理を完了した銘柄番号は外部の指定テキストファイルに書き出しがされる
    with open(path_w, mode='w') as f:
        f.write('\n'.join(stocknumbox))
    f.close()

    d = datetime.datetime.today()
    i=i+1

#米国金利と原油価格のスクレイピングを行う
#kakusyudat = models.comdata.CTRL(setting.CSV_KAKUSYUPATH)
#kakusyudat.allproc()

print("## done ##")
