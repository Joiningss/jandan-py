#-*-coding: utf-8-*-
import re
import urllib.request
import http.cookiejar
from collections import deque
from datetime import datetime
import socket
import codecs
socket.defaulttimeout = 3
 
queue = deque()  #等待采集概览队列
visited = set()  #已经采集的队列
detail = set()   #所有细览页面
node = set()     #所有概览页面
now = datetime.now()

url = 'http://www.newsgd.com/newindextest/'  # 入口页面, 可以换成别的
 
queue.append(url)
cnt = 0

def getHtml(url,head = {
  'Connection': 'Keep-Alive',
  'Accept': 'text/html, application/xhtml+xml, */*',
  'Accept-Language': 'zh_CN,zh;q=0.8',
  'User-Agent': 'Mozilla/5.0 ( compatible; MISE 5.5; Windows NT)' 
},decode_method = 'utf-8',timeout_s = 2):
	cj = http.cookiejar.CookieJar()
	opener = urllib.request.build_opener()
	header = []
	for key, value in head.items():
		elem = (key, value)
		header.append(elem)
	opener.addheaders = header
	page = opener.open(url,timeout=timeout_s)
	html = page.read().decode(decode_method)
	return html
	
f = codecs.open('newsgd.txt','a+',encoding='utf-8') 
year_month = now.strftime('%Y-%m')
day = now.strftime('%d')
reg = r'http://www.newsgd.com[^\.]*.htm'
reg_1 = r'http://www.newsgd.com[^\.\s">]*/'+year_month+'/'+day+'/content_[\d]{3,}.htm'
reg_2 = r'http://www.newsgd.com[^\.\s">]*/(default|default_[\d]{1}|node_[\d]{6}|node_[\d]{6}_[\d]{1}).htm'
			
while queue:
	url = queue.popleft()  # 队首元素出队
	visited |= {url}  # 标记为已访问
	print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
	cnt += 1
	try:
		html = getHtml(url)
	except Exception as e:
		continue
	else:
		re_obj = re.compile(reg, re.I)
		urllist = re_obj.findall(html)
		for x in urllist:
			if re.match(reg_1,x) and x not in detail:
				detail |= {x}
				f.write(x+'\n')
			elif re.match(reg_2,x) and x not in node:
				node |= {x}
				queue.append(x)
			else:
				pass

f.close()
print("全部抓取完毕!")
