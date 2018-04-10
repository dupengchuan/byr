# -*- coding: UTF-8 -*-
import json
import requests
import sys
from bs4 import BeautifulSoup
from threading import Timer
import time

s = requests.Session()

ajax_code_success = '0005'
ajax_code_fail = '0101'
base_url = 'https://bbs.byr.cn'

class BYR:
    def __init__(self, username, password):
        self.sleep_time = 0
        self.username = username
        self.password = password
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Referer': 'https://bbs.byr.cn/',
            'X-Requested-With': 'XMLHttpRequest'
        }

    #登录函数
    def login(self):
        """
        登录
        :return:
        """
        url = 'https://bbs.byr.cn/user/ajax_login.json'
        data = {
            'id': self.username,
            'passwd': self.password,
        }
        headers = {
            'Referer': 'https://bbs.byr.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
            'X-Requested-With': 'XMLHttpRequest'
        }
        content = s.post(url, data=data, headers=headers).text
        result = json.loads(content)
        return result

    #定时任务
    def handle(self,result):
        #if result.get('new_mail'):
        self.replyMail()
        pass


    #聊天接口
    def dialog(self,content):
        d1 = {
            "key": "e49d176663464f0dbe04084963af75c5",
            "info": content
        }
        result = json.loads(s.post("http://www.tuling123.com/openapi/api",data=d1).text)
        if result.get('code') == 100000:
            return result.get('text')
        else:
            print('dialog error!')
            return ' '
        pass

    def ajax_send(self,id,title,content,signature,backup,num):
        d = {
            "id" : id,
            "title" : title,
            "content" : content,
            "signature" : signature,
            "backup" : backup,
            "num" : num
        }
        result = json.loads(s.post(base_url + "/mail/NULL/ajax_send.json", data=d,headers=self.headers).text)
        return result
        pass

    def ajax_session(self):
        result = json.loads(s.get(base_url + "/user/ajax_session.json", headers=self.headers).text)
        return result
        pass

    #邮件答复函数
    def replyMail(self):
        html = s.get(base_url + "/mail?_uid=" + self.username, headers=self.headers).content
        soup = BeautifulSoup(html, 'lxml')  # 'html.parser' 比较慢'
        pagenum = soup.select("li.page-pre i")[0].text
        pagenum = int(int(pagenum)/20) + 1
        n = 1
        for n in range(1,pagenum):
            url = base_url + "/mail/inbox?p=" + str(n) + "&_uid=" + self.username
            html = s.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            title = soup.select('tr.no-read a.mail-detail')
            id = soup.select('tr.no-read td.title_2 a')
            i = 0
            for r in soup.select('tr.no-read'):
                content = self.dialog(title[i].text)
                href = title[i].get("href")  # one item
                result = json.loads(s.get(base_url + href, headers=self.headers).text)
                if not result.get('ajax_code'):
                    reutrn
                data = {
                    'id': id[i].text,
                    'title': 'Re: ' + title[i].text,
                    'content': content,
                    'signature': '0',
                    'backup': 'on',
                    'num': result.get('num')
                }
                while True:
                    res = json.loads(
                        s.post(base_url + "/mail/inbox/ajax_send.json", data=data, headers=self.headers).text)
                    if res.get("ajax_code") == "0607":
                        print(res)
                        break
                    if res.get("ajax_code") == "0403":
                        self.sleep_time += 1
                        time.sleep(self.sleep_time)
                i += 1
                time.sleep(self.sleep_time)
        pass

def loop(byr,result):
        byr.handle(result)
        # result = json.loads(s.get(base_url+"/user/ajax_session.json", headers = byr.headers).text)
        # print (result)
        t = Timer(60*5,loop,(byr,result))
        t.start()
        pass

username = input('请输入账号：')
password = input('请输入密码：')
byr = BYR(username, password)
result = byr.login()
if result.get('ajax_code')==ajax_code_success:
    print('登录成功')
    loop(byr,result)
    num=0
    t = 0;
    for num in range(0,100):
        res = byr.ajax_send("sky1990","hello",num,0,"on","")
        while res.get("ajax_code")=="0403":
            t += 1
            time.sleep(t)
            res = byr.ajax_send("sky1990", "hello", str(num), 0, "on", "")
        time.sleep(t)
        if res.get("ajax_code") == '0607':
            print(num)
        #time.sleep(6)
elif result.get('ajax_code')==ajax_code_fail:
    print('登录失败')