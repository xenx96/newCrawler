#Library
import pandas as pd
import numpy as np
import time

#Personal Module
import crawling.crawling as c
import word.socialNetworkAnalysis as sna
import word.wordcloud as wc

#Do Main()
def main():
    do_crawling_save("스탠다드에너지",10)

#Crawler
"""
    setQuery(self,query): default is 배터리 this is keyword for search

    setPage(self,page): If you want to change page for getting data in other page, you'll use setPage
    
    setSearchURL(self,url): Default is Naver, If you want others, Change SearchURL

    setTags(self,tags): default is a tags.
    
    setClassname(self,cn): default is news_tit
"""
def do_crawling_save(query, maxPage):
    craw = c.NewsSearcher()

    ## DataFrame Setting
    headers = ["title", "url"]
    data = pd.DataFrame(columns = headers)

    ##Query Setting
    craw.setQuery(query)

    for i in range(0,maxPage):
        page = str(i)+"1"
        craw.setPage(page)
        
        #Get Search dataf
        title,url,time = craw.get_contents()
        title = pd.DataFrame(title, columns=["title"])
        url = pd.DataFrame(url, columns=["url"])
        time = pd.DataFrame(time, columns=["time"])
        
        #Bind data
        rows = columBind(title, url)
        rows = columBind(rows, time)
        data = pd.concat([data, rows])

    fname = set_filename(query)
    #Write.csv
    data.to_excel(fname, encoding="utf-8", index=False)
    print("Complete to save crawling-data")

def columBind(data1,data2):
    return pd.concat([data1,data2],axis=1)

def set_filename(keyword):
    year = time.localtime().tm_year
    mon = time.localtime().tm_mon
    day = time.localtime().tm_mday

    return "{}-{}-{} {}.xlsx".format(year, mon, day, keyword)
    
main()