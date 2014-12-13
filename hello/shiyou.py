__author__ = 'Administrator'

import requests
import time
import MySQLdb
import re
import urllib2

con = MySQLdb.connect(host='localhost', user='root', passwd='root',db='python')     #与数据库建立连接
cur = con.cursor()									    #获取操作游标
cur.execute("create table oil(Local_time VARCHAR(20),USDCNH VARCHAR(8),DINIW  VARCHAR(8))")	#创建一个oil表，包含记录时间、原油数两个参数
cur.execute("create table dollarhl(Local_time VARCHAR(20),CONC VARCHAR(20))")		    #创建一个oil表，包含记录时间、汇率两个参数
cur.execute("create table dollarzs(Local_time VARCHAR(20),CONC VARCHAR(20))")		    #创建一个oil表，包含记录时间、美元指数两个参数
									    #关闭数据库连接

url1 = 'http://www.cngold.org/img_date/yuanyou.html'
url2 = 'http://finance.sina.com.cn/money/forex/hq/USDCNY.shtml'
url3 = 'http://finance.sina.com.cn/money/forex/hq/DINIW.shtml'
html1 = requests.get(url1)
html2 = requests.get(url2)
html3 = requests.get(url3)

while(True):


     res1 = urllib2.urlopen(url1)
     res2 = urllib2.urlopen(url2)
     res3 = urllib2.urlopen(url3)
     page1 = res1.read()
     page2 = res2.read()
     page3 = res3.read()

     reg1 = r'''var js={futures:\["(.+)"\],extendedFutures:'''
     tuple1 =  re.findall(reg1,page1)
     arr1 = tuple1[0].split(',')
     cur.execute("insert into oil values ('%s',%f,'%s')"% ("国际石油期货",float(arr1[5]),str(arr1[27])))
     con.commit()


     reg2 = r'''var hq_str_(.+)="(.+),(.+),.+,.+,.+,.+,.+,.+,.+,.+'''
     tuple2 = re.findall(reg2,page2)
     cur.execute("insert into dollarhl values ('%s',%f,'%s')"% ("美元人民币汇率",float(tuple2[0][2]),str(tuple2[0][1])))
     con.commit()

     reg3 = r'''var hq_str_(.+)="(.+),(.+),.+,.+,.+,.+,.+,.+,.+,.+'''
     tuple3 = re.findall(reg3,page3)
     cur.execute("insert into dollarzs values ('%s',%f,'%s')"% ("美元指数",float(tuple3[0][2]),str(tuple3[0][1])))
     con.commit()							    #提交

     time.sleep(60*60)								    #隔一个小时采样一次
     cur.close()
     con.close()









