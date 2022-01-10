## Crawler For ACMCompetitions

codeforces、nowcoder、atcoder等平台近期比赛的爬虫

（接下来的更新中会做成Web端）

## 运行环境

LINUX系统、python3



## 下载安装

1. 下载到本地

```shell
git clone https://github.com/ricar0/Crawler-For-ACMCompetitions.git
```

2. 传到服务器端

3. 修改代码中的数据库地址和密码

4. 给start.sh增加权限

   ```shell
   chmod +x start.sh
   ```

   

5. 为程序添加定时任务(平均每小时爬取一次)

   ```shell
   1 * * * * /root/ACM-Competitions-Collections/start.sh
   ```

   

## 成功

![image-20220110201147190](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20220110201147190.png)

