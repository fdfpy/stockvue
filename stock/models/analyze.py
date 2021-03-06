#-*- coding:utf-8 -*-
import datetime,setting,jsm
from pandas import Series ,DataFrame
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from models import dbcontrol
import math
import os
import pandas_datareader.data as web #米国株データの取得ライブラリを読み込む
from scipy.stats import gaussian_kde
from scipy.integrate import cumtrapz #pdfを全区間で積分するためのライブラリ
from sklearn import linear_model
from pandas_datareader import data as pdr
import yfinance as yfin
import requests, bs4
yfin.pdr_override()

INITIAL_AF = 0.02 #パラボリックパラメータ
MAX_AF = 0.2 #パラボリックパラメータ



setting.HOME_PATH=setting.HOME_PATH if os.path.exists(setting.HOME_PATH) else setting.HOME_PATH_LOCAL
setting.GET_STOCK_F=setting.GET_STOCK_F if os.path.exists(setting.GET_STOCK_F) else setting.GET_STOCK_F_LOCAL




class StockGetTop(object):
    def __init__(self, stocknum = None):


        self.stocknum = str(stocknum)
        self.Y = datetime.datetime.today().year
        self.M = datetime.datetime.today().month
        self.D = datetime.datetime.today().day

class StockGetTop(object):
    def __init__(self, stocknum = None):


        self.stocknum = str(stocknum)
        self.Y = datetime.datetime.today().year
        self.M = datetime.datetime.today().month
        self.D = datetime.datetime.today().day


class StockGet(StockGetTop):

    def __init__(self, stocknum = None):
        super().__init__(stocknum)
    
    ########## 株探から株価を取得する ##########################
    
    @classmethod   
    def get_kabutan(self,stocknum):

        # if stocknum==0:
        #     stocknum=str("0000")
        # print("stocknum")
        # print(str(stocknum))

        #stocknum=str(stocknum)
        if stocknum==str(9999):
            res = requests.get('https://kabutan.jp/stock/kabuka?code=0000&ashi=day')
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "html.parser")

            def datconv(moji):
                return int(float(moji.get_text().replace(',', '')))


            today_225=soup.find_all("table")[4] #日経225本日の株価データ抽出
            kako_225=soup.find_all("table")[5] #日経225過去30日分のデータを抽出する

            #本日の日経225'始値','高値','安値','終値','売買高(株)'をスクレイピングする
            t225_dat=[[today_225.find("time").get_text(),
                datconv(today_225.find_all("td")[0]),        
                datconv(today_225.find_all("td")[1]),        
                datconv(today_225.find_all("td")[2]),        
                datconv(today_225.find_all("td")[3]),
                datconv(today_225.find_all("td")[6]),
                ]]

            i=0
            kako225_data=[]
            #過去14日に日経平均株価を吸いクレイピングする
            for i in range (0,14):
                kako225_tmp=[kako_225.find_all("time")[i].get_text(),
                    datconv(kako_225.find_all("td")[0+7*i]),        
                    datconv(kako_225.find_all("td")[1+7*i]),        
                    datconv(kako_225.find_all("td")[2+7*i]),        
                    datconv(kako_225.find_all("td")[3+7*i]),
                    datconv(kako_225.find_all("td")[6+7*i]),
                    ] 
    
                kako225_data.append(kako225_tmp)


            df_today_225=pd.DataFrame(t225_dat,columns=['本日','始値','高値','安値','終値','売買高(株)'])
            df_kako_225=pd.DataFrame(kako225_data,columns=['日付','始値','高値','安値','終値','売買高(株)'])


            #dfstmp=pd.concat([df_today_225, df_kako_225], join='outer')


        else:

            dfstmp = pd.read_html("https://kabutan.jp/stock/kabuka?code=" + str(stocknum))




        #前日から20日前までに株価情報を取得する。
        #print("dfstmp[5]")
        #print(dfstmp[5])
        #dfs20 =  dfstmp[5].head(20).loc[:,['日付','始値','高値','安値','終値','売買高(株)']]
        dfs20 = df_kako_225 if stocknum==str(9999) else dfstmp[5].head(20).loc[:,['日付','始値','高値','安値','終値','売買高(株)']]
        dfs20= dfs20.rename(columns={'日付': 'DATE0','始値': 'OPEN', '高値': 'HIGH', '安値': 'LOW', '終値': 'CLOSE', '売買高(株)': 'VOL'  })#各列名を所望の列名に変更する。
        dfs20['DATE0'] = '20' + dfs20['DATE0']  
        dfs20['DATE'] = pd.to_datetime(dfs20['DATE0'], format='%Y/%m/%d')
        dfs20 =  dfs20.loc[:,['OPEN','HIGH','LOW','CLOSE','VOL','DATE']]
        dfs20 =dfs20.reindex(columns=['DATE','CLOSE','OPEN','HIGH','LOW','VOL'])
        dfs20.set_index('DATE',inplace=True)
        dfs20=dfs20.sort_values(['DATE'],ascending = True)
        #print("dfs20")
        #print(dfs20)

        #本日の株価情報を取得する。  
        dfstoday = df_today_225 if stocknum==str(9999) else dfstmp[4].loc[:,['本日','始値','高値','安値','終値','売買高(株)']]
        dfstoday= dfstoday.rename(columns={'本日': 'DATE0','始値': 'OPEN', '高値': 'HIGH', '安値': 'LOW', '終値': 'CLOSE', '売買高(株)': 'VOL'  })#各列名を所望の列名に変更する。

        #print("dfstoday")
        #print(dfstoday)

        dfstoday['DATE0'] = '20' + dfstoday['DATE0']  
        dfstoday['DATE'] = pd.to_datetime(dfstoday['DATE0'], format='%Y/%m/%d')
        dfstoday =  dfstoday.loc[:,['OPEN','HIGH','LOW','CLOSE','VOL','DATE']]
        dfstoday =dfstoday.reindex(columns=['DATE','CLOSE','OPEN','HIGH','LOW','VOL'])
        dfstoday.set_index('DATE',inplace=True)

        #前日から20日前までに株価情報 と 本日の株価情報を結合する
        dfs20 = pd.concat([dfs20,  dfstoday], join='outer') #df0とdf1を和結合させる。

        #print("dfs20")
        #print(dfs20)
      
        return dfs20


    @classmethod   
    def get_kabuka(self,stocknum):
        

        Y = datetime.datetime.today().year
        M = datetime.datetime.today().month
        D = datetime.datetime.today().day
        start=datetime.datetime(Y-2, M, D)
        end=datetime.datetime(Y, M, D)


        snum=stocknum +".T" if str(stocknum).isnumeric()==True else stocknum 


        #df=web.DataReader(snum ,'yahoo',start,end) #株価データを取得する。2021/7/2から使用できなくなっている
        df = pdr.get_data_yahoo(snum, start, end)






        df.reset_index('Date',inplace=True)
        df=df.drop(columns='Adj Close') #列Aを削除する。
        df=df.rename(columns={'Date': 'DATE','High': 'HIGH','Low': 'LOW', 'Open': 'OPEN', 'Close': 'CLOSE', 'Volume': 'VOL'})#各列名を所望の列名に変更する。
        df=df.reindex(columns=['DATE','CLOSE','OPEN','HIGH','LOW','VOL']) #列を入れ替える
        df.set_index('DATE',inplace=True)

        return df


    @classmethod  
    def kesson(self,x):
        #print("#x")
        #x=pd.DataFrame(x)
        #print(type(x))
 

        if x.OPEN=='－':
            # x.CLOSE = int(x.CLOSE)
            # x.OPEN = int(x.CLOSE)-1
            # x.LOW = int(x.CLOSE)-1
            # x.HIGH =int(x.CLOSE)+1
            x.CLOSE =30000.0
            x.OPEN = 29999.0
            x.LOW = 30001.0
            x.HIGH =30001.0


        #print(x)    
        return x




    @classmethod   
    def proc(self,stocknum):


        filepath=setting.HOME_PATH + str(stocknum) + ".csv"

        ##(1)株式の場合        
        if str(stocknum).isnumeric()==True:

            ##(1-1)新規にデータを取得する銘柄
            if os.path.exists(filepath)==False :
 
                df0=self.get_kabutan(stocknum)
                df1=self.get_kabuka(stocknum)
                dfc=pd.concat([df0, df1], join='outer') #df0とdf1を和結合させる。
                dfc1 = dfc.groupby(level=0).last()  #重複行は削除する。


            ##(1-2)すでにデータを取得した銘柄
            else:
                df0 = pd.read_csv(str(filepath))#index_col=0は列名もデータと一緒に取り出す。
                df0['DATE0'] = pd.to_datetime(df0['DATE'], format='%Y/%m/%d') #文字列型日付けを日付け型に変更する
                df0=df0.drop(columns='DATE') #列Aを削除する。
                df0=df0.rename(columns={'DATE0': 'DATE'})#各列名を所望の列名に変更する。
                df0.set_index('DATE',inplace=True)

                df1 = self.get_kabutan(stocknum)

                dfc = pd.concat([df0, df1], join='outer') #df0とdf1を和結合させる。
                dfc1 = dfc.groupby(level=0).last()  #重複行は削除する。
   


        ##(2)指数系銘柄または米国株の場合
        else:


            if stocknum==str("^JPYX"):  #為替
                stocknum="JPY=X"
            if stocknum==str("^CLF"):  #原油
                stocknum="CL=F"  

            dfc1=self.get_kabuka(stocknum)

        #取引なしの日は「-」が記入され、テクニカル分析ができなくなるので「-」をclose値に置き換える。
        dfc1=dfc1.apply(lambda x:self.kesson(x),axis=1)
        #print("dfc1")
        #print(dfc1)

        #取引なしの日は「-」が記入され、kesson(x)関数で修正処理をしてもデータの型が合わなくなり、以降のテクニカル分析でエラーを発生させる。
        #よって、再度csvファイルからデータを読み出す処理を実施している。
        dfc1.to_csv(str(filepath),header=True)
        dfc1 = pd.read_csv(str(filepath))
        dfc1['DATE'] = pd.to_datetime(dfc1['DATE'], format='%Y/%m/%d') #文字列型日付けを日付け型に変更する
        dfc1.set_index('DATE',inplace=True)


        self.db_s=dfc1











class Technical(StockGet):  #銘柄の株価よりテクニカル分析計算を行う。
    def __init__(self,stocknum):
        super().__init__(stocknum)
        #print("self.db_s")
        #print(self.db_s)      
        StockGet.proc(stocknum)    #株価を取得する。    
        self.kabuka_get(self.db_s) #銘柄の本日の株価と昨日との差を求める。
        self.vol_get(self.db_s)   #株価のshigma値を取得する。     
        self.ichimoku(self.db_s) #一目均衡表
        self.bolinger(self.db_s) #ボリンジャーバンドの計算
        self.calc_parabolic(self.db_s) #パラボリック解析
        self.shaperatio(self.db_s) #shape ratioの計算
        self.calmar(self.db_s)   #calmar ratioの計算
        self.combine()  #DBCONTオブジェクトに渡す変数をまとめる。
 

        ######################################################
        #self.getsymbol(self.db_s) #日足情報
        #self.vol_get(self.db_s) #Volatirity calculation
        #self.getsymbol(self.db_s) #日足情報
        #self.week_getsymbol(self.db_sw) #週足情報        
        #print("analyze2")
        #self.macd(self.db_s)
        #print("analyze2.5")
        #self.smaget(self.db_s)
        #print("analyze3")
        #self.getbps()
        #print("analyze4")
        #self.getper(self.db_s)
        #self.smacross(self.db_s)
        #self.bolinger(self.db_s)
        #self.smaweekget(self.db_sw)
        #self.kairi(self.db_s)       
        #print("self.db_sw")
        #print(self.db_sw)

    def kabuka_get(self, mat): #銘柄の本日の株価と昨日との差を求める。
        #print("mat")
        #print(mat)
        self.today_kabuka=mat['CLOSE'].tail(1)[0]
        kinou_kabuka=mat[len(mat)-2:len(mat)-1]['CLOSE'][0]
        self.dif_kabuka=self.today_kabuka-kinou_kabuka
        #print("today_kabuka")
        #print(self.today_kabuka)  
        #print("dif_kabuka")
        #print(round(self.dif_kabuka,1))  

    def future_day(self, today,d): #todayのd日後の日付を算出する。
        return datetime.date(today.year, today.month, today.day)+datetime.timedelta(days=d)


    def ichimoku(self, mat): #一目均衡表を計算する。
        #print(mat)
        vec = []
        today=mat.index[len(mat.index)-1]
        today=datetime.date(today.year, today.month, today.day) #todayは%H:%M:%S'を含むので、%H:%M:%Sを削除する。

        #today = datetime.datetime.strptime(str(mat.index[len(mat.index)-1]), '%Y-%m-%d') #最新の日付を算出する




        #print(today)
        todaykabuka=mat.tail(1)['CLOSE'][0]
        for i in range(24):  #最新の日付から25日先の日付までを生成する       
            vec.append(self.future_day(today,i+1))


        #最新の日付から25日先までの日付をindexにもつDataFrameを作成する。
        matd = pd.DataFrame(0,index=vec, columns=['CLOSE', 'OPEN', 'HIGH', 'LOW', 'VOL'])
        
        mat=mat.append(matd,sort=True) #最新の日付から25日先の日付までをドッキングする

        #df2 = pd.DataFrame(0,index=vec, columns=['TENKAN', 'KIJYUN', 'SENKOU1', 'SENKOU2', 'CHIKOU2'])
        #print("mat")
        #print(mat)


        #print(mat.index[len(mat.index)-1])


        df_high_rate = mat['HIGH']
        df_low_rate = mat['LOW']
        df_close_rate=mat['CLOSE']

        #転換線の算出 
        df_high_tenkan = df_high_rate.rolling(9).max()
        df_low_tenkan = df_low_rate.rolling(9).min()
        df_tenkan = (df_high_tenkan + df_low_tenkan)/2
        #print(df_tenkan)


        #基準線の算出
        df_high_kijyun = df_high_rate.rolling(26).max()
        df_low_kijyun = df_low_rate.rolling(26).min()
        df_kijyun = (df_high_kijyun + df_low_kijyun)/2
        #print(df_kijyun)


        #先行スパン1の算出
        df_senkouspan1 = (df_tenkan + df_kijyun)/2
        df_senkouspan1 = df_senkouspan1.shift(25)
        #print(df_senkouspan1)

        #先行スパン2の算出
        df_high_senkouspan2 = df_high_rate.rolling(52).max()
        df_low_senkouspan2 = df_low_rate.rolling(52).min()
        df_senkouspan2 = (df_high_senkouspan2 + df_low_senkouspan2)/2
        df_senkouspan2 = df_senkouspan2.shift(25)
        #print(df_senkouspan2)


        #遅行スパンの算出
        df_chikouspan = mat['CLOSE'].shift(-25)

        #一目均衡表の要素を集めたDataFrameを作成する。
        df_ichimokumat = DataFrame(mat, columns=['TENKAN', 'KIJYUN', 'SENKOU1', 'SENKOU2', 'CHIKOU2'])
        df_ichimokumat['TENKAN'] = df_tenkan
        df_ichimokumat['KIJYUN'] = df_kijyun
        df_ichimokumat['SENKOU1'] = df_senkouspan1
        df_ichimokumat['SENKOU2'] = df_senkouspan2 
        df_ichimokumat['CHIKOU2'] = df_chikouspan              

        #print(df_ichimokumat)
        #print(today.strftime("%Y-%m-%d"))

        #最新日の一目均衡表データを抽出する。
        ichimoku_today=df_ichimokumat.loc[ df_ichimokumat.index[[len(df_ichimokumat.index)-25]] ] 
        #最新日から25日前の一目均衡表データを抽出する。
        ichimoku_today_25mae=df_ichimokumat.loc[ df_ichimokumat.index[[len(df_ichimokumat.index)-51]] ]  
        #最新日から25日後の一目均衡表データを抽出する。        
        ichimoku_today_25after=df_ichimokumat.loc[ df_ichimokumat.index[[len(df_ichimokumat.index)-1]] ] 

        today_tenkansen=ichimoku_today['TENKAN'][0]
        today_kijyunsen=ichimoku_today['KIJYUN'][0]
        today_senkouspan2=ichimoku_today['SENKOU2'][0]
        self.today_tenkansen=today_tenkansen #本日の転換線計算値を外部に出力する

        # print("ichimoku_today")
        # print(ichimoku_today)
        # print("todaykabuka")
        # print(todaykabuka)
        # print("today_tenkansen")
        # print(today_tenkansen)
        # print("today_kijyunsen")
        # print(today_kijyunsen)
        # print("today_senkouspan2")
        # print(today_senkouspan2)

        if today_kijyunsen >= today_tenkansen and todaykabuka < today_kijyunsen  and todaykabuka >= today_senkouspan2 :
            self.meigara_sta=4

        elif today_kijyunsen >= today_tenkansen and todaykabuka < today_kijyunsen  and todaykabuka < today_senkouspan2 :
            self.meigara_sta=5

        elif today_kijyunsen >= today_tenkansen and todaykabuka >= today_kijyunsen  and todaykabuka < today_senkouspan2 :
            self.meigara_sta=0

        elif today_kijyunsen >= today_tenkansen and todaykabuka >= today_kijyunsen  and todaykabuka >= today_senkouspan2 :
            self.meigara_sta=6

        elif today_kijyunsen < today_tenkansen and todaykabuka < today_kijyunsen  and todaykabuka < today_senkouspan2 :
            self.meigara_sta=7

        elif today_kijyunsen < today_tenkansen and todaykabuka < today_kijyunsen  and todaykabuka >= today_senkouspan2 :
            self.meigara_sta=3

        elif today_kijyunsen < today_tenkansen and todaykabuka >= today_kijyunsen  and todaykabuka >= today_senkouspan2 and todaykabuka >= today_tenkansen:
            self.meigara_sta=21

        elif today_kijyunsen < today_tenkansen and todaykabuka >= today_kijyunsen  and todaykabuka >= today_senkouspan2 and todaykabuka < today_tenkansen:
            self.meigara_sta=20

        elif today_kijyunsen < today_tenkansen and todaykabuka >= today_kijyunsen  and todaykabuka < today_senkouspan2 and todaykabuka >= today_tenkansen :
            self.meigara_sta=11           

        elif today_kijyunsen < today_tenkansen and todaykabuka >= today_kijyunsen  and todaykabuka < today_senkouspan2 and todaykabuka < today_tenkansen :
            self.meigara_sta=10




        # print("meigara_sta") 
        # print(self.meigara_sta)      
 
        #print("ichimoku_today_25after")
        #print(ichimoku_today_25after) 

        #df_ichimokumatをcsvファイルに書き出し
        df_ichimokumat.to_csv("test.csv")

    #過去2年分の株価変動のvolatirityを取得する。　
    def vol_get(self, mat):

        stock_vol = 100 * mat['CLOSE'].pct_change() #n番目のデータとn-1番目のデータの変化率を取得する。
        stock_vol = stock_vol.dropna() #欠損データの除去を行っている。
        volatirity = np.std(stock_vol) #過去1年の株価のボラティリティーの標準偏差計算
        stock_now = mat['CLOSE'].tail(1)[0]
        #print("stock_vol")
        #print(stock_vol)
        #print("volatirity")       
        #print(volatirity)
        #print("stock_now")
        #print(stock_now)        

        self.stock_p1sig = round(stock_now*(math.e**(volatirity/100)), 0)
        self.stock_p05sig = round(stock_now*(math.e**(0.5*volatirity/100)), 0)
        self.stock_n1sig = round(stock_now*(math.e**(-volatirity/100)), 0)
        self.stock_n05sig = round(stock_now*(math.e**(-0.5*volatirity/100)), 0)
        #print(stock_p1sig)
        #print(stock_n1sig)        

    #ボリンジャーバンドの計算
    def bolinger(self, mat):
        #print("mat")
        #print(mat)
        mat = DataFrame(mat['CLOSE'].dropna())
        ma_boli = DataFrame(mat, columns=['CLOSE', 'MA_M', 'B_U1', 'B_U2', 'B_U3', 'B_L1', 'B_L2', 'B_L3', 'B_STV'])
        #print("ma_boli")
        #print(ma_boli)       
        ma_boli['MA_M'] = ma_boli['CLOSE'].rolling(window=setting.M_IDOU, center=False).mean()
        ma_boli['B_STV'] = ma_boli['CLOSE'].rolling(window=setting.M_IDOU, center=False).std(ddof=0)
        ma_boli['B_U1'] = ma_boli['MA_M'] + ma_boli['B_STV']
        ma_boli['B_U2'] = ma_boli['MA_M'] + 2*ma_boli['B_STV']
        ma_boli['B_U3'] = ma_boli['MA_M'] + 3*ma_boli['B_STV']
        ma_boli['B_L1'] = ma_boli['MA_M'] - ma_boli['B_STV']
        ma_boli['B_L2'] = ma_boli['MA_M'] - 2*ma_boli['B_STV']
        ma_boli['B_L3'] = ma_boli['MA_M'] - 3*ma_boli['B_STV']
        #print("ma_boli")
        #print(ma_boli)   
        today_boli=ma_boli.tail(1)
        #print("today_boli")
        #print(today_boli) 

        #print("today_boli['B_U1']")
        #print(today_boli['B_U1'][0])
        stock_now=today_boli['CLOSE'][0]
        #print(stock_now)



        today_sig = {"today_p1sig" : today_boli['B_U1'][0],
                     "today_p2sig" : today_boli['B_U2'][0],
                     "today_p3sig" : today_boli['B_U3'][0], 
                     "today_n1sig" : today_boli['B_L1'][0],
                     "today_n2sig" : today_boli['B_L2'][0],
                     "today_n3sig" : today_boli['B_L3'][0],
                     "baseline"    : today_boli['MA_M'][0],
                     "sigma"       : today_boli['B_STV'][0]
                     }

        self.today_n=(stock_now-today_sig["baseline"])/today_sig["sigma"]
    
        #print(today_sig)
        #print("today_n",self.today_n)


        df_bolsta= pd.read_csv(setting.HOME_PATH + "bolsta.csv",encoding='utf-8',index_col=0) #index_col=0は列名もデータと一緒に取り出す。
     
        try:
            bol10=float(df_bolsta.loc[self.stocknum0 if self.stocknum0.isnumeric()==True else self.stocknum0,'10%'])   
            bol90=float(df_bolsta.loc[self.stocknum0 if self.stocknum0.isnumeric()==True else self.stocknum0,'90%'])

        except Exception as e:

            bol10="NONE"
            bol90="NONE"


        if bol10=="NONE":
            self.band="ERR"     
        else:
            if self.today_n < bol10 :
                self.band="D10"
            elif  bol10 <= self.today_n and self.today_n <=bol90 :
                self.band=round(self.today_n,1)
            elif  self.today_n > bol90 :
                self.band="U90"

        
        #print(self.band)

    def combine(self): #DBCONTオブジェクトに渡す変数をまとめる。

        self.comb = {"stocknum" :self.stocknum,
                     "today_kabuka" :int(self.today_kabuka),
                     #"dif_kabuka" :round(self.dif_kabuka,1),
                     "dif_kabuka" :int(self.dif_kabuka),                     
                     "band":self.band,
                     "p1sig":self.stock_p1sig, 
                     "p05sig":self.stock_p05sig,
                     "n1sig":self.stock_n1sig,
                     "n05sig":self.stock_n05sig,
                     "meigara_sta":self.meigara_sta,
                     "tenkansen" :self.today_tenkansen,
                     "para_sar":self.sar_latest,
                     "para_status":self.status_latest,
                     "sharp_ratio":self.spr,
                     "culmar_ratio":self.clmr,
                     "ar": self.ar_latest #2020/12 add
        }

                    

        #print("self.comb")
        #print(self.comb)

    #パラボリック解析
    def calc_parabolic(self,mat):
        # 初期値
        acceleration_factor = INITIAL_AF
        # INFO: 初期状態は上昇トレンドと仮定して計算
        bull = True
        extreme_price = mat.HIGH[0]
        temp_sar_array = [mat.LOW[0]]
        status=0
        status_array=[]
        ar_array=[] #2020/12 add

        # HACK: dataframeのまま処理するより、to_dictで辞書配列化した方が処理が早い
        candles_array = mat.to_dict('records')
        for i, row in enumerate(candles_array):
            current_high = row['HIGH']
            current_low = row['LOW']
            last_sar = temp_sar_array[-1]

            # レートがparabolicに触れたときの処理
            if self.parabolic_is_touched(
                bull=bull,
                current_parabo=last_sar,
                current_h=current_high, current_l=current_low
            ):
                #print('touch',i)
                temp_sar = extreme_price
                acceleration_factor = INITIAL_AF
                if bull:
                    bull = False
                    extreme_price = current_low
                    status=0
                else:
                    bull = True
                    extreme_price = current_high
                    status=0
            else:
                # SARの仮決め
                #print('nontouch',i)
                temp_sar = self.calc_next_parabolic(
                    last_sar=last_sar, ep=extreme_price, acceleration_f=acceleration_factor
                )
                #print("i",i)
                #print("temp_sar",temp_sar)
                #print("last_sar",last_sar)
                #print("extreme_price",extreme_price)
                #print("acceleration_factor",acceleration_factor)

                # AFの更新
                if (bull and extreme_price < current_high) \
                    or not bull and extreme_price > current_low:
                    acceleration_factor = min(
                        acceleration_factor + INITIAL_AF,
                        MAX_AF
                    )
                
                #print("i",i)
                #print("temp_sar",temp_sar)
                #print("last_sar",last_sar)
                #print("extreme_price",extreme_price)
                #print("acceleration_factor",acceleration_factor)
                
                # SARの調整
                if i>1:
                    if bull:
                        temp_sar = min(
                           temp_sar, candles_array[i-1]['LOW'], candles_array[i-2]['LOW']
                        )
                        # print("TRUE",i)
                        #print("candles_array[i-1]['low']", candles_array[i-1]['low'])
                        #print("candles_array[i-2]['low']", candles_array[i-2]['low'])                
                        #print("temp_sar:::",temp_sar)
                        extreme_price = max(extreme_price, current_high)
                    else:
                        temp_sar = max(
                            temp_sar, candles_array[i-1]['HIGH'], candles_array[i-2]['HIGH']
                        )
                        #print("FALSE",i)
                        extreme_price = min(extreme_price, current_low)

            if i == 0:
                temp_sar_array[-1] = temp_sar
                status=1 if bull==True else -1
                status_array.append(status)
                ar_array.append(acceleration_factor) #2020/12 add
                #print("temp_sar_array[-1]", temp_sar_array[-1])
            else:
                temp_sar_array.append(temp_sar)
                status=status+1 if bull==True else status-1
                status_array.append(status)
                ar_array.append(acceleration_factor) #2020/12 add

        self.sar_latest=temp_sar_array[len(temp_sar_array)-1]
        self.status_latest=status_array[len(status_array)-1]
        self.ar_latest=ar_array[len(ar_array)-1]     #2020/12 add 
        #print("self.ar_latest")        
        #print(self.ar_latest)   
        df0 = pd.DataFrame(temp_sar_array,columns=["SAR"])
        df1= pd.DataFrame(status_array,columns=["STATUS"])
        df2= pd.DataFrame(ar_array,columns=["AR"]) #2020/12 add
        dfc=pd.concat([df0, df1,df2],axis=1) #2020/12 add
        #print("dfc",dfc)
        #print("sar_latest",self.sar_latest)    
        #print("status_latest",self.status_latest)  






    def calc_next_parabolic(self,last_sar, ep, acceleration_f=INITIAL_AF):
        return last_sar + acceleration_f * (ep - last_sar)


    def parabolic_is_touched(self,bull, current_parabo, current_h, current_l):
    
        #print("current_parabo",current_parabo)
        #print("current_l", current_l)    
        #print("current_h", current_h)    
        #print("not bull", not bull)
        if bull and (current_parabo > current_l):
            #print("A1")
            return True
        elif not bull and (current_parabo < current_h):
            #print("A2")
            return True
            #print("A3")
        return False


    #Sharp Ratioを計算する関数
    def shaperatio(self,DF):

        df = DF.copy()
        df["daily_ret"] = DF["CLOSE"].pct_change() #株価終値の前日との変化率を計算する。
        ret_ave=np.mean(df["daily_ret"])
        vol_sp = df["daily_ret"].std()
        #print("sharp ratio:",math.sqrt(256)*ret_ave/vol_sp) 
        self.spr=math.sqrt(256)*ret_ave/vol_sp

    #Sharp Ratioを計算する関数
    def calmar(self,DF):
        "function to calculate calmar ratio"
        df = DF.copy()
        self.clmr = self.CAGR(df)/self.max_dd(df)
        #print("calmar ratio:",self.clmr) 


    def CAGR(self,DF):
        df = DF.copy()
        df["daily_ret"] = DF["CLOSE"].pct_change() #株価終値の前日との変化率を計算する。
        df["cum_return"] = (1 + df["daily_ret"]).cumprod() #cumprod(全要素の累積積を スカラーyに返します.
        n = len(df)/252 #1年の取引日を252日に設定している。   
        CAGR = (df["cum_return"][-1])**(1/n) - 1
        return CAGR


    def max_dd(self,DF):
        "function to calculate max drawdown"
        df = DF.copy()
        df["daily_ret"] = DF["CLOSE"].pct_change()
        df["cum_return"] = (1 + df["daily_ret"]).cumprod()  #cumprod()全要素の掛け算を行う。
        #print(df["cum_return"])

        #ax.legend() #凡例を描写する
        df["cum_roll_max"] = df["cum_return"].cummax()
        df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
        df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
        max_dd = df["drawdown_pct"].max()
        #ax=df["cum_return"].plot(marker="*",figsize=(10, 5))    
        #ax=df["cum_roll_max"].plot(marker="*",figsize=(10, 5))    
        #ax=df["drawdown"].plot(marker="*",figsize=(10, 5))   
        #ax=df["drawdown_pct"].plot(marker="*",figsize=(10, 5))       
        #ax.legend() #凡例を描写する
        return max_dd



#前日株価に対して、本日株価下落率(@c0%の確率を設定の上)を算出するメソッドのクラス
class GETCRITERIA(StockGet):  
    def __init__(self,c0,hosei,stocknum):
     
        super().__init__(stocknum)
        self.c0=c0
        self.hosei=hosei        
        self.get_lowcriteria(self.db_s,self.c0,self.hosei)
  
    #前日株価に対して、本日株価下落率(@c0%の確率を設定の上)を算出する。
    #hoseiは計算上もc0%になるようにデータに補正を加える。
    def get_lowcriteria(self,df0,c0,hosei):


        #データ集計用の行列を用意する。
        mat=[]
        mat = DataFrame(mat, columns=['DIF','DIF2','DIF2SMA'])
        #print("mat")
        #print(mat)

        #最新日の株価CLOSE値読み取り
        latest_close=df0['CLOSE'].iloc[df0['CLOSE'].count()-1]

        #前日の株価CLOSE値読み取り
        yesterday_close=df0['CLOSE'].iloc[df0['CLOSE'].count()-2]
        
        #Close列を1行下にずらす。
        df1=pd.concat([df0['CLOSE'].shift(1),df0['LOW']],axis=1)

        #print("df1")
        #print(df1)

        #前日Close値 と 当日Low値の変化率を取得する。
        mat['DIF']=100*(df1['LOW']/df1['CLOSE']-1)


        #前日Close値 と 当日Low値の変化率の2乗を算出する。
        mat['DIF2']=mat['DIF'] *  mat['DIF']

        #前日と当日の変化率2乗値の移動平均を算出する(Close値)
        mat['DIF2SMA']=mat['DIF2'].rolling(window=10).mean()

        #print("DIF: 前日Close値 と 当日Low値の変化率を取得する。")
        #print("DIF2: 前日と当日の変化率2乗値を算出する(Close値)")
        #BlockingIOErrorprint("DIF2SMA: 前日と当日の変化率2乗値の移動平均を算出する(Close値)。")
        #print(mat)

        #SEABORNを使い時系列グラフを描写する。
        sdf=[]
        sdf = DataFrame(sdf, columns=['DIF','DIF2SMA'])
        sdf['DIF'] = mat['DIF']
        sdf['DIF2SMA'] = mat['DIF2SMA']

        sdf.reset_index(inplace =True) #indexを解除する
        sdf=sdf.drop(columns='DATE') #date列を削除する。
        sdf=sdf.dropna()
        #print("sdf")
        #print(sdf)

        sdflogx=DataFrame([],columns=['DIF','DIF2SMA','CRETERIA','VERIFY'])
        #sdflogx=DataFrame(sdf,columns=['DIF','DIF2SMA'])


        sdflogx['DIF2SMA']=np.log10(sdf['DIF2SMA'])
        sdflogx['DIF']=sdf['DIF']
        #print(sdflogx)        
        #print(sdflogx)
        
        

        df_dif2sma_latest=[]
        new_DIF=sdflogx.iloc[sdflogx['DIF'].count()-1]["DIF"]       
        new_DIF2SMA=sdflogx.iloc[sdflogx['DIF2SMA'].count()-1]["DIF2SMA"]     
        #df_dif2sma_latest=pd.DataFrame([new_DIF,new_DIF2SMA],columns=['DIF','DIF2SMA'])
        df_dif2sma_latest=pd.DataFrame([[new_DIF,new_DIF2SMA]],columns=['DIF','DIF2SMA']) 
        #print("df_dif2sma_latest")
        #print(df_dif2sma_latest)
        
        

        #DataFrame datを行keyを基準に昇順にならべ、小さい順から5グループに分割する。
        datgp=self.datadiv(sdf,"DIF2SMA")  #datgp[0]:(DIF,DIF2SMA)データセットを5グループに分割したもの
                                      #datgp[1]:5グループそれぞれのDIF2SMAの上限値と下限値の中間値を算出したもの


        val= [0] * 10
        #print(val)
        for i,ele in  enumerate(["sdf0","sdf1","sdf2","sdf3","sdf4"]): 

            sdf_list=datgp[0][ele]["DIF"].values.tolist() #DataFarme型をList型に変換する。
    
            #sdf_listに対し、カーネル密度関数を発生させる。
            #また、カーネル密度関数の累積度数を計算し、累積値down,upとなるX値を返す。
            val[i]=self.pdf_kernel(sdf_list,c0,0.9) 


        criteria_dat = [
            [datgp[1]["sdfp0"],val[0]["down"]],
            [datgp[1]["sdfp1"],val[1]["down"]],
            [datgp[1]["sdfp2"],val[2]["down"]],
            [datgp[1]["sdfp3"],val[3]["down"]],
            [datgp[1]["sdfp4"],val[4]["down"]]
        ]    

        D_criteria=pd.DataFrame(criteria_dat,columns=['X','Y'])

        #Dataset 「D_criteria」に対して、説明変数X,従属変数Yとして対数線形回帰係数を算出する。
        regval=self.logreg(D_criteria,"X","Y",hosei)


        df_creteria=self.dat_generate(regval["slope"],regval["intercept"],datgp[1]['sdfs'],datgp[1]['sdfe'])


        sdflogx['CRETERIA']=regval["slope"]*sdflogx['DIF2SMA']+regval["intercept"]

        #グラフ描写を行う。
        #fig,(ax1)=plt.subplots(1,1,sharey=True)
        #ax1=sns.regplot(x="DIF2SMA", y="DIF", data=sdflogx,fit_reg=False)
        #ax1=sns.regplot(x="X", y="Y", data=df_creteria,fit_reg=False)
        #ax1=sns.rugplot(x="DIF2SMA", y="DIF",data=df_dif2sma_latest,fit_reg=False)
        #df_dif2sma_latest.plot(kind="scatter",x="DIF2SMA", y="DIF",s=500,c="yellow",marker="*", alpha=1, linewidths=2,
        #    edgecolors="red",ax=ax1)

        #確率値検証        
        sdflogx['VERIFY'] = sdflogx.apply(lambda x:self.judge(x),axis=1)
        confirmval=sdflogx['VERIFY'].sum()/sdflogx['VERIFY'].count()

 
        #c%下限値を算出する。
        dif_expected=regval['slope']*df_dif2sma_latest["DIF2SMA"][0]+regval['intercept']


        kagenchi=round(latest_close*(1+dif_expected/100),1)

        #self.criteria={"confirmval":confirmval,"ret_val":regval,"df_dif2sma_latest":df_dif2sma_latest,"latest_close":latest_close,"dif_expected":dif_expected,"yesterday_close":yesterday_close,"kagenchi":kagenchi}
        self.criteria={"confirmval":confirmval,"coeff":regval['coeff'],"kagenchi":kagenchi}
        #return [{"confirmval":confirmval,"ret_val":regval}]

    #条件判定関数を定義する。
    def judge(self,x):
        return 1 if x.DIF > x.CRETERIA else 0



    #DataFrame datを行keyを基準に昇順にならべ、小さい順から5グループに分割する。
    def datadiv(self,dat,key):
        dataleng=dat[key].count() #DataFrame datのkey行のデータ長さを求める。
        delta_len=math.floor(dataleng/5) #DataFrame datのkey行のデータ長さを求める。
        df1=dat.sort_values(by=[key], ascending=True) ##DataFrame datを行keyを基準に昇順にならべる。

        #df1を5グループに分ける。
        sdfall={"sdf0":df1[0:delta_len],
                "sdf1":df1[delta_len+1:2*delta_len],
                "sdf2":df1[2*delta_len+1:3*delta_len],
                "sdf3":df1[3*delta_len+1:4*delta_len],
                "sdf4":df1[4*delta_len+1:].dropna()
               }
    
    
        #print(sdfall)
        sdfp= np.zeros((5, 2))
        sdfp[0][0]=sdfall["sdf0"]["DIF2SMA"] .iloc[0]
        sdfp[0][1]=sdfall["sdf0"]["DIF2SMA"] .iloc[sdfall["sdf0"]["DIF2SMA"].count()-1]  
        sdfp0=(sdfp[0][0]+ sdfp[0][1])/2
    
        sdfp[1][0]=sdfall["sdf1"]["DIF2SMA"] .iloc[0]
        sdfp[1][1]=sdfall["sdf1"]["DIF2SMA"] .iloc[sdfall["sdf1"]["DIF2SMA"].count()-1]
        sdfp1=(sdfp[1][0]+ sdfp[1][1])/2
    
        sdfp[2][0]=sdfall["sdf2"]["DIF2SMA"] .iloc[0]  
        sdfp[2][1]=sdfall["sdf2"]["DIF2SMA"] .iloc[sdfall["sdf2"]["DIF2SMA"].count()-1]      
        sdfp2=(sdfp[2][0]+ sdfp[2][1])/2
    
        sdfp[3][0]=sdfall["sdf3"]["DIF2SMA"] .iloc[0]  
        sdfp[3][1]=sdfall["sdf3"]["DIF2SMA"] .iloc[sdfall["sdf3"]["DIF2SMA"].count()-1]    
        sdfp3=(sdfp[3][0]+ sdfp[3][1])/2
    
        sdfp[4][0]=sdfall["sdf4"]["DIF2SMA"] .iloc[0]  
        sdfp[4][1]=sdfall["sdf4"]["DIF2SMA"] .iloc[sdfall["sdf4"]["DIF2SMA"].count()-1]    
        sdfp4=(sdfp[4][0]+ sdfp[4][1])/2
    
   
        sdfpn={"sdfp0":sdfp0,"sdfp1":sdfp1,"sdfp2":sdfp2,"sdfp3":sdfp3,"sdfp4":sdfp4,"sdfs":sdfp[0][0],"sdfe":sdfp[4][1]}    

    
        return [sdfall,sdfpn]




    #datasetを与え、カーネル密度関数を発生させる。また、カーネル密度関数の累積度数を計算し、
    #累積値down,upとなるX値を返す。
    def pdf_kernel(self,dataset,down,up):

        d_max=np.max(dataset)+0.2
        d_min=np.min(dataset)-0.2

        d_kernel = gaussian_kde(dataset) #カーネル密度推定関数を生成する。バンド幅は自動計算されている。

        #積分を行う範囲を指定する：d_minからd_maxの範囲で積分を行う。
        d_xs = np.linspace(d_min, d_max, num=1000)

        #カーネル密度関数の入力(d_xs)と出力(d_ys)を定義している。
        d_ys = d_kernel(d_xs)

        #累積分布関数をd_xsの範囲で積分する。
        d_integral = cumtrapz(d_ys, d_xs)

        #cdf(x) = 0.03となるxを求める。d_integral配列の中で0.03に最も近くなる数値が配列中の何番目に当たるかを算出している。
        idx_d= np.searchsorted(d_integral, down)

        #cdf(x) = 0.9となるxを求める。d_integral配列の中で0.9に最も近くなる数値が配列中の何番目に当たるかを算出している。
        idx_u = np.searchsorted(d_integral, up)


        #グラフ表示を行っている。
        #ax1=plt.plot(d_xs, d_ys, label="KDE")
        #plt.xlim(d_min-1, d_max+1) 

        #累積値5%の範囲を表示
        #plt.fill_between(d_xs[:idx_d], 0, d_ys[:idx_d], facecolor="r", alpha=0.5)


        #累積値90%の範囲を表示
        #plt.fill_between(d_xs[idx_u:], 0, d_ys[idx_u:], facecolor="r", alpha=0.5)

        #凡例を右上に表示
        #plt.legend(loc="upper right")

        pdf_val={"down":d_xs[idx_d],"up":d_xs[idx_u]}
        return pdf_val


    #対数回帰分析
    def logreg(self,datset,keyx,keyy,hosei):
    

        df0=[np.log10(datset[keyx]),datset[keyy]]
        df0=pd.DataFrame(df0)
        df0=df0.T

        # 線形回帰モデル
        clf = linear_model.LinearRegression()

        # 説明変数xに "x1"のデータを使用
        x =df0.loc[:, [keyx]].values

        # 目的変数yに "x2"のデータを使用
        y =df0[keyy].values

        # 予測モデルを作成（単回帰）
        clf.fit(x, y)

        # パラメータ（回帰係数、切片）を抽出
        [a] = clf.coef_
        b = clf.intercept_+ hosei

        ret_val={"slope":a,"intercept":b,"coeff":clf.score(x, y)} 

        return ret_val
    

    def dat_generate(self,slope,inter,xstart,xend):
        xlist = np.linspace(np.log10(xstart), np.log10(xend), num=100)
        #df0=pd.DataFrame(np.log10(xlist),columns=["X"])
        df0=pd.DataFrame(xlist,columns=["X"])   
        #df1=pd.DataFrame(slope*np.log10(xlist)+inter,columns=["Y"])
        df1=pd.DataFrame(slope*xlist+inter,columns=["Y"])
        dfc=pd.concat([df0, df1],axis=1)
        #print(dfc)
  
        return dfc


