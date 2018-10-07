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
# INPUT/OUTPUT

data_path= "2 - input data - csv"

# version 1 - pop
#data_folder= data_path + "/tags_19000/data" 
#pickle_raw_df_name="raw_df_pop" # 
#pickle_df_name="df_pop" 
#model_ouput_name="word2vec_pop_tag.model" 

# version 2 - ds
data_folder= data_path + "/data science v2/data"
pickle_raw_df_name="raw_df_ds"
pickle_df_name="df_ds"
model_ouput_name="word2vec_ds_tag.model" 

# version 3 - ds+pop
#data_folder= data_path + "/combined" 
#pickle_raw_df_name="raw_df_combined" 
#pickle_df_name="df_combined"  
#model_ouput_name="word2vec_combined_tag.model" 

# Uncomment to load pickled object
#file_object = open(pickle_raw_df_name,'rb')  
#raw_df = pickle.load(file_object)  

#%%
##############################################################################
# local FUNCTIONS
def read_csv_data(data_folder):
    list_df_s = []
    path_data = "%s" %data_folder
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

def convert_multiplier(str_nb):
       multipliers = { 'K': 1e3, 'k': 1e3, 'M': 1e6,'m': 1e6,'B': 1e9,'b': 1e9}
       pattern = r'([0-9.]+)([bkmBKM])'
       if re.findall(pattern, str_nb)==[]:
              output_nb=str_nb
       else:
              for number, suffix in re.findall(pattern, str_nb):
                     number = float(number)
                     output_nb = str(int(number * multipliers[suffix]))              
       return output_nb

def replace_empty_in_df_columns(df,column_names):
       for column in column_names:
             df[column].replace('[]','0',inplace=True)
       return df

def replace_multiplier_in_df_columns(df,column_names):  
       for column in column_names:
              df[column]=df[column].apply(lambda x: convert_multiplier(x))
       return df

def lower_df_columns(df, column_names):
       for column in column_names:
              df[column]=df[column].str.lower()
       return df

def calculate_frequency(tag_list):
      tag_frequency = defaultdict(int)
      for tag_row in tag_list:
             for tag in tag_row:
                    tag_frequency[tag] += 1
      return tag_frequency

def clean_df(df):
       # Keep English posts only
       df.rename(inplace=True,columns={'detected language': 'detected_language'})
       df=df[df.detected_language == 'en']

       # Drop post duplicates, keep most recently published
       df = df.sort_values('post_time').drop_duplicates(['post_id'], keep='last')
       df.reset_index(inplace=True)
       df.sort_values('index',inplace=True)

       # Replace empty by 0, change format of number of responses & claps
       df=replace_empty_in_df_columns(df,['claps','response'])
       df=replace_multiplier_in_df_columns(df,['claps','response'])
       df=lower_df_columns(df,['tag1','tag2','tag3','tag4','tag5','original_tag'])      
       return df

def extract_tags(df):
       # Get tags from 5 columns of tags and concatenate all tags to list of unique tags
       tags = df[['tag1','tag2','tag3','tag4','tag5']]
       tag_list=tags.get_values()
       tag_list=tag_list.tolist()
       tag_list = [[token for token in tag_row if str(token)!='nan'] for tag_row in tag_list]
       return tag_list

#%%
##################################################
# Load Data
df=read_csv_data(data_folder)
file_object = open(pickle_raw_df_name,'wb') 
pickle.dump(df,file_object)   
file_object.close()

##################################################
# Raw Data Cleaning
# Raw Data (df) -> Cleaned Data (df)
df=clean_df(df)

#pickle df
file_object = open(pickle_df_name,'wb') 
pickle.dump(df,file_object)   
file_object.close()

file_object = open(pickle_df_name,'rb')  
df = pickle.load(file_object)  

#%%
##################################################
# Get sequences of tags
# Cleaned Data (df) -> tag_list

tag_list=extract_tags(df)
#####################################################
# Cleaning step for word2vec
# Calculate frequency of tokens
tag_frequency=calculate_frequency(tag_list)

# Keep tag if frequency >2 in tag_list (for word2vec)
tag_list_filtered = [[token for token in tag_row if tag_frequency[token] > 2] for tag_row in tag_list]
tag_frequency=calculate_frequency(tag_list_filtered)

###################################################     
# Create Word2Vec model 
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

#model = gensim.models.Word2Vec.load("word2vec_tagds.model")
#model.wv.most_similar(tag_query)

