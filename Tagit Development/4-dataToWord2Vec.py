# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 11:08:20 2018
Lline - Insight Project 
       Prepare Data for tag embedding using word2vec,  train and save model
       - Load Data
       - Clean Data:
              - Keep only posts published in English
              - Drop post duplicates, keep most recently published
              - Replace empty by 0, change format of number of responses & claps
       - Get sequences of tags
       - Identify tags with missing follower number
       - Cleaning step for word2vec
       - Train and save word2vec model
  
@author: Lline
"""


##############################################################################
#Import libraries
import os
import glob
import pandas as pd
import re
import gensim
from collections import defaultdict 
import pickle


##############################################################################
# INPUT
#Data Input

#data_folder="tags_19000/data" # version 1 - pop
data_folder="data science v2/data" # version 2 - DS
#data_folder="combined/data" # version 3 - DS+pop

#pickle_raw_df_name="raw_df_pop" # version 1 - pop
pickle_raw_df_name="raw_df_DS" # version 2 - DS
#pickle_raw_df_name="raw_df_combined"  # version 3 - DS+pop

#pickle_df_name="df_pop" # version 1 - pop
pickle_df_name="df_DS" # version 2 - DS
#pickle_df_name="df_combined"  # version 3 - DS+pop


# if necessary picckle.load your raw_df
#fileObject = open(pickle_raw_df_name,'rb')  
#raw_df = pickle.load(fileObject)  

##############################################################################
# local FUNCTIONS
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


##################################################
# Load Data
df=read_csv_data(data_folder)
fileObject = open(pickle_raw_df_name,'wb') 
pickle.dump(df,fileObject)   
fileObject.close()

##################################################
# Raw Data Cleaning
# Raw Data (df) -> Cleaned Data (df)

# Keep only posts published in English
df.rename(inplace=True,columns={'detected language': 'detected_language'})
df=df[df.detected_language == 'en']
#
## Drop post duplicates, keep most recently published
df = df.sort_values('post_time').drop_duplicates(['post_id'], keep='last')
df.reset_index(inplace=True)
df.sort_values('index',inplace=True)
#
## Replace empty by 0, change format of number of responses & claps
df=replace_empty(df)
df=replace_multiplier(df)
df=lower_tags(df)

#pickle df
fileObject = open(pickle_df_name,'wb') 
pickle.dump(df,fileObject)   
fileObject.close()

fileObject = open(pickle_df_name,'rb')  
df = pickle.load(fileObject)  

#%%
##################################################
# Get sequences of tags
# Cleaned Data (df) -> tag_list
tags = df[['tag1','tag2','tag3','tag4','tag5']]
tag_list=tags.get_values()
tag_list=tag_list.tolist()
tag_list = [[token for token in tag_row if str(token)!='nan'] for tag_row in tag_list]

#####################################################
# Cleaning step for word2vec
# Calculate frequency of tokens
tag_frequency = defaultdict(int)
for tag_row in tag_list:
       for tag in tag_row:
              tag_frequency[tag] += 1

################### START OF INTERMEDIATE STEP : IDENTIFY MISSING FOLLOWER NUMBER ##################################
## Intermediate step : get list of tags with no tag follower number pickle them for future use
# get tags with no TF whose frequency > frequency criteria
              
outputFileName="missingTFF2"
frequencyCriteria=2
currentDictionary="follower_nb_dictionnary"
dictObject=open(currentDictionary,'rb') # get current dictionary
dict_follower = pickle.load(dictObject)    

frequent_tag_list = [[token for token in tag_row if tag_frequency[token] ==frequencyCriteria ] for tag_row in tag_list]
frequent_tag_frequency = defaultdict(int)
for tag_row in frequent_tag_list:
       for tag in tag_row:
              frequent_tag_frequency[tag] += 1
              
count_yes=0
count_no=0
for tag in frequent_tag_frequency.keys():
       if tag in dict_follower.keys():
              count_yes=count_yes+1
       else:
              count_no=count_no+1
print(count_yes) # nb of tags in tag embedding that dt have number of tag follower
print(count_no)

# keep tag that do not have TFN and have a certain frequency
missingTagFollowerFrequent=[tag for tag in frequent_tag_frequency.keys() if tag not in dict_follower.keys()]
fileObject = open(outputFileName,'wb') 
pickle.dump(missingTagFollowerFrequent,fileObject)   
fileObject.close()
###################END INTERMEDIATE STEP##################################


# Keep tag if frequency >2 in tag_list (for word2vec)
tag_list_filtered = [[token for token in tag_row if tag_frequency[token] > 2] for tag_row in tag_list]

#tag_frequency = defaultdict(int)
#for tag_row in tag_list_filtered:
#       for tag in tag_row:
#              tag_frequency[tag] += 1



###################################################     
# Create Word2Vec model

model_ouput_name="word2vec_pop_tag.model" # version1
#model_ouput_name="word2vec_DS_tag.model" # version2
#model_ouput_name="word2vec_combined_tag.model" # version3

   
model = gensim.models.Word2Vec(tag_list_filtered)
model.save(model_ouput_name)
model.train(tag_list_filtered, total_examples=len(tag_list_filtered), epochs=10)
model.save(model_ouput_name)


###################################################     
# Exploration of model:
#print(model)

## Try model with query
#tag_query='data science'
#most_similar_10=model.wv.most_similar(tag_query)
#print(most_similar_10)
#most_similar_10=model.wv.most_similar("code")
#print(most_similar_10)
#most_similar_100=model.wv.most_similar("code",topn=100)
#print(most_similar_100)
##model.wv.closer_than('data science','python')

#model = gensim.models.Word2Vec.load("word2vec_tagDS.model")
#model.wv.most_similar(tag_query)

