import jieba
import csv
import re
import wordcloud
import matplotlib.pyplot as plt

csv_name = 'yyqx_csv.csv'  # 微博信息文件

with open(csv_name, 'r', encoding='utf-8') as f:
    """
        读取微博信息到info列表
        info: type: list
    """
    reader = csv.reader(f)
    info = [row[1:]for row in reader][1:]

with open(csv_name, 'r', encoding='utf-8') as f:
    """
        读取微博内容到content列表
        content: type: list
    """
    reader = csv.reader(f)
    content = [row[1]for row in reader][1:]

with open(csv_name, 'r', encoding='utf-8') as f:
    """
        读取微博内容到content列表
        is_original: type: list
    """
    reader = csv.reader(f)
    is_original = [row[2]for row in reader][1:]

weibo_num = len(info)  # 数据集中微博总数
original_num = is_original.count('True')  # 原创微博数量
repost_num = is_original.count('False')  # 转发微博数量

original_list = [i[0] for i in info if i[1] == 'True']  # 原创微博列表
repost_list = [i[0] for i in info if i[1] == 'False']  # 转发微博列表


def read_list_file(filename):
    """
        读取文件中内容为列表的txt文件(每行以'\n'分隔)
        如: 停用词，否定词，程度副词
        filename: 文件路径
        return:file_list type: list
    """
    file_list = [k.strip() for k in open(
        filename, encoding='utf-8').readlines() if k.strip() != '\n']
    return file_list


def read_dict_file(filename):
    """
        读取文件中内容为键值对的txt文件
        如: BosonNLP情感词典
        filename: 文件路径
        return: classify_dict tyoe: dict
    """
    classify_list = [k.strip() for k in open(
        filename, encoding='utf-8').readlines() if k.strip() != '\n']
    classify_dict = dict()
    for i in classify_list:
        if len(i.split(' ')) == 2:
            classify_dict[i.split(' ')[0]] = i.split(' ')[1]
    return classify_dict


def jieba_cut(string, stopwords):
    """
        对每一条微博进行jieba分词并去除停用词
        string: 微博 type: str
        stopwords: 停用词列表 type: list
        return: 去除停用词后的分词列表
    """
    string = string.replace(u'\xa0', u' ')  # 将\xa0字符替换为' '
    word_list = jieba.lcut(string)
    word_list = [i for i in word_list if i not in stopwords and i != ' ']
    for i in range(0, len(word_list)):
        if word_list[i] in emoji_dict.keys():
            word_list[i] = str(emoji_dict[word_list[i]])
    return word_list


# BosonNLP情感词典
BosonNLP = 'senti_dict/BosonNLP_sentiment_score/BosonNLP_sentiment_score/BosonNLP_sentiment_score.txt'
BosonNLP_dict = read_dict_file(BosonNLP)  # 读取情感词典内容到dcit中

# 否定词列表
Nega = 'senti_dict/polar_dict/nega_dict.txt'
Nega_list = read_list_file(Nega)  # 读取否定词内容到list中

# 程度副词
degree = 'senti_dict/polar_dict/degree_dict.txt'
degree_dict = read_dict_file(degree)  # 读取程度副词磁带你内容到dict中

# 停用词
stop_file = 'senti_dict/stopwords/stopwords.txt'
stopwords = read_list_file(stop_file)  # 读取程度副词词典内容到list中

# emoji词典
emoji_file = 'senti_dict/emoji_dict/emoji.txt'
emoji_dict = read_dict_file(emoji_file)   # 读取emoji词典内容到dict中

# 处理emoji_dict词典
pattern = re.compile('{(.*?)}')
for k, v in emoji_dict.items():
    emoji_dict[k] = re.findall(pattern, v)


def senti_ana(string, stopwords, BosonNLP_dict, Nega_list, degree_dict):
    """
        对文本内容进行情感分析, 返回情感得分
        string: 微博文本内容 str
        stopwords: 停用词 list
        BosonNLP_dict: 情感词典 dict
        Nega_list: 否定词词典 list
        degree_dict: 程度副词词典 dict
        return: score 情感得分
    """
    word_list = jieba_cut(string, stopwords)  # 对文本内容进行分词

    sen_word = dict()  # 情感词词典 索引为分词结果在word_list中的下标
    nega_word = dict()  # 否定词词典 同上
    degree_word = dict()  # 程度副词词典 同上

    # 对分词结果进行分类
    for i in range(len(word_list)):
        word = word_list[i]
        if word in BosonNLP_dict and word not in Nega_list and word not in degree_dict.keys():
            sen_word[i] = BosonNLP_dict[word]
        elif word in Nega_list and word not in degree_dict.keys():
            nega_word[i] = -1
        elif word in degree_dict.keys():
            degree_word[i] = degree_dict[word]

    # 计算得分
    score = 0  # 初始得分为0
    weight = 1  # 初始权重为1
    sen_index = -1  # 初始情感词索引为-1
    sen_index_list = list(sen_word.keys())  # 情感词索引列表

    for i in range(len(word_list)):
        if i in sen_word.keys():
            score += weight*float(sen_word[i])
            sen_index += 1
            if sen_index < len(sen_index_list)-1:
                for j in range(sen_index_list[sen_index], sen_index_list[sen_index+1]):
                    # 如果两相邻情感词之间有否定词
                    if j in nega_word.keys():
                        weight = -weight
                    # 如果两相邻情感词之间有程度副词
                    elif j in degree_word.keys():
                        weight *= float(degree_word[j])
            if sen_index < len(sen_index_list)-1:
                i = sen_index_list[sen_index+1]

    return score  # 返回情感得分


all_scorelist = []
for i in content:
    score = senti_ana(i, stopwords, BosonNLP_dict, Nega_list, degree_dict)
    all_scorelist.append(score)

all_filename = 'all_with_score.csv'

def write_csv(filename):
    try:
        result_headers = ['微博id', '微博正文/转发理由', '是否原创', '情感得分']
        with open('yyqx_csv.csv', 'r', encoding='utf-8') as f:
            reader=csv.reader(f)
            content = [row[:]for row in reader][1:]
        
        for i in range(0,len(content)):
            content[i].append(all_scorelist[i])

        with open(filename, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([result_headers])
            writer.writerows(content)
        
    except Exception as e:
        print(e)

write_csv(all_filename)
