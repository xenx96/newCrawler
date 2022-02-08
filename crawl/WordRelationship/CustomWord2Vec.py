from gensim.models import Word2Vec
import logging

def get_processed_data(origin_df, start_date, end_date):
    query = origin_df[(origin_df.Date_Time >= start_date) & (origin_df.Date_time <= end_date)]
