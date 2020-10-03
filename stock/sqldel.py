# coding: utf-8

import sys
import sqlite3
import pandas as pd
import csv
import setting
import json


###########################
#入力情報の読みとり
###########################

f = open(setting.STOCKDEL_PATH, 'r')  #JSONファイルを開く
#print("A1")
json_dict = json.load(f) #開いたJSONファイルからJSONデータを読み出す。
STOCK_NUM=json_dict['stock_num'] #銘柄番号を取得する



Inx=STOCK_NUM
#Inx=unicode(Inx, 'utf-8')
InxARY=Inx.split(',')


########################################
# DBに記録した情報をcsvファイルにダンプする
########################################


def delete_task(c,num):

    sql='DELETE FROM STOCK_INFO WHERE STOCK_NUM=?'
    cur=c.cursor()
    cur.execute(sql,(num,))
    c.commit()

def db_dump(c):
    sql_com='SELECT * FROM STOCK_INFO ORDER BY STOCK_NUM ASC'
    cur=c.cursor()
    tmp=cur.execute(sql_com)  
    with open(setting.CSV_DB_PATH,'w',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerows(tmp)






###########################################
# メイン処理
###########################################

if __name__=='__main__':



    
    try:

######################
# 指定行を削除する
######################
        for i in InxARY:
            con=sqlite3.connect(setting.DB_PATH)
            delete_task(con,i)
            db_dump(con)
            con.close()
            print("DEL DONE")
    except Exception as ex:
        print("ERROR:{}".format(ex))

