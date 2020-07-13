# Python-Course-Final-Work

## emotion anaysis

### Folders

| 文件夹        | 备注                                                         |
| ------------- | ------------------------------------------------------------ |
| senti_dict    | 情感词典 包含BosonNlp，停用词词典，否定词词典，程度副词词典，emoji词典等 |
| *_txt         | 爬取到的html源码(.txt文件 encoding='utf-8')(*为用户名缩写 lfq:老番茄 yyqx:易烊千玺) |
| *_html        | 爬取到的html源码(.html文件 encoding='utf-8') 便于xpath解析   |
| *_jpg         | 用户数据分析所得的词云图、直方图等                           |
| back_up_files | 课程设计过程中涉及到的历史代码、文件集合(用于回滚)           |

### .csv files

| 文件名                   | 备注                           |
| ------------------------ | ------------------------------ |
| lfq_csv.csv              | 老番茄的微博爬虫结果           |
| lfq_with_score.csv       | 老番茄的情感分析结果           |
| lfq_with_score_mark.csv  | 人工标记的老番茄情感分析结果   |
| yyqx_csv.csv             | 易烊千玺的微博爬虫结果         |
| yyqx_with_score.csv      | 易烊千玺的情感分析结果         |
| yyqx_with_score_mark.csv | 易烊千玺的人工标记情感分析结果 |

### .txt files

| 文件名         | 备注                   |
| -------------- | ---------------------- |
| lfq_txt.txt    | 老番茄的微博爬虫结果   |
| cipin_lfq.txt  | 老番茄的词频分析       |
| yyqx_txt.txt   | 易烊千玺的微博爬虫结果 |
| cipin_yyqx.txt | 易烊千玺的词频分析     |
| stopwords.txt  | 初始停用词文件         |

lfq_txt.txt:老番茄的微博爬虫结果
cipin_lfq.txt:老番茄的词频分析
yyqx_txt.txt:易烊千玺的微博爬虫结果
cipin_yyqx.txt:易烊千玺的词频分析
stopwords.txt:初始停用词文件

### .py files

| 文件名            | 备注                                                    |
| ----------------- | ------------------------------------------------------- |
| weibo_spider.py   | 微博爬虫类 爬取微博页面(需添加自己的cookies)            |
| html_parser.py    | 页面解析类 解析html页面，爬取微博到.csv文件和.txt文件中 |
| get_emoji_dict.py | 爬emoji与汉语对照表                                     |