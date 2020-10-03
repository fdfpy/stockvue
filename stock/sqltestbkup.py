# coding: utf-8

import sys
import sqlite3
import pandas as pd
import csv
import calendar
import datetime
import setting

###########################
#入力情報の読みとり
###########################




stock_num=sys.argv[1]



#f=open('/home/pi/Desktop/stock/sqltest.txt','w')
#f.write(sys.argv[1])




########################################
# DBに記録した情報をcsvファイルにダンプする
########################################



def db_dump(c):
    sql_com='SELECT * FROM STOCK_INFO ORDER BY STOCK_NUM ASC'
    tmp=c.execute(sql_com)   
    with open(setting.CSV_FILE_PATH ,'w') as f:
        writer=csv.writer(f)
        writer.writerows(tmp)


    
    #f=open('/home/pi/Desktop/stock/sqltest.txt','w')
    #sql_com='SELECT * FROM STOCK_INFO'
    #for row in c.execute(sql_com):
       # f.write(str(row))
    #f.close()

###########################################
# 指定月の最終日を取得する。
###########################################

def last_date(M):
    Y=datetime.datetime.today().year
    #print("M")

    date=datetime.date(Y, M, 1) - datetime.timedelta(days=1)
    #print(date)
    return date


#KESSAN_MONTH=last_date(KESSAN_MONTH)



###########################################
# メイン処理
###########################################

if __name__=='__main__':



    
    try:

######################
# DBに情報を記録する
######################

        con=sqlite3.connect(setting.DB_PATH)
        print(setting.DB_PATH)
        con.text_factory=str
        cur=con.cursor()
        insert_sql='INSERT INTO STOCK_INFO (STOCK_NUM,TODAY,DIF) values (?,?,?)'
        STOCK_INFO=(stock_num,"","")
        cur.execute(insert_sql,STOCK_INFO)
        con.commit()
        db_dump(cur)
        con.close()
        #print 'parameter1 is ' + sys.argv[1]
        #print 'parameter2 is ' + sys.argv[2]
        #f=open('/home/pi/Desktop/stock/sqltest.txt','w')
        #f.write(sys.argv[1])
        #f.write(sys.argv[2])
        #f.close()

#    except Exception as ex:
#        f.write(format(ex))
#        f.close()

######################
# エラー処理
# 銘柄が同じデータを書き込んだ場合は、更新する。
######################



    except sqlite3.IntegrityError as ex:
        print("#")
        print(ex)
        if "UNIQUE constraint failed: STOCK_INFO.STOCK_NUM" in ex:
            print("ERROR:{}".format(ex))
            insert_sql='REPLACE INTO STOCK_INFO (STOCK_NUM,TODAY,DIF) values (?,?,?)'
            STOCK_INFO=[(stock_num,"","")]
            con.executemany(insert_sql,STOCK_INFO)
            con.commit()
            db_dump(cur)
            con.close()



        #elif "datatype mismatch" in ex:
        #    print("ERROR:{}".format(ex))          
            
        


#except sqlite3.IntegrityError.datatype mismatch      
