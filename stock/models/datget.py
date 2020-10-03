#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import datetime
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
import os.path
import pandas_datareader.data as web #米国株データの取得ライブラリを読み込む



####(1)取得する株価番号,取得基準年を記載します。#######

#STOCKNUMS=[4800,1570,'^N225','VOOV','^DJI','JPY=X']   #取得する株価番号を入力します。
STOCKNUMS=[4800]
YEAR=2020 #取得基準年を記入します。取得基準年から過去2年分の株価データを取得します。

####(2)chromedriverの設定を行います。#######

options = Options() 
options.add_argument('--headless')
options.add_argument('--disable-gpu')

####(3)X環境がない(コンソール上で実施)場合、下記を有効にする#######

#pyvirtualdisplayパッケージを使って仮想ディスプレイ（Xvfb）を起動させてSeleniumを使う方法
display = Display(visible=0, size=(1024, 1024))
display.start()


####(4) 各種フォルダの設定を行います ##############

EXECUTABLE_PATH="/usr/bin/chromedriver"  #/chromedriver.exeのパスを指定する。
HOME_PATH="/home/pi/dcshare/stock/models/"  #株価データを取得するディレクトリを設定します。



class GET_KABUDATA():


    def __init__(self,stocknum,year):
    
        stocknum=str(stocknum)
        self.year=year
        
        
        try:
            print('銘柄番号' + str(stock)+'の株価データを取得します')
            if os.path.exists(HOME_PATH + str(stocknum)+'.csv')==False:

                if stocknum.isnumeric()==False:
                    self.get_PandasDR(stocknum)
            
                else:
                    self.get_new_stockdat(stocknum,year)
            
            else:
                if str(stocknum).isnumeric()==False:
                    self.get_PandasDR(stocknum)
            
                else:
                    self.get_add_stockdat(stocknum,year)

            print('銘柄番号' + str(stock)+'の株価データ取得を完了しました')
            print('**********')
            
        except Exception as e:
            print(e)
            print('株価取得失敗')                
                
                
                
    def get_add_stockdat(self,stocknum,year):
        
        s_date=[]
        s_open=[]
        s_high=[]
        s_low=[]
        s_close=[]
        s_volume=[]
        dfstock=[]
        add_s_date=[]
        add_s_open=[]
        add_s_high=[]
        add_s_low=[]
        add_s_close=[]
        add_s_volume=[]  
        add_s_stock=[] 
        add_dfstock=[]       
        
        
        browser = webdriver.Chrome(options=options,executable_path=EXECUTABLE_PATH)
        url='https://kabuoji3.com/stock/'+ str(stocknum) + '/'+ str(year) + '/'
        browser.get(url)
        elem_tmp0 = browser.find_element_by_class_name('data_contents')
        elem_tmp1 = elem_tmp0.find_element_by_class_name('data_block')
        elem_tmp2 = elem_tmp1.find_element_by_class_name('data_block_in')
        elem_tmp3 = elem_tmp2.find_element_by_class_name('table_wrap')
        elem_table= elem_tmp3.find_element_by_class_name('stock_table.stock_data_table')
        elem_table_kabuka=elem_table.find_elements(By.TAG_NAME, "tbody")

        for i in range(0,len(elem_table_kabuka)):
    
            kabudat=elem_table_kabuka[i].text.split()   
            s_date.append(str(kabudat[0].split('-')[0]) +'/'+ str(kabudat[0].split('-')[1]) +'/'+ str(kabudat[0].split('-')[2]))     
            s_open.append(kabudat[1])
            s_high.append(kabudat[2])
            s_low.append(kabudat[3])
            s_close.append(kabudat[4])
            s_volume.append(kabudat[5])
            s_stock={'DATE':s_date,'CLOSE':s_close,'OPEN':s_open,'HIGH':s_high,'LOW':s_low,'VOL':s_volume}        
        
        dfstock=pd.DataFrame(s_stock,columns=["DATE","CLOSE","OPEN","HIGH","LOW","VOL"]) #今年度の株価データをスクレイピングする。 
        dfstock=dfstock.sort_index() #取得した株価データを日付順に並べる。

        #print("dfstock")        
        #print(dfstock)  
        
        
        
        dfstock_csv= pd.read_csv(HOME_PATH + str(stocknum)+'.csv', index_col=0) #サーバーに保存している株価データをcsvファイルから読み出す。
        dfstock_csv.reset_index("DATE",inplace=True) 
        

        #サイトから新規にスクレイピングした株価情報の最新の日付を取得する
        dfstock_latest = dfstock['DATE'].iloc[dfstock['DATE'].count()-1]
        dfstock_latest=datetime.datetime.strptime(dfstock_latest, '%Y/%m/%d')
        dfstock_latest_date=datetime.date(dfstock_latest.year, dfstock_latest.month, dfstock_latest.day)
        
        
        
        #サーバーに保存されている株価情報の最新の日付を取得する。  
        dfstock_csv_latest = dfstock_csv['DATE'].iloc[dfstock_csv['DATE'].count()-1]
        dfstock_csv_latest=datetime.datetime.strptime(dfstock_csv_latest, '%Y/%m/%d')
     

        dfstock_latest_date =datetime.date(dfstock_latest_date.year, dfstock_latest_date.month, dfstock_latest_date.day)  
        dfstock_csv_latest_date =datetime.date(dfstock_csv_latest.year, dfstock_csv_latest.month, dfstock_csv_latest.day)
      
        difday=dfstock_latest_date - dfstock_csv_latest_date
        #print(difday.days)

       
        
        for i in range(len(elem_table_kabuka)+1-difday.days,len(elem_table_kabuka)):
            

            kabudat=elem_table_kabuka[i].text.split()   
            add_s_date.append(str(kabudat[0].split('-')[0]) +'/'+ str(kabudat[0].split('-')[1]) +'/'+ str(kabudat[0].split('-')[2]))     
            add_s_open.append(kabudat[1])
            add_s_high.append(kabudat[2])
            add_s_low.append(kabudat[3])
            add_s_close.append(kabudat[4])
            add_s_volume.append(kabudat[5])
            add_s_stock={'DATE':add_s_date,'CLOSE':add_s_close,'OPEN':add_s_open,'HIGH':add_s_high,'LOW':add_s_low,'VOL':add_s_volume} 
            

        
        add_dfstock=pd.DataFrame(add_s_stock,columns=["DATE","CLOSE","OPEN","HIGH","LOW","VOL"])    
        #print("add_dfstock")
        #print(add_dfstock)       
        #print("dfstock")      
        #print(dfstock)    
        #print("dfstock_csv") 
        #print(dfstock_csv) 
        
        #dfstock=dfstock.set_index("DATE",inplace=True)
        #add_dfstock=add_dfstock.set_index("DATE",inplace=True)
        
        dfstock=pd.concat([dfstock_csv, add_dfstock])  
        #print("dfstock")           
        #print(dfstock)    
        dfstock.set_index("DATE",inplace=True)
        dfstock.to_csv(HOME_PATH + str(stocknum)+'.csv')
        
        
        browser.close()#ブラウザを閉じる  for文の外に書かないとエラーになる         
        
        
        
        
        
    def get_new_stockdat(self,stocknum,year):
        
        s_date=[]
        s_open=[]
        s_high=[]
        s_low=[]
        s_close=[]
        s_volume=[]
        dfstock=[]
        browser = webdriver.Chrome(options=options,executable_path=EXECUTABLE_PATH)
        for j in range(0,3):
            url='https://kabuoji3.com/stock/'+ str(stocknum) + '/'+ str(year-j) + '/'
            browser.get(url)
            elem_tmp0 = browser.find_element_by_class_name('data_contents')
            elem_tmp1 = elem_tmp0.find_element_by_class_name('data_block')
            elem_tmp2 = elem_tmp1.find_element_by_class_name('data_block_in')
            elem_tmp3 = elem_tmp2.find_element_by_class_name('table_wrap')
            elem_table= elem_tmp3.find_element_by_class_name('stock_table.stock_data_table')
            elem_table_kabuka=elem_table.find_elements(By.TAG_NAME, "tbody")

            for i in range(0,len(elem_table_kabuka)):
    
                kabudat=elem_table_kabuka[i].text.split()   
                s_date.append(str(kabudat[0].split('-')[0]) +'/'+ str(kabudat[0].split('-')[1]) +'/'+ str(kabudat[0].split('-')[2]))     
                s_open.append(kabudat[1])
                s_high.append(kabudat[2])
                s_low.append(kabudat[3])
                s_close.append(kabudat[4])
                s_volume.append(kabudat[5])
                s_stock={'DATE':s_date,'CLOSE':s_close,'OPEN':s_open,'HIGH':s_high,'LOW':s_low,'VOL':s_volume}

                
        dfstock=pd.DataFrame(s_stock,columns=["DATE","CLOSE","OPEN","HIGH","LOW","VOL"])
        dfstock.set_index("DATE",inplace=True)
        dfstock=dfstock.sort_index() #取得した株価データを日付順に並べる。
        dfstock.to_csv(HOME_PATH + str(stocknum)+'.csv')

        browser.close()#ブラウザを閉じる  for文の外に書かないとエラーになる 

        
 


    def get_PandasDR(self,stocknum):
        ed=datetime.datetime.now()
        st=datetime.datetime.now()- datetime.timedelta(days=600)        
        df=web.DataReader(stocknum, 'yahoo',st,ed) #日経225の株価データを取得する
        df=df.drop(columns='Adj Close') #列Aを削除する。
        df.reset_index("Date",inplace=True)
        df= df.rename(columns={'Date': 'DATE','High': 'HIGH', 'Low': 'LOW',  'Open': 'OPEN', 'Close': 'CLOSE',  'Volume': 'VOL' })#各列名を所望の列名に変更する。
        df = df[['DATE','CLOSE','HIGH','LOW','OPEN','VOL']]
        df.set_index("DATE",inplace=True)
        df.to_csv(HOME_PATH + str(stocknum)+'.csv') #dfを外部のcsvファイルに書き込む 
        
        
        
 
        
for stock in STOCKNUMS:
    

    GET_KABUDATA(stock,YEAR)


print('株価取得終了しました。')
