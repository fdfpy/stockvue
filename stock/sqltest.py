#-*- coding:utf-8 -*-


import sys
import sqlite3
import pandas as pd
import csv
import calendar
import datetime
import setting
import json

###########################
#入力情報の読みとり
###########################

f = open(setting.STOCKDATA_PATH, 'r', encoding='utf-8')  #JSONファイルを開く,日本語を扱いたい場合はencoding='utf-8'を追記すること


json_dict = json.load(f) #開いたJSONファイルからJSONデータを読み出す。

#★★★ 銘柄パラメータを増やすときに追記する箇所★★★
STOCK_NUM=json_dict['stock_num'] #銘柄番号を取得する
C_NAME=json_dict['c_name'] #会社名
EPS=json_dict['eps'] #一株益
KESSAN=json_dict['kessan'] #ボリンジャー位置
URL=json_dict['url'] #株価1σ値
KAISYA=json_dict['kaisya'] #株価0.5σ値
HAITOUB=json_dict['haitoub'] #配当利回り
HOLD=json_dict['hold'] #配当利回り
#★★★★★★★★★★★★★★★★★★ 



########################################
# DBに記録した情報をcsvファイルにダンプする
########################################



def db_dump(c):
    sql_com='SELECT * FROM STOCK_INFO ORDER BY STOCK_NUM ASC'
    tmp=c.execute(sql_com)   
    with open(setting.CSV_DB_PATH,'w',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerows(tmp)




###########################################
# メイン処理
###########################################

if __name__=='__main__':

       

    
    try:

######################
# DBに情報を記録する
######################
        #print("A3")
        con=sqlite3.connect(setting.DB_PATH)
        con.text_factory=str
        cur=con.cursor()

        #★★★STEP3 of 4 銘柄パラメータを増やすときに追記する箇所★★★        
        insert_sql='INSERT INTO STOCK_INFO (STOCK_NUM,C_NAME,EPS,KESSAN,URL,KAISYA,HAITOUB,HOLD) values (?,?,?,?,?,?,?,?)'
        STOCK_INFO=(STOCK_NUM,C_NAME,EPS,KESSAN,URL,KAISYA,HAITOUB,HOLD)
        #★★★★★★★★★★★★★★★★★★ 

        cur.execute(insert_sql,STOCK_INFO)
        con.commit()
        db_dump(cur)
        con.close()
        print("OK")


######################
# エラー処理
# 銘柄が同じデータを書き込んだ場合は、更新する。
######################



    except sqlite3.IntegrityError as ex:
               
        if "UNIQUE constraint failed: STOCK_INFO.STOCK_NUM" in str(ex):
            print("ERROR:{}".format(ex))

            #★★★ STEP4 of 4 銘柄パラメータを増やすときに追記する箇所★★★  
            insert_sql='REPLACE INTO STOCK_INFO (STOCK_NUM,C_NAME,EPS,KESSAN,URL,KAISYA,HAITOUB,HOLD) values (?,?,?,?,?,?,?,?)'
            STOCK_INFO=[(STOCK_NUM,C_NAME,EPS,KESSAN,URL,KAISYA,HAITOUB,HOLD)]
            #★★★★★★★★★★★★★★★★★★ 

            con.executemany(insert_sql,STOCK_INFO)
            con.commit()
            db_dump(cur)
            con.close()
  
