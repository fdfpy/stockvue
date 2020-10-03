#-*- coding:utf-8 -*-
import sys
import sqlite3
import pandas as pd
import csv
import setting
import json
from models import dbcontrol
import sys



stock_num = sys.stdin.readline().split("\n")[0]  #標準入力からデータを取得する。 \nを削除する必要がある。

#stock_numの形式を "'xxx'"に変更する。これをしないとDBから文字列キーを検索できなくなりエラーが発生する。
moji0 = ""  
listbox = [ "'", stock_num,"'"]
stock_num=moji0 .join(listbox)


#指定した一銘柄の全登録情報をDBから読み出してcsvに書き込みを行う。
dbcontrol.SQLDBCONT(stock_num,setting.CSV_READ_PATH)
print("## done ##")