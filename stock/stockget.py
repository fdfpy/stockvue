#-*- coding:utf-8 -*-
import controller.process
import pandas as pd
import setting
import datetime
import sys




d = datetime.datetime.today()

stocknum = sys.stdin.readline()  #標準入力からデータを取得する #for normal
#stocknum=str(5388) #for debug
#stocknum=str("JPYX") #for debug

#stocknum='VOOV' #for debug
stocknum=stocknum.split("\n")[0] #フロントエンドから送られるデータは"\n"が付与されるので"\n"を削除している。 #for normal

#stocknum=int(stocknum)

#print("stocknum")
#print(stocknum)





controller.process.allproc(stocknum,0,1)
d = datetime.datetime.today()

print("## done ##")
