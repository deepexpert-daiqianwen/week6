___author__ = 'Administrator'
 #coding:utf-8
import re
import cookielib
import smtplib
from email.mime.text import MIMEText
import string
import sys
import time
import threading
import urllib2
import urllib
mailto_list=[YYY@139.com]
mail_host="smtp.139.com"  #设置服务器
mail_user="XXXX"    #邮箱用户名
mail_pass="XXXXXX"  #邮箱密码
mail_postfix="mail.139.com" #发件箱的后缀

def send_mail(to_list,sub,content): #to_list：收件人；sub：主题；content：邮件内容

     me="hello"+"<"+mail_user+"@"+mail_postfix+">"
     msg = MIMEText(content,_subtype='plain',_charset='utf-8')
     msg['Subject'] = sub
     msg['From'] = me
     msg['To'] = ";".join(to_list)
     try:
         server = smtplib.SMTP()

         server.connect(mail_host)
         server.login(mail_user,mail_pass)
         server.sendmail(me, to_list, msg.as_string())
         server.close()
         return True
     except Exception, e:
         print str(e)
         return False

url = 'http://store.apple.com/hk-zh/buy-iphone/iphone6/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
postdata =  '{"dimensionScreensize":"(.*?)","dimensionColor":"(.*?)","dimensionCapacity":"(.*?)","partNumber":".*?","price":"(.*?)","displayShippingQuote":"(.*?)".*?}'
headers = { 'User-Agent' : user_agent }
data = urllib.urlencode(postdata)
while True:
  req = urllib2.Request(url, data, headers)
try:
  response = urllib2.urlopen(req)
except urllib2.URLError, e:
 print "Error retrieving data:", e
sys.exit(1)
result = response.read()
data=re.compile(postdata).findall(result)
if data:
 if send_mail(mailto_list,"订购iphone","iphone6有货"):
     print  "信息发送成功！"
 else:
     print "邮件发送失败！"

time.sleep(60)
