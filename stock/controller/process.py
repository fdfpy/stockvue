#-*- coding:utf-8 -*-
from models import dbcontrol,analyze
#from views import dict
import setting


c0=90 #本日株価下落率(@c0%の確率を設定の上)を算出する
c1=80
c2=60
hosei0=-0.2 #補正値
hosei1=-0.1 #補正値
hosei2=-0.1 #補正値

def allproc(stocknum,i,leng) :
    csvmodel = dbcontrol.CSVModel()   #CSVファイルの作成
    technical = analyze.Technical(stocknum) #株価データの収集

    try:
        getcriteria0 = analyze.GETCRITERIA(1-c0/100,hosei0,stocknum) #株価データの収集  (本日株価下落率 c0)
        getcriteria1 = analyze.GETCRITERIA(1-c1/100,hosei1,stocknum) #株価データの収集  (本日株価下落率 c0)
        getcriteria2 = analyze.GETCRITERIA(1-c2/100,hosei2,stocknum) #株価データの収集  (本日株価下落率 c0) 
        criteria_all={"cri0":getcriteria0.criteria,"cri1":getcriteria1.criteria,"cri2":getcriteria2.criteria}
    except Exception as e:
        criteria_all={"cri0":0,"cri1":1,"cri2":2}

    technical.comb.update(criteria_all)
    #print(technical.comb)
    dbcont = dbcontrol.DBCONT(technical.comb) #テクニカル分析の結果をstock.dbとcsvファイルに書き込み
    #dictprocess = dict.DictProcess(technical,stocknum) #テクニカル分析の結果のグラフ作成
    #if  i==(leng-1):  #全銘柄の分析完了後に、EXP-VOLグラフとPER時系列グラフを作成
    #    dictsummary = dict.DictSummary(technical)
    #print("dictsummary")

