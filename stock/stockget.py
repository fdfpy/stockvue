#-*- coding:utf-8 -*-
import controller.process
import pandas as pd
import setting
import datetime
import sys




d = datetime.datetime.today()

stocknum = sys.stdin.readline()  #標準入力からデータを取得する
#stocknum=str(4345) #for debug
#stocknum='VOOV' #for debug
stocknum=stocknum.split("\n")[0] #フロントエンドから送られるデータは"\n"が付与されるので"\n"を削除している。
#stocknum=int(stocknum)

#print("stocknum")
#print(stocknum)



#銘柄番号9999のときは為替米ドル円を取得する
if stocknum==str(9999) :
    stocknum='USDJPY'
    #print(stocknum)


controller.process.allproc(stocknum,0,1)
d = datetime.datetime.today()

print("## done ##")
