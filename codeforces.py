import re
import requests
import json
import pymysql
import datetime
con = pymysql.connect(host='localhost',user='root',passwd='wmy0976543244', db='competition')

cur=con.cursor()

url="https://codeforces.ml/contests"
obj=re.compile(r'<tr data-contestId="(?P<link>[0-9]+)">[\s\S]<td>[\s\S](?P<name>.*?)[\s\S]</td>.*?'
               r'<span class="format-time" data-locale="en">(?P<time>.*?)</span>[\s\S]'
               r'.*?<td>[\s\S](?P<length>.*?)[\s\S]</td>'
                                                                    ,re.S)

headers = { # 这里使用自己电脑浏览器的user-agent即可
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}

r = requests.get(url, headers=headers)
c = r.text
it = obj.finditer(c)

filename= 'json/codeforces.json'
data=[]

sql = "delete from competitions where website = (%s)"
cur.execute(sql, ("codeforces"))
mon = {'Jan':'1','Feb':'2',"Mar":'3','Apr':'4',"May":'5',"Jun":'6',"Jul":'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}
for i in it:
    dic = i.groupdict()
    dic['link'] = 'https://codeforces.ml/contests/' + dic['link']
    dic['time']=dic['time'].split('\n')[0]
    print(dic['length'])
    sql = "insert into competitions values(%s,%s,%s,%s,%s)"
    p=dic['time'].split(' ')
    pp=p[0].split('/')
    time=pp[2]+'-'+mon[pp[0]]+'-'+pp[1]+' '+p[1]
    dic['time']=(datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")+datetime.timedelta(hours=5)).strftime('%Y-%m-%d %H:%M')

    cur.execute(sql, ("codeforces", dic["name"], dic['time'], dic["link"], dic["length"]))

    data.append(dic)

with open(filename,'w',encoding='utf-8') as file:
    file.write(json.dumps(data,ensure_ascii=False))

r.close()
cur.close()
con.commit()
con.close()
