#-*-coding:utf-8-*-
import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
import pymysql
import socket
socket.setdefaulttimeout(2)

#自定义opener
def makeMyOpener(url,head = {
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
    page = opener.open(url)
    html = page.read().decode('utf-8')
    return html

#文件读取迭代器
def read_file(fpath): 
    BLOCK_SIZE = 1024 
    with open(fpath, 'rb') as f: 
        while True: 
            block = f.read(BLOCK_SIZE) 
            if block: 
                yield block 
            else: 
                return

f = read_file('list.txt')
conn = pymysql.connect(host='hostname',port=3306,user='username',passwd='password',db='dbname',charset='utf8')
cur = conn.cursor()

        
for url in f:
    try:
        html = makeMyOpener(url)
        soup = BeautifulSoup(html,from_encoding='utf-8')
        
        title = soup.find('h1',attrs={'id':'article_title'}).text.strip()
        srcname = soup.find('span',attrs={'id':'source_baidu'}).text.replace(u'来源：','').strip()
        author = soup.find('span',attrs={'id':'author_baidu'}).text.replace(u'作者：','').strip()
        editor = soup.find('span',attrs={'id':'editor_baidu'}).text.replace(u'编辑：','').strip()
        urltime =  soup.find('span',attrs={'id':'pubtime_baidu'}).text.strip()
        contentHtml = soup.find('div', attrs={'id':'content'})
        content = contentHtml.text.strip()
        urlimages = contentHtml.find_all('img')  #图片链接
        urlimage = ''
        pager = contentHtml.find('div',attrs={'width':'100%'})  #分页标识
        for p1 in urlimages:
			pic = p1.get('src') if p1.get('src') != 'http://www.southcn.com/public/2014/css/snwap/300.jpg' else ''
            urlimage += pic + ';'
        k = 2
        if(pager):    
            while True:
                try:
                    next_url = url.split('.htm')[0]+'_'+str(k)+'.htm'
                    next_html = makeMyOpener(next_url)
                    contentHtml = soup.find('div', attrs={'id':'content'})
                    content += contentHtml.text.strip()
                    urlimages = contentHtml.find_all('img')  #图片链接
                    for p2 in urlimages:
						pic = p2.get('src') if p2.get('src') != 'http://www.southcn.com/public/2014/css/snwap/300.jpg' else ''
                        urlimage += pic + ';'
                    k += 1
                except Exception as e:
                    break
        sql = "insert into southcn(urltitle,srcname,author,editor,content,urlimage,urltime,urlname) values('"+title+"','"+srcname+"','"+author+"','"+editor+"','"+content+"','"+urlimage+"','"+urltime+"','"+url+"')"
        cur.execute(sql)
        conn.commit()
        print('clawering: '+url+'\n')
    except Exception as e:
        print(e)
cur.close()
conn.close()
print('now you have clawer all the pages')
