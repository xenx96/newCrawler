#Library
import pandas as pd
import time
import numpy as np
#Personal Module
import crawling.crawling as c
import CustomWordCloud.wc as wc
import db.newsContents as db_news

#Do Main()
def main(keyword,page):
    do_crawling_save(keyword,page)
    make_wordclud(keyword)

#Crawler---------------------------------------------------------
def do_crawling_save(query, max_page):
    craw = c.NewsSearcher()

    ## DataFrame Setting
    headers = ["title", "url"]
    data = pd.DataFrame(columns = headers)

    ##Query Setting
    craw.setQuery(query)
    data = []
    for i in range(0,max_page):
        page = str(i)+"1"
        craw.setPage(page)
        
        title,url,news_time = craw.get_contents()
        data = make_ary_json(data,query,title,url,news_time)

    save_db(data)
    print("Complete to save crawling-data")

# Cbind with pd.DataFrame
def colum_bind(data1,data2):
    return pd.concat([data1,data2],axis=1)

def save_db(data):
    db = db_news.ContentsDB()
    db.insertContents(data)

def make_ary_json(ary,query,title,url,news_time):
    dt = ary
    keyword = check_keyword_num(query)
    for i in range(len(title)):
        data = {"keyword" : keyword, "title":title[i][0], 
                    "url":url[i][0], "date":news_time[i][0]}
        dt.append(data)

    return dt

def check_keyword_num(query):
    keyword = 0
    if query == "스탠다드에너지" :
        keyword = 1
    if query == "배터리" :
        keyword = 2
    if query == "바나듐이온배터리" :
        keyword = 3
    return keyword
    
#Date + filename -----------------------------------------------
def set_filename(keyword):
    year = time.localtime().tm_year
    mon = time.localtime().tm_mon
    day = time.localtime().tm_mday

    return "{}-{}-{} {}".format(year, mon, day, keyword)

## Using WordCloud
def make_wordclud(data):
    file_name = set_filename(data)
    now = file_name.replace("-",".")
    db = db_news.ContentsDB()
    keyword = check_keyword_num(data)
    input_file = db.getContents(keyword,now)
    
    WC = wc.CustomWC()
    WC.wordcloud_from_text (
        input_file = input_file,
        output_file = "../public/wordcloud/{}.png".format(file_name),
        )
    print("wordcloud")


main("배터리",100)
main("스탠다드에너지",100)
main("바나듐이온배터리",100)