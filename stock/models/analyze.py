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



setting.HOME_PATH=setting.HOME_PATH if os.path.exists(setting.HOME_PATH) else setting.HOME_PATH_LOCAL
setting.GET_STOCK_F=setting.GET_STOCK_F if os.path.exists(setting.GET_STOCK_F) else setting.GET_STOCK_F_LOCAL




class StockGetTop(object):
    def __init__(self, stocknum = None):
        self.stocknum = stocknum
        self.Y = datetime.datetime.today().year
        self.M = datetime.datetime.today().month
        self.D = datetime.datetime.today().day

class StockGet(StockGetTop):
    def __init__(self, stocknum = None):
        super().__init__(stocknum)
        get_stock_f = setting.GET_STOCK_F

        if get_stock_f == 0:
            
            filepath=setting.HOME_PATH + str(self.stocknum) + ".csv"

            #str(self.stocknum)が数値型の場合
            if str(self.stocknum).isnumeric()==True or str(self.stocknum)=='USDJPY':
                #過去に銘柄の株価を取得したデータが存在する場合
                if os.path.exists(filepath)==True :
                    #指定した銘柄についてすでに取得した株価データをcsvファイルより読み出す。                
                    self.pre_db_s = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".csv", index_col=0) #index_col=0は列名もデータと一緒に取り出す。   
     
                    #self.pre_db_s = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".csv")    
                    #print("self.pre_db_s") 
                    #print(self.pre_db_s)                  
                    #self.pre_db_sw = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".week.csv", index_col=0)    #index_col=0は列名もデータと一緒に取り出す。
        
                    #print("self.pre_db_s")
                    #print(self.pre_db_s)     
                    #print("self.predb_s.tail(1)[Date][0]")             
                    #print(self.pre_db_s.tail(1)) #最新の株価の日付を取得する
                    #print(self.pre_db_s.tail(1)["Date"][0]) #最新の株価の日付を取得する            
                    #self.update_day=self.pre_db_s.tail(1)["DATE"][0] #csvファイルに記録された最新の株価の日付を取得する
                    self.update_day=self.pre_db_s.tail(1)  #csvファイルに記録された最新の株価の日付を取得する


                else :
                    #新規の銘柄の場合は、全期間の株価を取得する。
                    self.stockgetdayjsm(datetime.date(self.Y-2, self.M, self.D),datetime.date(self.Y, self.M, self.D), self.stocknum)
                    self.stockgetweekjsm(datetime.date(self.Y-2, self.M, self.D),datetime.date(self.Y, self.M, self.D), self.stocknum)             
                    self.pre_db_s = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".csv", index_col=0)  
              
                    #self.pre_db_s = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".csv", index_col=1, parse_dates=True , names=["Date"])    
                    #self.pre_db_s = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".csv")      
                    #self.pre_db_sw = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".week.csv", index_col=0) 
       
                    #self.pre_db_sw = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".week.csv", index_col=1, parse_dates=True , names=["Date"])        
                    #既存銘柄はcsvファイルを読み出しているので、新規銘柄も同じ形式にしたいのでcsvにダンプしてcsvで読み出すことにした。20190923          
                    ##self.pre_db_s=self.db_s
                    ##self.pre_db_sw=self.db_sw
                    #print("self.pre_db_s")
                    #print(self.pre_db_s)     
                    #print("self.predb_s.tail(1)[Date][0]")             
                    ##print(self.pre_db_s.tail(1)["Date"][0]) #最新の株価の日付を取得する
                    #print(self.pre_db_s.tail(1)["Date"][0]) #最新の株価の日付を取得する            
                    self.update_day=self.pre_db_s.tail(1) #csvファイルに記録された最新の株価の日付を取得する


                #self.update_day.index[0]が文字列であれば日付型に変更する。self.update_day.index[0]が日付型であればそのままにする
                dt = datetime.datetime.strptime(self.update_day.index[0], '%Y-%m-%d')
            
                #index(日付)を取り出し日付の形式変換
                ##dt = datetime.datetime(self.update_day.index[0], '%Y-%m-%d') #index(日付)を取り出し日付の形式変換            
                self.SY=dt.year #dt(最新の株価の日付)の年を取得
                self.SM=dt.month #dt(最新の株価の日付)の月を取得
                self.SD=dt.day #dt(最新の株価の日付)の日を取得
                #print("self.SY")        
                #print(self.SY)
                #print("self.SM")        
                #print(self.SM)     
                #print("self.SD")            
                #print(self.SD) 

                #db_sのindex列を削除する。以降のcodeと合わせるため
                self.db_s = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".csv", index_col=0)#index_col=0は列名もデータと一緒に取り出す。
                #self.db_sw = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".week.csv", index_col=0)#index_col=0は列名もデータと一緒に取り出す。
                #print("self.db_s")
                #print(self.db_s)


                #self.stockgetdayjsm(datetime.date(self.Y-1, self.M, self.D),datetime.date(self.Y, self.M, self.D), self.stocknum)
                #株価データ差分を取得する(日足)
                self.stockgetdayjsm(datetime.date(self.SY, self.SM, self.SD),datetime.date(self.Y, self.M, self.D), self.stocknum)
                #self.stockgetweekjsm(datetime.date(self.Y-2, self.M, self.D),datetime.date(self.Y, self.M, self.D), self.stocknum)
                #株価データ差分を取得する(週足)
                #self.stockgetweekjsm(datetime.date(self.SY, self.SM, self.SD)- datetime.timedelta(days=7),datetime.date(self.Y, self.M, self.D), self.stocknum)



            #str(self.stocknum)が英文字の場合
            elif  str(self.stocknum).isnumeric()==False:



                start=datetime.datetime(self.Y-2, self.M, self.D)
                end=datetime.datetime(self.Y, self.M, self.D)
                df=web.DataReader(str(self.stocknum),'yahoo',start,end) #バンガード S&P500 VALUE
                self.update_day=df.tail(1)
                #print(df)
                #print(self.update_day.index[0].date())  
                df=df.drop(columns='Adj Close') #列Aを削除する。
                df.to_csv(setting.HOME_PATH + str(self.stocknum) + ".csv",header=False) #dfを外部のcsvファイルに書き込む 
                #df.to_csv(setting.HOME_PATH + str(self.stocknum) +".week.csv",header=True) #ダミーデータ

                ##print("self.update_day")
                ##print(type(self.update_day.index[0])) #index(日付)を取り出す





                dt = self.update_day.index[0]
            
                #index(日付)を取り出し日付の形式変換
                ##dt = datetime.datetime(self.update_day.index[0], '%Y-%m-%d') #index(日付)を取り出し日付の形式変換            
                self.SY=dt.year #dt(最新の株価の日付)の年を取得
                self.SM=dt.month #dt(最新の株価の日付)の月を取得
                self.SD=dt.day #dt(最新の株価の日付)の日を取得
                #print("self.SY")        
                #print(self.SY)
                #print("self.SM")        
                #print(self.SM)     
                #print("self.SD")            
                #print(self.SD) 

                #db_sのindex列を削除する。以降のcodeと合わせるため
                self.db_s = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".csv", index_col=0,names=["DATE","HIGH","LOW","OPEN","CLOSE","VOL"])#index_col=0は列名もデータと一緒に取り出す。
                #self.db_sw = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".week.csv", index_col=0)#index_col=0は列名もデータと一緒に取り出す。
                self.db_s.to_csv(setting.HOME_PATH + str(self.stocknum) + ".csv",header=True) #ヘッダーの表示を更新して再度csvファイルにデータを書き出す 
                #print("self.db_s")
                #print(self.db_s)


 
        elif get_stock_f == 1:
            #print(setting.HOME_PATH + str(self.stocknum) + ".csv")
            self.db_s = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".csv", index_col=0, parse_dates=True , names=["Stock"])
            #print(self.db_s)
            #self.db_sw = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".week.csv", index_col=0, parse_dates=True,
            #                names=["Stock"])




    def stockgetdayjsm(self, start_date, end_date, stock_num):
        q = jsm.Quotes()
        stock = q.get_historical_prices(stock_num, jsm.DAILY, start_date, end_date)  # 指定期間、指定銘柄の株価取得
        date_stock = [data.date.date() for data in stock]  # 日付の取得(date()で時刻の情報を削除している)  
        open_stock = [data.open for data in stock]  # 始値の取得
        high_stock = [data.high for data in stock]  # 高値の取得
        low_stock = [data.low for data in stock]  # 低値の取得
        close_stock = [data.close for data in stock]  # 終値の取得
        volume_stock = [data.volume for data in stock]  # 出来高の取得         
        db_s=pd.DataFrame([date_stock,close_stock,open_stock,high_stock,low_stock,volume_stock]).T   # 日付,始値,高値,低値,終値,出来高のマトリックスの作成
        db_s.columns = ['DATE','CLOSE','OPEN','HIGH','LOW','VOL']       
        db_s=db_s.set_index('DATE') # DATE列をindexに指定する  
        self.add_db_s=db_s.sort_index() # DATE列で古い順番に並べる
        #print("add_db_s")
        #print(self.add_db_s)  
        #self.add_db_s=self.add_db_s(axis='index')
        #self.add_db_s = DataFrame(self.add_db_s, columns=['Stock'])  #列名'Stock'を付与する。
        #print("self.db_s")
        #print(self.db_s)

        #(try-catch)新規の銘柄の場合はself.db_sが存在しないため、except以降の処理:self.db_s=self.add_db_sとする
        try:
            #print("self.add_db_s")
            #print(self.add_db_s) 
            #print(self.db_s)  
            self.db_s=self.db_s.append(self.add_db_s) #既存の株価に新規に追加した株価を追加する    
            #print("self.db_s") 
            #print(self.db_s)     
            #print("d0")                      
            #self.db_s = self.db_s.drop_duplicates().sort_index()    #重複行があれば削除する & 日付が古い順番にデータを並べ替える
            self.db_s = self.db_s.drop_duplicates()    #重複行があれば削除する (sort_index()はエラーが出るため削除)
            #print("d1")    
            #print("self.db_s gb")
            #print(self.db_s)

        except AttributeError: 
            self.db_s=self.add_db_s


        #print("self.db_s")         
        #print(self.db_s)    



        self.db_s.to_csv(setting.HOME_PATH + str(stock_num) + ".csv",header=True) #headerなしでcsvファイルに書き出し
        return self.db_s


    def stockgetweekjsm(self,start_date,end_date,stock_num):
        q = jsm.Quotes()
        stock = q.get_historical_prices(stock_num, jsm.WEEKLY, start_date, end_date)   #指定期間、指定銘柄の株価取得
        open_stock = [data.open for data in stock]  # 始値の取得
        high_stock = [data.high for data in stock]  # 高値の取得
        low_stock = [data.low for data in stock]  # 低値の取得
        close_stock = [data.close for data in stock]  # 終値の取得
        volume_stock = [data.volume for data in stock]  # 出来高の取得   
        date_stock = [data.date.date() for data in stock]  # 日付の取得(date()で時刻の情報を削除している)
        db_sw = pd.DataFrame([date_stock,close_stock,open_stock,high_stock,low_stock,volume_stock]).T   # 日付,始値,高値,低値,終値,出来高のマトリックスの作成
        db_sw.columns = ['DATE','CLOSE','OPEN','HIGH','LOW','VOL']
        db_sw=db_sw.set_index('DATE') # DATE列をindexに指定する  
        self.add_db_sw=db_sw.sort_index() # DATE列で古い順番に並べる


       #(try-catch)新規の銘柄の場合はself.db_sが存在しないため、except以降の処理:self.db_sw=self.add_db_swとする        
        try:     
            self.db_sw=self.db_sw.append(self.add_db_sw) #既存の株価に新規に追加した株価を追加する
            #print("check000")
            #self.db_sw=self.db_sw.drop_duplicates().sort_index()      #重複行があれば削除する & 日付が古い順番にデータを並べ替える
            self.db_sw=self.db_sw.drop_duplicates()      #重複行があれば削除する (sort_index()はエラーが出るため削除)
            #print("self.db_sw")
            #print(self.db_sw)           
        except AttributeError:
            self.db_sw=self.add_db_sw

        #self.db_sw.to_csv(setting.HOME_PATH + str(stock_num) +".week.csv",header=True)
        return self.db_sw




class Technical(StockGet):  #銘柄の株価よりテクニカル分析計算を行う。
    def __init__(self,stocknum):
        super().__init__(stocknum)
        #print("self.db_s")
        #print(self.db_s)        
        self.kabuka_get(self.db_s) #銘柄の本日の株価と昨日との差を求める。
        self.vol_get(self.db_s)   #株価のshigma値を取得する。     
        self.ichimoku(self.db_s) #一目均衡表
        self.bolinger(self.db_s)
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
        #rint(self.today_kabuka)  
        #print("dif_kabuka")
        #print(self.dif_kabuka)  

    def future_day(self, today,d): #todayのd日後の日付を算出する。
        return datetime.date(today.year, today.month, today.day)+datetime.timedelta(days=d)


    def ichimoku(self, mat): #一目均衡表を計算する。
        #print(mat)
        vec = []
        today = datetime.datetime.strptime(str(mat.index[len(mat.index)-1]), '%Y-%m-%d') #最新の日付を算出する
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
        ma_boli['B_STV'] = ma_boli['CLOSE'].rolling(window=setting.M_IDOU, center=False).std()
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
                     "baseline"    : today_boli['MA_M'][0]
                     }
    
        #print(today_sig)


        if stock_now < today_sig["today_n3sig"] :
            self.band="σ<-3"
        elif  today_sig["today_n3sig"]<= stock_now and stock_now < today_sig["today_n2sig"] :
            self.band="-3<=σ<-2"
        elif  today_sig["today_n2sig"]<= stock_now and stock_now < today_sig["today_n1sig"] :
            self.band="-2<=σ<-1"
        elif  today_sig["today_n1sig"]<= stock_now and stock_now < today_boli['MA_M'][0] :
            self.band="-1<=σ< 0"
        elif  today_boli['MA_M'][0]<= stock_now    and stock_now < today_sig["today_p1sig"] :
            self.band="0<=σ<1"
        elif  today_sig["today_p1sig"]<= stock_now and stock_now < today_sig["today_p2sig"] :
            self.band="1<=σ<2"
        elif  today_sig["today_p2sig"]<= stock_now and stock_now < today_sig["today_p3sig"] :
            self.band="2<=σ<3" 
        elif  today_sig["today_p3sig"]<= stock_now :
            self.band="σ<=3"

        


    def combine(self): #DBCONTオブジェクトに渡す変数をまとめる。

        self.comb = {"stocknum" :self.stocknum,
                     "today_kabuka" :self.today_kabuka,
                     "dif_kabuka" :self.dif_kabuka,
                     "band":self.band,
                     "p1sig":self.stock_p1sig, 
                     "p05sig":self.stock_p05sig,
                     "n1sig":self.stock_n1sig,
                     "n05sig":self.stock_n05sig,
                     "meigara_sta":self.meigara_sta,
                     "tenkansen" :self.today_tenkansen
        }

                    

        #print("self.comb")
        #print(self.comb)



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


