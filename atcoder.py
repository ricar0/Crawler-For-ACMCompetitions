import re
import requests
import datetime
import json
import pymysql

con = pymysql.connect(host='localhost',user='root',passwd='wmy0976543244', db='competition')

cur=con.cursor()

url="https://atcoder.jp/contests/"
obj1=re.compile(r'<div id="contest-table-upcoming">(?P<content>.*?)</div>', re.S)#获取最近比赛的html

obj=re.compile(
               r'<time class=\'fixtime fixtime-full\'>(?P<time>.*?)\+.*?</time>[\s\S]*?' 
               r'<td >[\s\S]*?' 
               r'<span class=".*?">◉</span>[\s\S]*?'
               r'<a href="(?P<link>.*?)">(?P<name>.*?)</a>[\s\S]*?'
               r'</td>[\s\S]*?'
               r'<td class="text-center">(?P<length>.*?)</td>'
                                                                    ,re.S)

headers = { # 这里使用自己电脑浏览器的user-agent即可
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}

r = requests.get(url, headers=headers)
c = r.text
itt=obj1.finditer(c)

for i in itt:
    dic = i.groupdict()
    c=dic['content'].format()

it = obj.finditer(c)


filename= 'json/atcoder.json'
data=[]

sql = "delete from competitions where website = (%s)"
cur.execute(sql, ("atcoder"))

for i in it:
    dic = i.groupdict()
    dic['link'] = 'https://atcoder.jp' + dic['link']
    sql="insert into competitions values(%s,%s,%s,%s,%s)"

    dic['time'] = (datetime.datetime.strptime(dic['time'], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    data.append(dic)
    cur.execute(sql, ("atcoder", dic["name"], dic["time"], dic["link"], dic["length"]))
with open(filename,'w',encoding='utf-8') as file:
    file.write(json.dumps(data,ensure_ascii=False))

r.close()
cur.close()
con.commit()
con.close()