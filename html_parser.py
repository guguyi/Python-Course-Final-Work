import re
import sys
import csv
import pandas
import requests
from lxml import etree
from bs4 import BeautifulSoup
from collections import OrderedDict


class html_parser(object):
    cookies = {
        'cookie': 'your cookies'}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

    def __init__(self, filename,  txtname, csvname, wrote_num_txt, wrote_num_csv):
        """
            filename: 爬取到的html页面（保存在txt文件中）
            to_csvname:目标csv路径
            to_txtname:目标txt路径
            wrote_num_txt:txt已写入的记录个数
            wrote_num_csv:csv已写入的记录个数
        """
        self.filename = filename
        self.to_csvname = csvname
        self.to_txtname = txtname
        self.wrote_num_txt = wrote_num_txt
        self.wrote_num_csv = wrote_num_csv
        self.weibo = []


    def get_tree(self):
        """
            生成lxml.etree._Element对象
        """
        try:
            with open(self.filename, mode='r', encoding='utf-8') as f:
                html = f.read()
            # 删除<?xml version="1.0" encoding="UTF-8"?>
            string = '<?xml version="1.0" encoding="UTF-8"?>'
            if string in html:
                html = html.replace(string, '')
            self.html = html
            tree = etree.HTML(html)
            self.tree = tree
        except Exception as e:
            print(e)
            print("get_tree error!")

    def deal_grabled(self, info):
        """
            处理爬取原创微博时的乱码
            info: lxml.etree._Element对象
        """
        try:
            info = (info.xpath('string(.)')).replace(u'\u200b', '').encode(
                sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding)
            return info
        except Exception as e:
            print(e)
            print("deal_grabled error!")

    def is_original(self, info):
        """
            判断一条微博是否为原创微博
            info: lxml.etree._Element对象
        """
        is_original = info.xpath(
            'div/span[@class="cmt"]')  # 原创微博span标签中有class="cmt"属性
        if len(is_original) > 3:
            return False
        else:
            return True

    def get_long_weibo(self, url):
        """
            获取长原创微博
            长原创微博需要再次请求url
            url: 'https://weibo.cn/comment/'+weibo_id
        """
        try:
            r = requests.get(url, headers=self.headers, cookies=self.cookies)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.content
            tree = etree.HTML(html)
            info = tree.xpath('//div[@class="c"]')[1]  # 定位
            content = self.deal_grabled(info)  # 处理乱码
            time = info.xpath("//span[@class='ct']/text()")[0]
            weibo_content = content[content.find(':') +
                                    1:content.rfind(time)]  # 分割
            return weibo_content

        except Exception as e:
            print(e)
            print("get_long_weibo error!")

    def get_original_weibo(self, info, weibo_id):
        """
            获取原创微博
            info: lxml.etree._Element对象
            weibo_id: weibo对应的唯一id
        """
        try:
            weibo_content = self.deal_grabled(info)  # 处理乱码
            weibo_content = weibo_content[:weibo_content.rfind(u'赞')]
            a_text = info.xpath('div//a/text()')
            if u'全文' in a_text:  # 长微博判断
                weibo_link = 'https://weibo.cn/comment/' + weibo_id
                content = self.get_long_weibo(weibo_link)
                if content:
                    weibo_content = content
            return weibo_content
        except Exception as e:
            print(e)
            print("get_original_weibo error!")

    def get_repost_weibo(self, info, weibo_id):
        """
            获取转发微博的转发理由
            info: lxml.etree._Element对象
            weibo_id: weibo对应的唯一id
        """
        try:
            reason = self.deal_grabled(info.xpath('div')[-1])
            reason = reason[:reason.rindex(u'赞')]
            weibo_content = reason
            return weibo_content
        except Exception as e:
            print(e)
            print("get_repost_weibo error!")

    def get_weibo_content(self, info, is_original):
        """
            获取微博正文
            info: lxml.etree._Element对象
            is_original: 是否为原创微博 对应原创微博的解析函数
        """
        try:
            weibo_id = info.xpath('@id')[0][2:]
            if is_original:  # 原创微博处理
                weibo_content = self.get_original_weibo(info, weibo_id)
            else:  # 转发微博处理
                weibo_content = self.get_repost_weibo(info, weibo_id)
            print(weibo_content)  # 打印微博正文
            return weibo_content
        except Exception as e:
            print(e)
            print("get_weibo_content error!")

    def get_one_weibo(self, info):
        """
            获取某一条微博的相关信息
        """
        try:
            weibo = OrderedDict()
            is_original = self.is_original(info)  # 是否为原创微博
            weibo['id'] = info.xpath('@id')[0][2:]  # 微博id是第2位以后的字符串
            weibo['content'] = self.get_weibo_content(
                info, is_original)  # 获取微博内容
            weibo['original'] = is_original  # 原创微博标识
            return weibo
        except Exception as e:
            print(e)
            print("get_one_weibo error!")

    def get_all_weibo(self):
        """
            获取一个html页面的全部微博
        """
        try:
            info = self.tree.xpath('//div[@class="c"]')
            is_exist = info[0].xpath('div/span[@class="ctt"]')  # 判断当前页面是否有微博
            if is_exist:
                for i in range(len(info)-2):
                    weibo = self.get_one_weibo(info[i])  # 获取一条微博的信息
                    if weibo:
                        self.weibo.append(weibo)
        except Exception as e:
            print(e)
            print("get_all_weibo error!")

    def write_txt(self):
        """
            将爬取到的微博写入txt文件中
        """
        try:
            result = []
            self.new_txt_num = 0  # 新写入txt记录个数
            """
            for k, i in enumerate(self.weibo):
                result.append('微博id: '+i['id']+'\n'+u'微博正文/转发理由: '+i['content'] +
                              '\n'+'是否原创: '+str(i['original'])+'\n\n')
                self.new_txt_num += 1  # 更新new_txt_num
            """
            for i in self.weibo:
                result.append('微博id: '+i['id']+'\n'+u'微博正文/转发理由: '+i['content'] +
                              '\n'+'是否原创: '+str(i['original'])+'\n\n')

            self.new_txt_num = len(self.weibo)
            self.wrote_num_txt = self.new_txt_num + self.wrote_num_txt  # 更新wrote_num_txt
            # print(result)
            self.result_txt = result
            self.write_result = ''.join(result)
            with open(self.to_txtname, 'a', encoding='utf-8') as f:
                f.write(self.write_result)

            print("write to .txt over!")
            print('write ' + str(self.new_txt_num) +
                  ' weibo ' + 'to .txt file!')
            print('There is already ' +
                  str(self.wrote_num_txt)+' weibo in .txt file!')
        except Exception as e:
            print(e)
            print("write_txt error!")

    def write_csv(self):
        """
            将爬取到的微博写入csv文件中
        """
        self.new_csv_num = 0  # 新写入csv记录个数
        try:
            result_headers = ['微博id', '微博正文/转发理由', '是否原创']
            result_data = [w.values() for w in self.weibo]
            # print(type(result_data))
            # print(len(result_data))
            self.new_csv_num = len(result_data)
            # print(result_data)

            with open(self.to_csvname, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                if self.wrote_num_csv == 0:
                    writer.writerows([result_headers])
                writer.writerows(result_data)
            self.wrote_num_csv = self.new_csv_num+self.wrote_num_csv
            print("write to .csv over!")
            print('write ' + str(self.new_csv_num) +
                  ' weibo ' + 'to .csv file!')
            print('There is already ' +
                  str(self.wrote_num_csv)+' weibo in .csv file!')
        except Exception as e:
            print(e)
