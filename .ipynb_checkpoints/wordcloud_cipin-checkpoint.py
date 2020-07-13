import jieba
import csv
import wordcloud
import matplotlib.pyplot as plt


def stopwords_append(s, stopwords_list):
    """
        添加停用词
        s:停用词
        stopwords_list:停用词列表
    """
    if s not in stopwords_list:
        stopwords_list.append(s)


def word_cloud(text):
    """
        词云生成
        text:str 空格分隔的词语
    """
    wc = wordcloud.WordCloud(background_color='white',
                             width=1000,
                             height=600,
                             font_path='Consolas-with-Yahei Nerd Font.ttf')
    wc.generate(text)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    return wc

"""
if '__name__' == '__main__':
    '''
        打开微博列表文件,提取微博信息
        content: list 微博正文/转发理由
    '''
    with open('yyqx_csv.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        content = [row[1]for row in reader][1:]

    print(len(content))  # 微博总数有828条

    stopwords_list = [k.strip() for k in open(
        'stopwords.txt', encoding='utf8').readlines() if k.strip() != '\n']  # 提取停用词到列表
    print(len(stopwords_list))  # 停用词列表长度

    stopwords_append('置顶',stopwords_list)
    stopwords_append('转发理由',stopwords_list)
    stopwords_append('转发',stopwords_list)
    stopwords_append('理由',stopwords_list)
    stopwords_append('明星动态',stopwords_list)
    stopwords_append('微博视频',stopwords_list)
    stopwords_append('原图',stopwords_list)
    stopwords_append('易',stopwords_list)
    stopwords_append('烊',stopwords_list)
    stopwords_append('千玺',stopwords_list)
    stopwords_append(' ',stopwords_list)
    stopwords_append('\xa0',stopwords_list)
    stopwords_append('组图',stopwords_list)
    stopwords_append('张',stopwords_list)
    stopwords_append('',stopwords_list)
    stopwords_append('视频',stopwords_list)
    stopwords_append('http',stopwords_list)
    stopwords_append('cn',stopwords_list)
    stopwords_append('微博',stopwords_list)
    
    txt = ' '.join(content)  # 微博拼接
    word_list = jieba.lcut(txt)  # 分词
    word_list = [i for i in word_list if i not in stopwords_list]  # 剔除停用词
    print(len(word_list))  # 所有词语个数
    c = {}
    for x in word_list:  # 计数
        if len(x) > 1 and x != '\r\n' and x != ' ':
            if(x not in c):
                c[x] = 0
            else:
                c[x] += 1
    items = sorted(c.items(), key=lambda item: item[1], reverse=True)

    with open('cipin.txt', 'a', encoding='utf-8') as f:  # 存入词频文件
        for i in items:
            f.write(i[0]+'  '+str(i[1])+'\n')

    text = ' '.join(word_list)  # 词语拼接

    word_cloud(text).to_file('yyqx.jpg')
"""