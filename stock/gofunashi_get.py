#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import datetime
from time import sleep
from selenium.webdriver.common.by import By
import shutil
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import datetime
import getpass




#pyvirtualdisplayパッケージを使って仮想ディスプレイ（Xvfb）を起動させてSeleniumを使う方法
display = Display(visible=0, size=(1024, 1024))
display.start()

#chromedriverの設定
options = Options() 
options.add_argument('--headless')
options.add_argument('--disable-gpu')



#https://kabutan.jp/stock/kabuka?code=1570


#指定した期間の有価証券報告書を取得するクラス
class KABUTAN_GET():

    #コンストラクタ
    def __init__(self,syokennum,outputcsv):
        
        
        self.syokennum=syokennum
        self.outputcsv=outputcsv
        self.browser = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
        self.browser.get('https://www.monex.co.jp/')
        #self.login() #マネックスサイトにログインする
        #self.gofunashidat_get() #5分足データをスクレイピングする関数
        #self.browser.close()#ブラウザを閉じる  for文の外に書かないとエラーになる 

    #マネックスサイトにログインする
    def login(self):

        ID='183393825'
        #ID='253'
        self.browser.execute_script('document.getElementsByName("loginid")[0].value="%s";' % ID)
        #elem_username = self.browser.find_element_by_name('loginid')     
        #elem_username.send_keys(ID)   
        sleep(3)
        elem_username= self.browser.find_element_by_name('passwd')
        elem_username.send_keys('!fdfpY2020')
        elem_login_btn = self.browser.find_element_by_class_name('btn_login_top')
        elem_login_btn.click()
        sleep(5)

    #銘柄スカウターにログインする    
    def meigarasukauter(self):    
        PATH0='/html/body/div[6]/div/div[2]/div[3]/div/div[4]/ul[1]/li[1]/span'
        elem_checkbox=self.browser.find_element_by_xpath(PATH0)
        elem_checkbox.click()
        urltext=self.browser.find_elements_by_link_text(u"マネックス銘柄スカウター")
        urltext[0].click()
        sleep(3)

    #コンマを削除して、数値型にする関数    
    def conv(self,moji):
        moji=moji.replace(',', '') 
        moji=int(moji)
        return moji    
    

    #5分足データをスクレイピングする関数
    def gofunashidat_get(self):

        num=[0,0,0,0,0,0,0,0]
        hinichi=[]
        openne=[]
        highne=[]
        lowne=[]
        closeme=[]
        volne=[]

        PATH1='/html/body/div[3]/div[1]/div/div[1]/div[2]/div/form[2]/input[2]'
        PATH2='/html/body/div[3]/div[1]/div/div[1]/div[2]/div/form[2]/input[3]'
        PATH3='/html/body/div[2]/div/div[6]/div[2]/div[1]/div/ul/li[5]'
        PATH4='/html/body/div[2]/div/div[6]/div[2]/div[2]/div[1]/div/ul[1]/li[1]'
        sleep(10)
        #テキストボックスに証券番号を入力する。& 虫眼鏡のマークをクリックする。
        #elem_numbox=self.browser.find_element_by_xpath(PATH1)
        self.browser.execute_script('document.getElementsByName("dscr")[0].value="%s";' % str(self.syokennum))
        #elem_numbox.send_keys(str(self.syokennum))
        elem_gomark=self.browser.find_element_by_xpath(PATH2)
        elem_gomark.click()

        
        #時系列のタブをクリックする。& 5分足データ表を表示させる。
        sleep(20)        
        elem_jikeiretsu=self.browser.find_element_by_xpath(PATH3)
        elem_jikeiretsu.click()
        sleep(3)    
        elem_5min=self.browser.find_element_by_xpath(PATH4)
        elem_5min.click()    
        sleep(3)
    
        #5分足データ数値を取得する。    
        for i in range(1,133):
            for j in range(0,7):
                PATH6=' /html/body/div[2]/div/div[6]/div[2]/div[2]/div[2]/table/tbody[3]/tr[' +str(i)+ ']/td[' +str(j+1)+ ']'
                num[j]=str(self.browser.find_element_by_xpath(PATH6).get_attribute('innerHTML')) #数値を取得する。
            hinichi.append(num[0])
            openne.append(self.conv(num[1]))
            highne.append(self.conv(num[2]))
            lowne.append(self.conv(num[3]))
            closeme.append(self.conv(num[4]))
            volne.append(self.conv(num[6]))
            
        #取得した5分足データをDataFrameに格納する。            
        df = pd.DataFrame({'DATE':hinichi,'OPEN':openne,'HIGH':highne,'LOW':lowne,'CLOSE':closeme,'VOL':volne})
        #print(df)
        tmp=pd.read_csv(str(self.outputcsv), index_col=0,parse_dates=True)
        tmp.reset_index("DATE",inplace=True) #DATE列のindexを解除
        newdf=pd.merge(df, tmp, how="outer")
        newdf.set_index("DATE",inplace=True)      
        newdf.to_csv(str(self.outputcsv))
        shutil.copyfile(str(self.outputcsv), 'cp' + str(self.outputcsv))
        #print(newdf)
  
        sleep(2)   


##################   MAIN ##################   

SYOKENNUM='1570'
OUTPUTCSV='1570_5min.csv'
    
    
def main():
    
    try:
        #print(getpass.getuser())
        print("START" + str(datetime.datetime.today()))
        with open('log.txt','a') as f:
            f.write("\n" + "START " + str(datetime.datetime.today()))       
        gofunashi=GOFUNASHI_GET(SYOKENNUM,OUTPUTCSV)
        gofunashi.login() #マネックスサイトにログインする
        gofunashi.gofunashidat_get() #5分足データをスクレイピングする関数
        gofunashi.browser.close()#ブラウザを閉じる  for文の外に書かないとエラーになる
        print("FINIST" + str(datetime.datetime.today()))
        with open('log.txt','a') as f:
            f.write("\n" + "FINISH " + str(datetime.datetime.today()))
     
    except Exception as e:

        with open('log.txt','a') as f:
            f.write("ERROR" + str(datetime.datetime.today()))                
    
if __name__ == "__main__":
    main()  