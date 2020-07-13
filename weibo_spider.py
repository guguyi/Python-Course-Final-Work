import re
import time
import requests
import pathlib
from lxml import etree
from bs4 import BeautifulSoup


class wb_spider(object):
    """
        请求网址:https://weibo.cn/
        请求方法:GET
        由于weibo反爬机制很强,所以先获取指定用户的全部weibo界面,保存在.txt文件中。
        相较于https://m.weibo.cn/ 和 https://weibo.com/ ,这个网址好爬很多。
    """
    # cookies = {'your cookies'}  # 你的cookies
    cookies = {
        'cookie': '_T_WM=94460060722; SCF=Akc6-rgt_orPQPcMl2x5HV85EqkMAXlAtNu4p7Xjq-Yk3pldnC21hCsqvkdyckOmI9VGTWz2-fh41X9Gv2M3pY0.; SUB=_2A25z2CfhDeRhGeBL7FES9i3LzzSIHXVRI0mprDV6PUJbkdANLUb3kW1NRssixUMbX_chzOWyuMU2qvh9yNV6fdq6; SUHB=0Ryq3AMeUc9U3v'}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    url0 = 'https://weibo.cn/'

    def __init__(self, uid, username):
        """
            构造函数
            uid: 要爬取用户的uid
        """
        if isinstance(uid, str):
            self.url = self.url0+str(uid)
        elif isinstance(uid, int):
            self.url = self.url0+'u/' + str(uid)
        self.username = username
        self.pagenum = 0

    def get_pagenum(self):
        """
            通过爬取微博用户的第一页来获取总微博页数
        """
        try:
            r = requests.get(self.url, headers=self.headers,
                             cookies=self.cookies)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.content
            tree = etree.HTML(html)
            pagelist = tree.xpath('//*[@id="pagelist"]/form/div/text()')
            self.pagenum = int(str(pagelist)[16:-3])
        except Exception as e:
            print(e)

    def filenaming(self):
        """
            文件名称生成并创建空文件
            self.username: 用户名
            self.pagenum: 微博总页数
        """
        filenamelist = []
        for i in range(1, self.pagenum+1):
            filename = self.username+'_'+str(i)+'.txt'
            filenamelist.append(filename)
            pathlib.Path(filename).touch()
        self.filenamelist = filenamelist

    def get_html(self):
        """
            将抓取到的html页面存储到txt文件中
        """
        # time_start = time.time()
        # print(time_start)
        for i in range(1, self.pagenum+1):
            try:
                time.sleep(3)
                # tmp_url = 'https://weibo.cn/tfyiyangqianxi?page='+str(i)
                tmp_url = self.url+'?page='+str(i)
                print(tmp_url)
                r = requests.get(tmp_url, cookies=self.cookies,
                                 headers=self.headers)
                r.raise_for_status()
                html = r.content
                with open(self.filenamelist[i-1], mode='wb+') as f:
                    f.write(html)
                time.sleep(5)
                print(i)
            except Exception as e:
                print('spider failed')
                print(e)
        time_end = time.time()
        print(time_end)
