#-*-coding: utf-8-*-
'''
author: tony
date: 2015-07-08
environment: python3.4 + bs4
'''

import urllib.request
import http.cookiejar
import random
import socket
import sqlite3
from time import sleep
from bs4 import BeautifulSoup
socket.defaulttimeout = 3
 

conn = sqlite3.connect('jandan.db')
conn.execute(
'''
create table if not exists duan(id integer not null primary key autoincrement,
content text,
stime char(20),
sauthor char(30),
surl char(60),
oo int,
xx int);
'''
)


def getHtml(url):
	cookie_support = urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
	#proxy_support = urllib.request.ProxyHandler({"http":"115.159.50.56:8080"})
	#若需要使用代理,请把proxy_support参数加入下面
	opener = urllib.request.build_opener(cookie_support,urllib.request.HTTPHandler) 
	urllib.request.install_opener(opener)
	user_agents = [
		'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11','Opera/9.25 (Windows NT 5.1; U; en)',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
		'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
		'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
		'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
		'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
		'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
		'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
		'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
		'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999',
		'Baiduspider+(+http://www.baidu.com/search/spider.htm)',
		'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
		'Sogou web spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
		'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/)',
		]
	   
	agent = random.choice(user_agents)
	opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.baidu.com'),('Host','http://jandan.net')]
	page = opener.open(url,timeout=3)
	html = page.read()
	return html

def crawler(start,end):
	print("现在开始启动爬虫!")
	for i in range(start,end):
		url = 'http://jandan.net/duan/page-'+str(i)+'#comments'
		html = getHtml(url)
		soup = BeautifulSoup(html)
		authors = soup.find_all('div',class_='author')
		texts = soup.find_all('div',class_='text')
		votes = soup.find_all('div',class_='vote')
		print('正在解析第' + str(i) + '页:'+url)
		
		for j in range(len(authors)):
			stext = ''
			author = authors[j].find('strong').text
			stime = authors[j].find('small').find('a').text
			surl = texts[j].find('a').get('href')
			ptags = texts[j].find_all('p')
			for ptag in ptags:
				stext += ptag.text
			oo = votes[j].text.split(' ')[1].strip('[]')
			xx = votes[j].text.split(' ')[3].strip('[]')
			conn.execute("insert into duan(content,stime,sauthor,surl,oo,xx) values('"+stext+"','"+stime+"','"+author+"','"+surl+"','"+oo+"','"+xx+"')")
		conn.commit()
		sleep(1)  #这里睡眠1秒, 不要爬太快, 以防被反爬技术识破

if __name__ == '__main__':
	start = input("输入起始页码:")
	end = input("输入结束页码,不要超过jandan.net/duan最大页码:")
	if start.isdigit() and end.isdigit() and (int(start) < int(end)):
		crawler(int(start),int(end)+1)
	else:
		print("你输入的页码不正确!")
	conn.close()
	print("退出爬虫!")
