from collections import Counter
from email.mime import image
from PIL import Image
from wordcloud import WordCloud
from konlpy.tag import Okt
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt

class CustomWC():
    ## INIT------------------------------------------------
    def __init__(self):
        self.FONT_PATH = "/home/crawl/CustomWordCloud/BMHANNA_11yrs_ttf.ttf"
        self.MASK_PATH = "/home/crawl/CustomWordCloud/mask.png"
    ## Use Function ---------------------------------------------------
    def wordcloud_from_text(self, input_file, output_file='wordcloud.png'):
        text = self.data_to_text(input_file)
        noun_list = self.get_noun_list(text)

        if len(noun_list) < 10:
            print ('wordcloud_from_text() - Too small noun list')
            return
        
        mask = self.set_mask_from_image(self.MASK_PATH)
        wc = WordCloud(font_path = self.FONT_PATH,
                            width=860, height=860,
                            max_font_size=80,
                            max_words=100,
                            mask=mask)
        wc.generate_from_frequencies(dict(noun_list))
        wc.recolor(color_func= self.grey_color_func)
        wc.to_file(output_file)

    #-------------------------------------------------------------
    @staticmethod
    def grey_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
        return("hsl(291,68%%, %d%%)" % np.random.randint(60,100)) 

    @staticmethod
    def set_mask_from_image(image_path):
        icon =  Image.open(image_path)
        mask = np.array(icon)
        return mask

    #-------------------------------------------------------------------------------------------------------------------
    def get_noun_list(self,text, method=0):    

        if method == 0:
            # KOR
            noun = self.tokenizer_konlpy(text)
        else:
            # ENG
            noun = self.tokenizer_nltk(text)

        count = Counter(noun)
        noun_list = count.most_common(3000)
        return noun_list

    #-------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tokenizer_nltk(text):
        is_noun = lambda pos : (pos[:2] == 'NN' or pos[:2] == 'NNP')
        tokenized = nltk.word_tokenize(text)
        return [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

    #-------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tokenizer_konlpy(text):
        okt = Okt()
        return [word for word in okt.nouns(text) if len(word) >1]

    #-------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def data_to_text(data):
        text = ""
        for txt in data :
            text += "\n" + txt[1]
        return text

