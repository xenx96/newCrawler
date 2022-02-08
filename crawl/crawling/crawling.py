from bs4 import BeautifulSoup
import requests
import time

class NewsSearcher():
    """
    setQuery(self,query): default is 배터리 this is keyword for search

    setPage(self,page): If you want to change page for getting data in other page, you'll use setPage
    
    setSearchURL(self,url): Default is Naver, If you want others, Change SearchURL

    setTags(self,tags): default is a tags.
    
    setClassname(self,cn): default is news_tit
    """
    def __init__(self) :
        self.searchURL = "https://search.naver.com/search.naver?where=news&query={}&sm=tab_opt&start={}&sort=1&photo=0&field=0" # &pd=4 //4는 1일 2는 1개월
        self.query = "배터리"
        self.page = "1"
        self.url = self.searchURL.format(self.query,self.page)
        self.tag = "a"
        self.cn = "news_tit"
        print("Default setting is naver news search.")
        
#Get Self -----------------------------
    def getQuery(self) :
        return self.query

    def getPage(self):
        return self.page

    def getURL(self):
        return self.url

#Set Self ------------------------------
    def setQuery(self, query):
        self.query = query
        self.url = self.searchURL.format(query, self.page)

    def setPage(self, page):
        self.page = page
        self.url = self.searchURL.format(self.query, page)
    
    def setSearchURL(self, url):
        self.searchURL = url
        self.url = url.format(self.query, self.page)

    def setTags(self, tag):
        self.tag = tag
    
    def setClassname(self, cn):
        self.cn = cn

# Method
    def get_contents(self):
        content = self.getHTML()        
        soup = BeautifulSoup(content, "html.parser")
        rows = soup.find_all(self.tag, 
                                class_=self.cn) 
        title = self.getText(rows)
        url = self.getNewsAddress(rows)
        time = self.getNewsTime(soup)
        
        return title, url, time
    
    def getHTML(self):
        return requests.get(self.url).content

    @staticmethod
    def getText(element):
        rows = []
        for el in element :
            ary = []
            ary.append(el.text)
            rows.append(ary)

        return rows

    @staticmethod
    def getNewsAddress(element):
        rows = []
        for el in element :
            ary = []
            ary.append(el.attrs["href"])
            rows.append(ary)

        return rows

    def getNewsTime(self,soup):
        element = soup.find_all("span", 
                                class_="info") 
        rows = []
        for el in element :
            if el.text.find("면") >= 0:
                continue

            ary = []
            value = self.str_convert_to_time(el.text)
            ary.append(value)
            rows.append(ary)

        return rows
     
    def str_convert_to_time(self, value):
        year, mon, day, hour, min = self.get_time_now()
        
        if value.find("분") >= 0:
           t = int(value.replace("분 전", ""))
           min -= t
        
        if value.find("시간") >= 0:
            t = int(value.replace("시간 전", ""))
            hour -= t
        
        if value.find("일") >= 0:
            t = int(value.replace("일 전", ""))
            day -= t


        return self.set_news_time(year, mon, day, hour, min)
    
    @staticmethod
    def get_time_now():
        year = time.localtime().tm_year
        mon = time.localtime().tm_mon
        day = time.localtime().tm_mday
        hour = time.localtime().tm_hour
        min = time.localtime().tm_min

        return year,mon,day,hour,min
    
    @staticmethod
    def set_news_time(year, mon, day, hour, min):
        
        if min < 0 :
            hour -= 1
            min = 60 + min

        if hour < 0 :
            day -= 1
            hour = 24 + hour
        
        if day <= 0 :
            mon -= 1
            day = 30 + day
        
        if mon <= 0 :
            year -= 1
            mon = 12 + mon

        return "{}.{}.{}".format(year, mon, day)
