import re
import requests
import json
import pymysql

con = pymysql.connect(host='localhost',user='root',passwd='wmy0976543244', db='competition')

cur=con.cursor()

url="https://ac.nowcoder.com/acm/contest/vip-index"
obj1=re.compile(r'<div class="platform-mod js-current">(?P<content>.*?)<div class="platform-mod js-end">', re.S)#获取最近比赛的html

obj=re.compile(r'<div class="platform-item-main">([\s\S]*?)'
               r'<div class="platform-item-cont">([\s\S]*?)'
               r'<h4>([\s\S]*?)'
               r'<a href="(?P<link>.*?)>?" target="_blank">(?P<name>.*?)</a>.*?'
               r'<li class="match-time-icon">比赛时间：(?P<time>.*?)至.*?(时长:(?P<length>.*?))</li>'
                                                                    ,re.S)

headers = { # 这里使用自己电脑浏览器的user-agent即可
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}

r = requests.get(url, headers=headers)
c = r.text
# f = open("data.csv", mode="w", encoding="utf-8", newline="")
# f.write(c)

itt=obj1.finditer(c)

for i in itt:
    dic = i.groupdict()
    c=dic['content']

it = obj.finditer(c)
filename= 'json/nowcoder.json'
data=[]

sql = "delete from competitions where website = (%s)"
cur.execute(sql, ("nowcoder"))

for i in it:
    dic = i.groupdict()
    dic['link'] = 'https://ac.nowcoder.com' + dic['link']
    dic['time']=dic['time'].split('\n')[0]
    data.append(dic)
    dic['length'] = dic['length'].split(')')[0]
    sql = "insert into competitions values(%s,%s,%s,%s,%s)"
    cur.execute(sql, ("nowcoder", dic["name"], dic["time"], dic["link"], dic["length"]))

with open(filename,'w',encoding='utf-8') as file:
    file.write(json.dumps(data,ensure_ascii=False))

r.close()
cur.close()
con.commit()
con.close()