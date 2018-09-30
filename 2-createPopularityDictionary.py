# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 11:59:46 2018

@author: Graccolab
"""

"""
Created on Mon Sep 24 11:08:20 2018

@author: Graccolab
"""

# import librarires  
import os
import glob
import pandas as pd
import re
#import gensim
#from collections import defaultdict
#import operator
#import numpy as np
import pickle

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

# Get as much tag follower data as possible
tag_follower_data="tag_follower"
df_tf=read_csv_data(tag_follower_data)

# keep English posts only
df_tf.rename(inplace=True,columns={'detected language': 'detected_language'})
df_tf=df_tf[df_tf.detected_language == 'en']


# Drop post duplicates, keep most recently published (now down to number_post = 46446)
df_tf = df_tf.sort_values('post_time').drop_duplicates(['post_id'], keep='last')
df_tf.reset_index(inplace=True)
df_tf.sort_values('index',inplace=True)

# Replace empty by 0, change format of number of responses & claps
df_tf=replace_empty(df_tf)
df_tf=replace_multiplier(df_tf)
df_tf=lower_tags(df_tf)

# get the 5 x 2 columns of tags and number of followers
df_tf_tag1=df_tf[['tag1','tag1_follower']].rename(columns={'tag1':'tag','tag1_follower':'tag_follower'})
df_tf_tag2=df_tf[['tag2','tag2_follower']].rename(columns={'tag2':'tag','tag2_follower':'tag_follower'})
df_tf_tag3=df_tf[['tag3','tag3_follower']].rename(columns={'tag3':'tag','tag3_follower':'tag_follower'})
df_tf_tag4=df_tf[['tag4','tag4_follower']].rename(columns={'tag4':'tag','tag4_follower':'tag_follower'})
df_tf_tag5=df_tf[['tag5','tag5_follower']].rename(columns={'tag5':'tag','tag5_follower':'tag_follower'})

#combine them as a series, keep unique tags
df_tf_follower=pd.concat([df_tf_tag1,df_tf_tag2,df_tf_tag3,df_tf_tag4,df_tf_tag5],sort=False)
df_tf_follower.sort_values(by=['tag', 'tag_follower'],inplace=True)
df_tf_follower.drop_duplicates(['tag'], keep='last', inplace=True)

# convert to dictionary
dict_df_follower= dict(zip(df_tf_follower['tag'], df_tf_follower['tag_follower'])) 
dict_df_follower['canada'] #Best dictionnary I have so  far ... 54846

# save it
file_Name="follower_nb_dictionnary"
fileObject = open(file_Name,'wb') # CREER FICHIER/OBJET
pickle.dump(dict_df_follower,fileObject)   # SAUVE FICHIER
fileObject.close() #CLOSE