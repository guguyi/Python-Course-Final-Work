import requests
import re
import time
from bs4 import BeautifulSoup
from lxml import etree


def emoji_spider(url):
    """
        爬取emoji页面
        url: emoji页面的url
        return: tree lxml.etree._Element类型对象
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        html = r.text
        tree = etree.HTML(html)
        return tree
    except Exception as e:
        print("spider failed")
        print(e)


def html_parser(tree):
    """
        解析抓取的html页面
        tree: lxml.etree._Element类型对象
        return: chinese, dict type: list
    """
    chinese = tree.xpath('//td[2][@class]/a[@href]/text()')
    emoji = tree.xpath('//td[3][@class]/a[1][@href]/text()')
    return chinese, emoji


def get_emoji_dict():
    """
        return: eomji_dict emoji字典
    """
    emoji_dict = dict()
    for offset in range(0, 11):
        url = 'https://hanyucidian.18dao.cn/emoji?page=0'+str(offset)
        tree = emoji_spider(url)
        chinese, emoji = html_parser(tree)
        for i in range(0, len(emoji)):
            try:
                if emoji[i] not in emoji_dict:
                    emoji_dict[emoji[i]] = set()
                    emoji_dict[emoji[i]].add(chinese[i])
                else:
                    emoji_dict[emoji[i]].add(chinese[i])
            except Exception as e:
                print(e)
        print('page '+str(offset) + ' get emoji over!')
        time.sleep(2)
    return emoji_dict

def write_to_txt():
    """
        写入txt文件
    """
    emoji_file='senti_dict/emoji_dict/emoji.txt'
    emoji_dict=get_emoji_dict()
    with open(emoji_file,'a',encoding='utf-8') as f:
        for k,v in emoji_dict.items():
            f.write(str(k)+' '+str(v)+'\n')

# write_to_txt()