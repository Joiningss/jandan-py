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
def makeMyOpener(head = {
  'Connection': 'Keep-Alive',
  'Accept': 'text/html, application/xhtml+xml, */*',
  'Accept-Language': 'zh_CN,zh;q=0.8',
  'User-Agent': 'Mozilla/5.0 ( compatible; MISE 5.5; Windows NT)' 
}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener()
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
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
