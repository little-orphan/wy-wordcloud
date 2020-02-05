#!/usr/bin/env python
# coding: utf-8


import requests
from lxml import etree
import os
import time
import re


import functools
class RMRB:
    def __init__(self,year_start,year_end):
        self.year_start = year_start
        self.year_end = year_end
        print("./RMRB/Durl404.txt：因网络问题未能成功爬取的目录url\n./RMRB/Aurl404.txt: 因网络问题未能成功爬取的文章url")
        print("* 当出现大量的404错误时，说明网络连接很差，需删除已爬文本,并重新运行程序。或在完成后自行处理Durl404.txt与 Aurl404.txt")
        print("* start...")
    
    def minDistance(self, word1, word2):
            n1 = len(word1)
            n2 = len(word2)
            dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]
            # 第一行
            for j in range(1, n2 + 1):
                dp[0][j] = dp[0][j-1] + 1
            # 第一列
            for i in range(1, n1 + 1):
                dp[i][0] = dp[i-1][0] + 1
            for i in range(1, n1 + 1):
                for j in range(1, n2 + 1):
                    if word1[i-1] == word2[j-1]:
                        dp[i][j] = dp[i-1][j-1]
                    else:
                        dp[i][j] = min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1] ) + 1
            #print(dp)
            return dp[-1][-1]
    
    def text_match(self,title,text):
        """ 默认第1行为版面名，第2行为专栏名，从第3行匹配标题 """
        assert type(title) == str
        assert type(text) == list
        if len(text) <= 2:
            return text
        
        title = ''.join(filter(lambda c: c>='\u4e00' and c <= '\u9fa5',title))
        if title == "图片":
            return text[2:]
        title = title.replace("图片",'')
        
        min_MED,min_MED_index = 999,0
        for tail_index in range(2,min(6,len(text))):
            tail_text = ''.join(text[2:tail_index+1])
            tail_text = ''.join(filter(lambda c: c>='\u4e00' and c <= '\u9fa5',tail_text))
            tail_text = tail_text.replace("图片",'')
            MED = self.minDistance(title,tail_text)
            min_MED,min_MED_index = [MED,tail_index] if MED < min_MED else [min_MED,min_MED_index]
            
        return text[min_MED_index+1:]
    
    def getPageName(self,text):
        assert type(text) == list
        if len(text) == 0:
            return ''
        
        page_name = re.findall(r'\(.*\)',text[0].strip())
        if page_name:
            page_name = page_name[0][1:-1]
            if page_name:
                return page_name
        return ''

    def getColumnName(self,text):
        assert type(text) == list
        if len(text) <= 1:
            return ''
        
        column_name = re.findall(r'：.*',text[1].strip())
        if column_name:
            column_name = column_name[0][1:]
            if column_name:
                return column_name
        return ''
    
    def preprocess(self):
        if not os.path.isdir("RMRB"):
            os.makedirs("RMRB")
    
    def start(self):
        for year in range(self.year_start,self.year_end+1):
            with open("RMRB\Durl404.txt","a") as fd404,open("RMRB\Aurl404.txt","a") as fa404,open("RMRB\RMRB_"+str(year)+ ".txt","a") as f:
                print(str(year)+': ',end="",flush=True)
                for month in range(1,13):
                    for day in range(1,32):
                            f.write("RMRB_{}{}{}\n".format(str(year),str(month) if month>9 else '0'+str(month),str(day) if day>9 else '0'+str(day)))
                        
                            url = "http://www.laoziliao.net/rmrb/" + str(year) + "-" + str(month) + "-" + str(day)

                            try:
                                response = requests.get(url)
                            except:
                                print("404 Skip the directory url： ",url)
                                fd404.write(url+'\n')
                                time.sleep(2)
                                continue

                            if response.status_code == 500:
                                continue

                            tree = etree.HTML(response.text)
                            article_urls = tree.xpath('//*[@id="box"]/div[1]/div/ul/li[1]/a/@href')

                            for page,article_url in enumerate(article_urls):
                                f.write("Page_{}\n".format(str(page+1) if page+1>9 else '0'+str(page+1)))
                            
                                try:
                                    article_response = requests.get(article_url)
                                except:
                                    print("404 Skip the article url： ",article_url)
                                    fa404.write(article_url+'\n')
                                    time.sleep(2)
                                    continue

                                article_tree = etree.HTML(article_response.text)
                                title_list = article_tree.xpath('//*[@id="box"]/div[1]/div/h2//text()')
                            
                                for article_num ,title in enumerate(title_list):
                                    locator = '//*[@id="box"]/div[1]/div/div[{}]//text()'.format(str(article_num+1))
                                    text = article_tree.xpath(locator)
                                    
                                    if article_num == 0:
                                        page_name = self.getPageName(text)
                                        if page_name:
                                            f.write("Page_name: {}\n".format(page_name))
                                    
                                    f.write("Article_{}\n".format(str(article_num+1) if article_num+1>9 else '0'+str(article_num+1)))
                                    
                                    column_name = self.getColumnName(text)
                                    if column_name:
                                        f.write("Column_name: {}\n".format(column_name))
                                       
                                    f.write("Title_:{}\n".format(title))

                                    text = self.text_match(str(title),text)
                                    text = '_p_'.join(text).strip()
                                    f.write("Text_:{}\n".format(text))
                            f.write('\n')            
                    f.write('\n')
                    print(str(month)+"; ",end="",flush=True)
                print()

def main():
    rmrb = RMRB(1989, 1989)
    rmrb.preprocess()
    rmrb.start()
    print("FINISHED")
    
if __name__ == "__main__":
    main()





