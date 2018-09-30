# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 18:47:08 2018

@author: Graccolab
"""
import os
import glob
import pandas as pd
#import re
import gensim
from collections import defaultdict

def read_csv_data(data_folder):
    list_df_s = []
    path_data = "data/%s" %data_folder
    list_csv = os.listdir(path_data)

    # loop over csv_files
    for csv in list_csv:
        # retrieve csv file
        path_csv = glob.glob(os.path.join(path_data+"/"+csv))[0]
        print(path_csv)
        # append to dataframe list if not empty
        list_df_s.append(pd.read_csv(path_csv,index_col=None, header=0,engine="python",encoding='utf-8-sig'))

    # concatenate dataframes and return
    return pd.concat(list_df_s)
data_folder="data science v1"
df=read_csv_data(data_folder)# Add an index, display unique values , count unique post values etc.
df.rename(inplace=True,columns={'detected language': 'detected_language'})
df=df[df.detected_language == 'en']
df.reset_index(inplace=True)
df.rename(inplace=True,columns={'index': 'indexOriginal'})
df.nunique()
df.groupby('original_tag').agg(['count', 'size', 'nunique']).stack()
df['post_id'].agg(['count', 'size', 'nunique'])


# Get tags from 5 columns of tags and Concatenate all tags to list of unique tags
allTags=pd.concat([df['tag1'],df['tag2'],df['tag3'],df['tag4'],df['tag5']])
allTags.nunique()
allTags=allTags.str.lower()
allTags=pd.Series(data=allTags.unique()).tolist()


##########################################
#####################################

#import gensim
#def load_model():
#        model = gensim.models.Word2Vec.load("word2vec_tag.model")
#        return model
#model=load_model()
#word_vectors = model.wv
#         
#for key,element in word_vectors.vocab.items(): 
#       #print(key)
#       if key in dict_df_follower:
#              print(key)

#better_choices=find_more_popular_tags(tag_output,input_follower_nb,dict_df_follower)
#print(better_choices)

