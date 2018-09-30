# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 11:08:20 2018

@author: Graccolab
"""

# import librarires  
import os
import glob
import pandas as pd
import re
import gensim
from collections import defaultdict
#import operator
#import numpy as np
#import pickle


#%%
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

def convert_multiplier(nb_str):
       multipliers = { 'K': 1e3, 'k': 1e3, 'M': 1e6,'m': 1e6,'B': 1e9,'b': 1e9}
       pattern = r'([0-9.]+)([bkmBKM])'
       if re.findall(pattern, nb_str)==[]:
              nb_output=nb_str
       else:
              for number, suffix in re.findall(pattern, nb_str):
                     number = float(number)
                     nb_output = str(int(number * multipliers[suffix]))              
       return nb_output

def replace_empty(df):
       df['claps'].replace('[]','0',inplace=True)
       df['response'].replace('[]','0',inplace=True)
       return df

def replace_multiplier(df):       
       df['claps'] = df['claps'].apply(lambda x: convert_multiplier(x))
       df['response'] = df['response'].apply(lambda x: convert_multiplier(x))

       return df

def lower_tags(df):
       df['tag1']=df['tag1'].str.lower()
       df['tag2']=df['tag2'].str.lower()
       df['tag3']=df['tag3'].str.lower()
       df['tag4']=df['tag4'].str.lower()
       df['tag5']=df['tag5'].str.lower()
       df['original_tag']=df['original_tag'].str.lower()
       return df

#%%
##################################################
#Data Input
data_folder="tags_19000/data"
df=read_csv_data(data_folder)


##################################################
#Data Cleaning
# Keep only posts published in English
df.rename(inplace=True,columns={'detected language': 'detected_language'})
df=df[df.detected_language == 'en']

# Drop post duplicates, keep most recently published
df = df.sort_values('post_time').drop_duplicates(['post_id'], keep='last')
df.reset_index(inplace=True)
df.sort_values('index',inplace=True)

# Replace empty by 0, change format of number of responses & claps
df=replace_empty(df)
df=replace_multiplier(df)
df=lower_tags(df)

# Get sequences of tags
tags = df[['tag1','tag2','tag3','tag4','tag5']]
tag_list=tags.get_values()
tag_list=tag_list.tolist()

#####################################################
# Cleaning step for word2vec
# Calculate frequency of tokens
frequency = defaultdict(int)
for tag_row in tag_list:
       for tag in tag_row:
              frequency[tag] += 1
# Keep tag in frequency >1
tag_list = [[token for token in tag_row if frequency[token] > 1] for tag_row in tag_list]
# Remove floats from list (nan values)
tag_list=[[tag for tag in tag_row if type(tag)!= float] for tag_row in tag_list]


###################################################     
# Create Word2Vec model
model = gensim.models.Word2Vec(tag_list)
#       size=150,
#        window=10,
#        min_count=2,
#        workers=10)
model.save("word2vec_tag.model")
model.train(tag_list, total_examples=len(tag_list), epochs=10)
model.save("word2vec_tag.model")

# Try model with query
tag_query='data science'
most_similar_10=model.wv.most_similar(tag_query)
most_similar_10=model.wv.most_similar("code")
most_similar_100=model.wv.most_similar("code",topn=100)

#model.wv.closer_than('data science','python')

toto=model.accuracy()
print(most_similar_10)
most_similar_10.hist()

model = gensim.models.Word2Vec.load("word2vec_tag.model")
model.wv.most_similar(tag_query)
# => include most_similar_10 in falsk
# => 
titi=model.wv.most_similar("dog")
print(titi)
# PLOT RESULTS


#    Finding the degree of similarity between two words.
#    model.similarity('woman','man')
#    0.73723527
#    Finding odd one out.
#    model.doesnt_match('breakfast cereal dinner lunch';.split())
#    'cereal'
#    Amazing things like woman+king-man =queen
#    model.most_similar(positive=['woman','king'],negative=['man'],topn=1)
#    queen: 0.508
#    Probability of a text under the model
#    model.score(['The fox jumped over the lazy dog'.split()])
#    0.21



# Data Exploration:
#dictionary = gensim.corpora.Dictionary(tag_list)
#dictionary.save('test_tags.dict')  # store the dictionary, for future reference
#print(dictionary)
#corpus = [dictionary.doc2bow(tag_row) for tag_row in tag_list]
#gensim.corpora.MmCorpus.serialize('test_tags.mm', corpus)  # store to disk, for later use


#######################################
# For a memory friendly version
#with open('tag_list.txt', 'w',encoding='utf-8-sig') as file_handler:
#    for item in tag_list:
#        file_handler.write("{}\n".format(item))
#        
#class MyCorpus(object):
#    def __iter__(self):
#        for line in open('tag_list.txt',encoding='utf-8-sig'):
#            # assume there's one document per line, tokens separated by whitespace
#            yield dictionary.doc2bow(line.lower().split())
#           
#corpus_memory_friendly = MyCorpus()  # doesn't load the corpus into memory
#print(corpus_memory_friendly)
## if we want to see the corpus
#for vector in corpus_memory_friendly:  # load one vector into memory at a time
#      print(vector)      
#######################################

      
#dictionary = gensim.corpora.Dictionary.load('test_tags.dict')
#corpus = gensim.corpora.MmCorpus('test_tags.mm')