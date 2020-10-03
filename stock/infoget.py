#-*- coding:utf-8 -*-
###### ブラウザを立ち上げない処理を行うコード  #########################################
from selenium import webdriver              # Webブラウザを自動操作する（python -m pip install selenium)
#import chromedriver_binary                  # パスを通すためのコード
from selenium.webdriver.chrome.options import Options # オプションを使うために必要
option = Options()                          # オプションを用意
option.add_argument('--headless')           # ヘッドレスモードの設定を付与
########################################################################################

import pandas as pd
import time

CODEs=5997

browser = webdriver.Chrome(options=option,executable_path="/usr/lib/chromium-browser/chromedriver") # Chromeを準備(optionでブラウザ立ち上げ停止にしている）
URL='https://kabutan.jp/stock/?code= '+ str(CODEs)
browser.get(URL)  #サイトを開く。ブラウザ自体は立ち上げない。
xpath='//*[@id="kobetsu_right"]/div[4]/table/tbody'
xpath1='//*[@id="kobetsu_right"]/div[3]/table/tbody/tr[3]'
company_eps=browser.find_element_by_xpath(xpath1 + '/td[4]') #EPS
company_haitoub=browser.find_element_by_xpath(xpath1 + '/td[5]') #配当
company_gaiyo=browser.find_element_by_xpath(xpath + '/tr[3]/td') #会社概要
company_url=browser.find_element_by_xpath(xpath + '/tr[2]/td') #会社URL
print(company_url)
browser.close()