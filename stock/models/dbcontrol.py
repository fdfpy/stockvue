#-*- coding:utf-8 -*-
import os
import pathlib
import pandas as pd
import setting
import sqlite3
import csv
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')



#★★  銘柄パラメータを増やすときに追記する箇所★★★ 2020/12 add
CSV_COLUMNS = ['STOCK_NUM', 'TODAY', 'DIF','C_NAME','EPS','BAND','P1SIG','P05SIG','N1SIG',
'N05SIG','HAITOUB','HOLD','MEIGARA_STA','TENKAN','CONFVAL0','CONFVAL1','CONFVAL2','COEFF0',
'COEFF1','COEFF2','KAGENCHI0','KAGENCHI1','KAGENCHI2',
'SAR','STA','SRATIO','CRATIO','AR'
]
#★★★★★★★★★★★★★★★★★★ 

#self.comb = [self.stocknum,self.today_kabuka,self.dif_kabuka]
class DBCONT(object):

    def __init__(self, data):
        #self.stocknum = stocknum
        #print("DBCOMT data")
        #print(data)
        self.csv_file = setting.CSV_FILE_PATH if os.path.exists(setting.CSV_FILE_PATH) else setting.CSV_FILE_PATH_LOCAL
        self.csv_cyu_file=setting.CSV_CYU_DB_PATH if os.path.exists(setting.CSV_CYU_DB_PATH) else setting.CSV_CYU_DB_PATH_LOCAL
        self.db_path = setting.DB_PATH  if os.path.exists(setting.DB_PATH) else setting.DB_PATH_LOCAL
        self.csv_db_path = setting.CSV_DB_PATH  if os.path.exists(setting.CSV_DB_PATH) else setting.CSV_DB_PATH_LOCAL
        self.csv_cyu_db_path = setting.CSV_CYU_DB_PATH  if os.path.exists(setting.CSV_CYU_DB_PATH) else setting.CSV_CYU_DB_PATH_LOCAL

        #★★ STEP2 of ★★★ 銘柄パラメータを増やすときに追記する箇所★★★ 

        stock_num=data['stocknum']
        today=data['today_kabuka']
        dif=data['dif_kabuka']
        band=data['band']
        p1sig=data['p1sig']
        p05sig=data['p05sig']
        n1sig=data['n1sig']
        n05sig=data['n05sig']
        meigara_sta=data['meigara_sta']
        tenkan=data['tenkansen']
        confval0=data['cri0']['confirmval']
        confval1=data['cri1']['confirmval']
        confval2=data['cri2']['confirmval']
        coeff0=data['cri0']['coeff']
        coeff1=data['cri1']['coeff']
        coeff2=data['cri2']['coeff']
        kagenchi0=data['cri0']['kagenchi']
        kagenchi1=data['cri1']['kagenchi']
        kagenchi2=data['cri2']['kagenchi']
        sar=data['para_sar']
        sta=data['para_status']
        sratio=data['sharp_ratio']
        cratio=data['culmar_ratio']
        ar=data['ar'] #2020/12 add
        # confval0=1
        # confval1=1
        # confval2=1
        # coeff0=1
        # coeff1=1
        # coeff2=1
        # kagenchi0=1
        # kagenchi1=1
        # kagenchi2=1



        #★★★★★★★★★★★★★★★★★★ 

         #USDJPYを取得したときは銘柄番号を9999に戻す
        if stock_num==str('USDJPY') :
            stock_num=str(9999)
        

        #DBへの書き込みを行う。
        self.dbkakikomi(str(stock_num),
                         today, 
                         dif,
                         band,
                         p1sig,p05sig,n1sig,n05sig,
                         meigara_sta,
                         tenkan,
                         confval0,confval1,confval2,
                         coeff0,coeff1,coeff2,
                         kagenchi0,kagenchi1,kagenchi2,
                         sar,sta,sratio,cratio,ar #add 2020/12 add
                         ) 


    def dbkakikomi(self,stock_num,today,dif,band,p1sig,p05sig,n1sig,n05sig,meigara_sta,tenkan,confval0,confval1,confval2,coeff0,coeff1,coeff2,kagenchi0,kagenchi1,kagenchi2,sar,sta,sratio,cratio,ar):  #各銘柄のボラティリティーをDBに追加する関数 2020/12 add
        con = sqlite3.connect(self.db_path)
        #print("self.db_path")
        #print(self.db_path)
        con.text_factory = str
        cur = con.cursor()

        #★★★ 銘柄パラメータを増やすときに追記する箇所★★★  #ass 2020/12 add
        insert_sql='UPDATE STOCK_INFO SET TODAY=?,DIF=?,BAND=?, P1SIG=?, P05SIG=?, N1SIG=?, N05SIG=?, MEIGARA_STA=?,TENKAN=?,CONFVAL0=?,CONFVAL1=?,CONFVAL2=?,COEFF0=?,COEFF1=?,COEFF2=?,KAGENCHI0=?,KAGENCHI1=?,KAGENCHI2=?,SAR=?,STA=?,SRATIO=?,CRATIO=?,AR=? WHERE STOCK_NUM=?'
        cur.execute(insert_sql,(today,dif,band,p1sig,p05sig,n1sig,n05sig,meigara_sta,tenkan,confval0,confval1,confval2,coeff0,coeff1,coeff2,kagenchi0,kagenchi1,kagenchi2,sar,sta,sratio,cratio,ar,stock_num)) # ← where句のstock_numは一番最後に持ってくる。
        #★★★★★★★★★★★★★★★★★★ 
        
        #print(cur)      
        #print(today)
        #print(dif)
        #print(stock_num)   
        #print("##db done")           
        con.commit()
        self.db_dump(cur) #SQLITE3 DBの値をCSVファイルにダンプする関数
        con.close()



    def db_dump(self,c):  #SQLITE3 DBの値をCSVファイルにダンプする関数
        con = sqlite3.connect(self.db_path)
        con.text_factory = str
        cur = con.cursor()
        sql_com = 'SELECT * FROM STOCK_INFO ORDER BY STOCK_NUM ASC'
        tmp = c.execute(sql_com)
        with open(self.csv_db_path, 'w',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(tmp)
            f.close()
        con.close()



class SQLDBCONT():

    def __init__(self, sel,csv_cyu_db_path):

        self.csv_cyu_db_path = csv_cyu_db_path
        self.db_path = setting.DB_PATH
        self.selectdb3(sel)


    def selectdb3(self,sel): #指定した銘柄のみを抽出する
        #print("sel")
        #sel=sel.split("\n")[0]
        InxARY = sel.split(',')  #文字列を配列に分解する
        
        self.sqlcommake(InxARY) #SQL文を自動記述する
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        #print("C1")
        df = pd.read_sql_query(self.sqlcommand,con)
        #print("C2")
        #print(df)

        df=df.set_index('STOCK_NUM')
        #print(df)
        #print("C")
        df.to_csv(self.csv_cyu_db_path,header=False)
        #print("D")
        #self.dump_csv(df,self.csv_cyu_db_path)
        #self.db_dump(self.db_cyusyutsu_path,self.csv_cyu_db_path, cur)
        #print(df1)
        #df2 = df.set_index('STOCK_NUM')


    def sqlcommake(self,vec): #list vecに入っている複数銘柄について　　SELECT * FROM STOCK_INFO WHERE STOCK_NUM IN (*,*,)というSQLコマンドを自動記述する
        moji = "("
        
        #print("vec")
        #print(vec.split("\n")[0])
        #vec=vec.split("\n")[0]
        for j in range(len(vec)-1):
            moji = moji + vec[j] + ","
        moji = moji+ vec[len(vec)-1] +")"


        self.sqlcommand = "SELECT * FROM STOCK_INFO WHERE STOCK_NUM IN" + moji

    #def dump_csv(self,df,csv_file_path):
        #with open(csv_file, 'w',encoding='utf-8') as f:
            #writer = csv.writer(f)
        #df.to_csv(csv_file_path)
            #writer.writerows(map(lambda x: [x], tmp))
            #f.close()




class DBModel(object):   #指定した箇所にCSVファイルがない場合、新たにcsvファイルを作成する。
    def __init__(self, csv_file):
        self.csv_file = csv_file
        if not os.path.exists(csv_file):
            pathlib.Path(csv_file).touch()  #指定したパスにcsvファイルを作成する。


class CSVModel(DBModel):
    """Definition of class that generates ranking model to write to CSV"""
    def __init__(self, csv_file=None, *args, **kwargs):
        if not csv_file:
            csv_file = self.get_csv_file_path()

        super().__init__(csv_file, *args, **kwargs)
        self.column = CSV_COLUMNS
        self.load_data()

    def get_csv_file_path(self):
        """Set csv file path.

        Use csv path if set in settings, otherwise use default
        """
        csv_file_path = None
        try:
            import setting
            if setting.CSV_FILE_PATH:
                csv_file_path = setting.CSV_FILE_PATH if os.path.exists(setting.CSV_FILE_PATH) else setting.CSV_FILE_PATH_LOCAL
        except ImportError:
            pass

        if not csv_file_path:
            csv_file_path = SEC_CSV_FILE_PATH
        return csv_file_path



    def load_data(self):
        """Load csv data.

        Returns:
            dict: Returns ranking data of dict type.
        """
        self.data = pd.read_csv(self.csv_file, names=CSV_COLUMNS)
        return self.data