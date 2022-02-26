#-*- coding:utf-8 -*-
import controller.process
import pandas as pd
import setting
import datetime
import sys




d = datetime.datetime.today()

stocknum = sys.stdin.readline()  #標準入力からデータを取得する #for normal
#stocknum=str(1570) #for debug
#stocknum=str(9999) #for debug #日経平均
#stocknum='SPXL' #for debug

stocknum=stocknum.split("\n")[0] #フロントエンドから送られるデータは"\n"が付与されるので"\n"を削除している。 #for normal

#stocknum=int(stocknum)

#print("stocknum")
#print(stocknum)





controller.process.allproc(stocknum,0,1)
d = datetime.datetime.today()

if str(stocknum).isnumeric()==True:
    print("## done ##")
