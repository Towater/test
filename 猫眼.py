#2018/7/18
#获取猫眼TOP100榜
#加入多线程
#加入与数据库的交互
import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
import re
import json
import pymysql


header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def get_page(URL):
    #加入网络判断
    try:
        MY_re = requests.get(URL,headers=header)
        if MY_re.status_code == 200:
            return MY_re.text
        return None
    except RequestException:
        return None
        
        
def parse_page(html):
    MY_pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)"' \
                      +'.*?class="name".*?title="(.*?)".*?class="star">(.*?)</p>' \
                      +'.*?class="releasetime">(.*?)</p>',re.S)
    
    items = re.findall(MY_pattern,html) 
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:]
        }

def save_file(item):
    with open ("e://new.txt",mode='a+') as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')     


def database(items):
    conn = pymysql.connect(user='root',password='980404',database='top',host='127.0.0.1')
    try:
        with conn.cursor() as csr:
            for item in items:
                sql = 'insert into movies values(%d,%s,%s,%s,%s)'
                csr.execute(sql,((int(item['index']),item['image'],item['title'],item['actor'],item['time'])))
                conn.commit()
            
    finally:
        conn.close()

def filetodatabase(item):
    

def main(page):
    MY_URL = 'http://maoyan.com/board/4?offset=' + str(page*10)
    MY_html = get_page(MY_URL)
    for item in parse_page(MY_html):
        print(item)
        save_file(item)
           
        

if __name__=="__main__":
    #普通写法
    for i in range(10):
        main(i)
            
   
'''   
    #普通写法
    for i in range(10):
        main(i)
    
    
    #多线程写法,无法按顺序输出
    pool = Pool()
    pool.map(main, [i for i in range(10)])    

'''    

