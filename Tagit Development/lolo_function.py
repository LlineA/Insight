# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:52:17 2018

@author: Graccolab
"""

import pickle
import gensim
import os
from wordcloud import WordCloud
import datetime
#import cv2
import matplotlib.pyplot as plt
def rename(file_beginning,dir_name):
       current_time=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
       old_filename = [filename for filename in os.listdir(dir_name) if filename.startswith(file_beginning)][0]
       new_filename = file_beginning + current_time + old_filename[-4:]
       os.rename(dir_name + "/" + old_filename, dir_name + "/" + new_filename)
       return new_filename

def get_dictionary(dict_name):
       fileObject = open(dict_name,'rb')  
       dict_df_follower = pickle.load(fileObject)  
       fileObject.close()  
       return dict_df_follower

def find_ten_neighbours(tag):
       neighbours=[]             
       return neighbours

def human_format(num):
       num = float('{:.3g}'.format(num))
       magnitude = 0
       while abs(num) >= 1000:
              magnitude += 1
              num /= 1000.0
       return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def load_model(model_name):
        model = gensim.models.Word2Vec.load(model_name)
        return model
 
def most_similar(input_tag,model,neighbour_nb):    
       most_similar_tags=model.wv.most_similar(input_tag,topn=neighbour_nb)      
       return most_similar_tags

def find_more_popular_tags(tag_output,input_follower_nb,tag_follower_dict):
       better_choices={}
       for tag in tag_output:
              if tag[0] in tag_follower_dict:
                     tag_follower_temp=int(tag_follower_dict[tag[0]])
              else:
                     tag_follower_temp=0
              if tag_follower_temp>input_follower_nb:
                     better_choices[tag[0]]=tag_follower_temp             
       return better_choices


def create_word_cloud(better_choices):
       # deleter current wc images:
       dir_name='flask_tagit/static/'
       file_beginning='wc_'
       wc_filenames = [filename for filename in os.listdir(dir_name) if filename.startswith(file_beginning)]
       for file in wc_filenames:
              os.remove(dir_name+file)    
              
       wordcloud_img = WordCloud(margin=0,prefer_horizontal=1, min_font_size=16,
                                 relative_scaling=1,normalize_plurals=False, background_color="white")
       wordcloud_img=wordcloud_img.fit_words(better_choices)
       
       current_time=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
       file_name='wc_'+current_time+'.png'
       file_path='flask_tagit/static/' + file_name
       wordcloud_img.to_file(file_path)
#       plt.imshow(wordcloud_img, interpolation='bilinear')
#       plt.axis("off")
#       plt.margins(x=0, y=0)
#       plt.savefig(file_path)
       
       return file_name
