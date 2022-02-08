import datetime
import time
import psycopg2

class ContentsDB():
    #--------------------------------------------------------------
    @staticmethod
    def connect():
        connection = psycopg2.connect(host="localhost", dbname="postgres",
        user='root', password ='admin')
        return connection
    #-------------------------------------
    def execute(self, sql, params={}):
        with self.connect() as connection :
            with connection.cursor() as cursor:
                cursor.execute(sql,params)

    def insertContents(self,data):
        sql = '''
        INSERT INTO news_contents.contents(keyword,title,url,date)
        VALUES  (unnest( %(keyword)s),
                unnest( %(title)s),
                unnest( %(url)s),
                unnest( %(date)s))
                ON CONFLICT (url) 
                DO NOTHING'''

        keyword =[df['keyword'] for df in data]
        title =[df['title'] for df in data]
        url =[df['url'] for df in data]
        date =[df['date'] for df in data]
        self.execute(sql, locals())

    def getContents(self,keyword,file_name):
        sql = '''
        SELECT * FROM news_contents.contents
        WHERE keyword = {};
        '''.format(keyword)

        cursor = self.connect().cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return data