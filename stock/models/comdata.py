from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import io
import sys
import csv
import pandas as pd


#'ascii' codec can't encode characters in position 0-6: ordinal not in range(128)エラー対策実施
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') 
#sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')



#chromedriverの設定
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1024,768')
options.add_argument('--disable-dev-shm-usage')    


    

class CTRL():

    def __init__(self,CSV_FILEPATH):
    
        self.CSV_FILEPATH=CSV_FILEPATH   

    
    ########## 米10年金利取得 ###########################
    
    def get_kinri(self):

        browser = webdriver.Chrome(options=options,executable_path="/usr/bin/chromedriver") # Chromeを準備(optionでブラウザ立ち上げ停止にしている)
        URL='https://m.finance.yahoo.co.jp/stock?code=%5ETNX&d=1w'
        browser.get(URL)  #サイトを開く。ブラウザ自体は立ち上げない
        self.USAyield10 = browser.find_element_by_class_name('priceFin') #米国10年金利を取得
        xpath='//*[@id="detail-module"]/div/ul/li[2]/dl/dd'
        self.delta=browser.find_element_by_xpath(xpath) #米国10年金利(前日差)を取得
        self.tmp0={ "yield10":[self.USAyield10.text],"yield_delta":[self.delta.text]}
        browser.close() #これがないと実行するたびにchromedriverのプロセスが蓄積しメモリを圧迫する。
        browser.quit() #これがないと実行するたびにchromedriverのプロセスが蓄積しメモリを圧迫する。

    ########## 原油取得 ###########################

    def get_genyu(self):

        browser = webdriver.Chrome(options=options,executable_path="/usr/bin/chromedriver") # Chromeを準備(optionでブラウザ立ち上げ停止にしている)
        URL='https://www.trkd-asia.com/rakutensecj/indx.jsp?ind=4&ric=0'
        browser.get(URL)  #サイトを開く。ブラウザ自体は立ち上げない
        xpath='//*[@id="cCommoditites"]/table/tbody/tr[1]/td/em'
        self.genyu=browser.find_element_by_xpath(xpath) #原油価格の取得
        xpath1='//*[@id="cCommoditites"]/table/tbody/tr[2]/td[1]/span'
        self.genyu_upval = browser.find_element_by_xpath(xpath1) #原油価格(前日差)の取得
        self.tmp1={ "genyu":[self.genyu.text],"genyu_delta":[self.genyu_upval.text]}
        browser.close() #これがないと実行するたびにchromedriverのプロセスが蓄積しメモリを圧迫する。
        browser.quit() #これがないと実行するたびにchromedriverのプロセスが蓄積しメモリを圧迫する。

    ########## 日経平均EPS取得 ###########################

    def get_nikkeieps(self):


        browser = webdriver.Chrome(options=options,executable_path="/usr/bin/chromedriver") # Chromeを準備(optionでブラウザ立ち上げ停止にしている)

        URL='https://nikkei225jp.com/data/per.php'
        browser.get(URL)  #サイトを開く。ブラウザ自体は立ち上げない
        xpath= '//*[@id="datatbl"]/tbody/tr[2]/td[7]'
        company_eps=browser.find_element_by_xpath(xpath) #EPSint(str.replace(‘,’, ”))
        self.tmp2={"nikkei_eps":company_eps.text.replace(",", "")}
        browser.close() #これがないと実行するたびにchromedriverのプロセスが蓄積しメモリを圧迫する。
        browser.quit() #これがないと実行するたびにchromedriverのプロセスが蓄積しメモリを圧迫する。        
            


     ########## 一連の作業を実施する関数 ###########################

    def allproc(self):
        
        #self.get_kinri()
        self.get_genyu()
        self.get_nikkeieps()        
        #kinribox=self.tmp0 #米国10年金利情報
        kinribox={ "yield10":"0.1","yield_delta":"0.1"} #Dummy
        genyubox=self.tmp1 #原油価格情報
        nikkeieps=self.tmp2 #日経225EPS
        kinribox.update(genyubox)  #辞書型配列の結合
        kinribox.update(nikkeieps)
        df = pd.DataFrame(kinribox) #データをMatrixに格納する
        df.to_csv(self.CSV_FILEPATH) #dfの内容をcsvファイルに書き出す。
        #print(df)

#print("AAA")
CSV_KAKUSYUPATH='/home/pi/dcshare/stock/kakusyudat.csv'
#CSV_KAKUSYUPATH='/home/stock/kakusyudat.csv'
test= CTRL(CSV_KAKUSYUPATH)
test.allproc()




    
