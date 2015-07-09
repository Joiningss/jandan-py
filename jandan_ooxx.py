#-*-coding:utf-8-*-
import urllib.request

import http.cookiejar
import socket,os
from time import sleep,ctime
import threading
from bs4 import BeautifulSoup
targetDir = r"E:\Pictures\ooxx"
socket.setdefaulttimeout(2)

#自定义opener
def makeMyOpener():
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
    return opener

#图片存储路径
def destFile(path):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    pos = path.rindex('/')
    t = os.path.join(targetDir,path[pos+1:])
    return t

#下载图片
def download_img(start,end=1425):
    for i in range(start, end):  #从第900页开始
        url = 'http://jandan.net/ooxx/page-'+str(i)+'#comments'
        try:
            opener = makeMyOpener()
            urlop = opener.open(url)
            page = urlop.read().decode('utf-8')
            urlop.close()  #每次都要关闭连接
        except urllib.request.URLError as e:
            print(e.code)
            continue
        soup = BeautifulSoup(page,from_encoding="utf-8")
        print("page duan: "+ str(i))
        locations = soup.find_all("div", class_="text") #a标签下的url
        
        for p1 in locations:
            location = p1.find_all('img')
            for p1 in location:
                 pic_url = p1.get('org_src') if p1.get('org_src') else p1.get('src')
                 if pic_url is not None and '，' not in pic_url and 'http' in pic_url:
                     print('正在下载图片:'+pic_url)
                     try:
                         urllib.request.urlretrieve(pic_url,destFile(pic_url))
                         #sleep(1)  #休眠1秒
                     except IOError as e:
                         print(e)
                         continue    
    print('全部图片下载完成')

if __name__ == "__main__":
	start = input("输入起始页码,你可以回车跳过,默认从900页开始:")
	if start.isdigit() and int(start) >= 900:
		download_img(int(start))
	else:
		download_img(900)
