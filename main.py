from weibo_spider import wb_spider
from html_parser import html_parser
from wordcloud_cipin import *
import time


if __name__ == '__main__':
    """
    wb=wb_spider('tfyiyangqianxi','yyqx')
    print(wb.url)
    print(wb.url0)
    wb.get_pagenum()
    print(wb.pagenum)
    wb.filenaming()
    wb.get_html() 

    to_txtfile = 'yyqx_txt.txt'
    to_csvfile = 'yyqx_csv.csv'


    filenamelist = []
    for i in range(1, 83+1):
        filenamelist.append('yyqx_txt/yyqx_'+str(i)+'.txt')
    # print(filenamelist)


    wrote_num_txt = 0
    wrote_num_csv = 0
    page = 0


    for page in range(1, 84):
        filename = ('yyqx_txt/yyqx_'+str(page)+'.txt')
        hp = html_parser(filename, to_txtfile, to_csvfile,
                         wrote_num_txt, wrote_num_txt)
        # print(wrote_num_csv)
        hp.get_tree()
        hp.get_all_weibo()
        hp.write_txt()
        hp.write_csv()
        wrote_num_txt = hp.wrote_num_txt
        wrote_num_csv = hp.wrote_num_csv
        # print(page)
        # print(hp.new_csv_num)
        # print(wrote_num_csv)

    
    with open('yyqx_csv.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        content = [row[1]for row in reader][1:]

    print(len(content))  # 微博总数有828条

    stopwords_list = [k.strip() for k in open(
        'stopwords.txt', encoding='utf8').readlines() if k.strip() != '\n']  # 提取停用词到列表
    print(len(stopwords_list))  # 停用词列表长度
    stopwords_append('置顶', stopwords_list)
    stopwords_append('转发理由', stopwords_list)
    stopwords_append('转发', stopwords_list)
    stopwords_append('理由', stopwords_list)
    stopwords_append('明星动态', stopwords_list)
    stopwords_append('微博视频', stopwords_list)
    stopwords_append('原图', stopwords_list)
    stopwords_append('TFBOYS', stopwords_list)
    stopwords_append('易', stopwords_list)
    stopwords_append('烊', stopwords_list)
    stopwords_append('千玺', stopwords_list)
    stopwords_append(' ', stopwords_list)
    stopwords_append('\xa0', stopwords_list)
    stopwords_append('组图', stopwords_list)
    stopwords_append('张', stopwords_list)
    stopwords_append('', stopwords_list)
    stopwords_append('视频', stopwords_list)
    stopwords_append('http', stopwords_list)
    stopwords_append('cn', stopwords_list)
    stopwords_append('微博', stopwords_list)
    txt = ' '.join(content)  # 微博拼接
    word_list = jieba.lcut(txt)  # 分词
    word_list = [i for i in word_list if i not in stopwords_list]  # 剔除停用词
    print(len(word_list))  # 所有词语个数
    c = {}
    for x in word_list:  # 计数
        if len(x) > 1 and x != '\r\n' and x != ' ':
            if(x not in c):
                c[x] = 1
            else:
                c[x] += 1
    items = sorted(c.items(), key=lambda item: item[1], reverse=True)

    with open('cipin.txt', 'a', encoding='utf-8') as f:  # 存入词频文件
        for i in items:
            f.write(i[0]+'  '+str(i[1])+'\n')
            
    with open('new_stopwords.txt', 'a', encoding='utf-8') as f:
        for i in stopwords_list:
            f.writelines(i)

    text = ' '.join(word_list)  # 词语拼接

    word_cloud(text).to_file('yyqx.jpg')
    """
