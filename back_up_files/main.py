from weibo_spider import wb_spider
from html_parser import html_parser
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
    """
    to_txtfile = 'yyqx_txt.txt'
    to_csvfile = 'yyqx_csv.csv'

    """
    filenamelist = []
    for i in range(1, 83+1):
        filenamelist.append('yyqx_txt/yyqx_'+str(i)+'.txt')
    # print(filenamelist)
    """

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