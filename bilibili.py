from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import requests
#from lxml import html
import re
import threading
import urllib3
urllib3.disable_warnings()
table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

def dec(x):
    """将BV号转化为av号"""
    r=0
    for i in range(6):
        r+=tr[x[s[i]]]*58**i
    return (r-add)^xor


def star():
    url=text1.get(1.0,END)
    url2 = "https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&qn=64&type=&otype=json"
    headers2 = {
        "host": "",
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }

    BVid=re.findall("video/(.+)\?",url)
    avid=dec(BVid[0])
    text2.insert(1.0,'av号：'+str(avid)+'\n')
    cid ,name = get_cid(avid)
    text2.insert(3.0,'视频名称：'+name+'\n')
    flv_url , size = get_flvurl(url2.format(avid=avid,cid=cid))
    print(flv_url)
    bulk = size / 1024 / 1024
    text2.insert(5.0,"本视频大小为：%.2fM" % bulk+'\n')
    h = re.findall("https://(.*?)com",flv_url)
    print(h)
    host = h[0]+"com"
    headers2["host"] = host
    res = requests.get(flv_url,headers=headers2,stream=True, verify=False)

    if res.status_code==200:
        text2.insert(7.0,'下载成功')
    save_movie(res,name)

def get_cid(aid):
    """得到cid"""
    header = {
        'host': 'api.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
             }
    url = "https://api.bilibili.com/x/player/pagelist?aid={aid}&jsonp=jsonp".format(aid=aid)
    response = requests.get(url,headers=header).json()
    return response["data"][0]["cid"] ,response["data"][0]["part"]

def get_flvurl(url):
    """获得视频真实flv地址"""
    header = {'host': 'api.bilibili.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

    response = requests.get(url,headers=header).json()
    return response["data"]["durl"][0]["url"],response["data"]["durl"][0]["size"]

def save_movie(res,name):
    """保存视频"""
    chunk_size = 1024
    with open("C:\\Users\\gongdong\\Desktop\\pic\\{name}.flv".format(name = name),"wb") as f:
        for data in res.iter_content(1024):
            f.write(data)


def thread_it(func,*args):
    """将函数打包进线程内执行"""
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()

win = Tk()
#界面参数
win.title('load video')
win.geometry('600x500')
win['bg'] = 'mistyrose'
win.iconbitmap('')
#标签
la1 = Label(win,text='请输入视频',font = ('隶书',15))
la1.place(relx = 0.4,rely = 0.05,)
la2 = Label(win,text = '消息')
#文本框
text1 = Text(win,width = 60, height = 4)
text1.place(relx = 0.15,rely = 0.12)
la2.place(relx = 0.46,rely = 0.37)
text2 = Text(width=60, height=15)
text2.place(relx=0.15,rely=0.42)
#按钮
button1 = Button(win,text = 'start',command =lambda :thread_it(star))
button1.place(relx=0.44,rely=0.25)
win.mainloop()
