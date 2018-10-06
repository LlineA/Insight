# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 14:55:38 2018
Lline - Insight Project 
       Data descriptives
  
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
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
#%%
##############################################################################
# INPUT
#Data Input

#data_folder="2 - input data - csv/tags_19000/data" # version 1 - pop
data_folder="2 - input data - csv/data science v2/premiere iteration 2017-01" # version 2 - DS 
data_folder="2 - input data - csv/data science v2/data" # version 2 - DS 152k
data_folder="2 - input data - csv/data science v2/deuxieme iteration 10days 2017-01" # version 2 - DS 104k
#data_folder="2 - input data - csv/combined/data" # version 3 - DS+pop

#pickle_raw_df_name="raw_df_pop" # version 1 - pop
#pickle_raw_df_name="raw_df_DS" # version 2 - DS
#pickle_raw_df_name="raw_df_combined"  # version 3 - DS+pop

#pickle_df_name="df_pop" # version 1 - pop
#pickle_df_name="df_DS" # version 2 - DS
#pickle_df_name="df_combined"  # version 3 - DS+pop
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
# Load Data
df=read_csv_data(data_folder)

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


# Histogram of number of tags used

# Histogram of number of claps
 

#%%
##################################################
# Get sequences of tags
# Cleaned Data (df) -> tag_list
tags = df[['tag1','tag2','tag3','tag4','tag5']]
tag_list=tags.get_values()
tag_list=tag_list.tolist()
tag_list = [[token for token in tag_row if str(token)!='nan'] for tag_row in tag_list]

tag_list.nunique()

df['author_id'].nunique()


df['claps'] = df['claps'].apply(pd.to_numeric, errors='coerce')
df['claps'].mean()
df['claps'].median()
df['index'].groupby('claps').count()

table_claps=pd.DataFrame(df.groupby(['claps'],sort=True)['index'].count())
table_claps.rename(columns={'index':'claps'},inplace=True)
nb_post=len(df)
table_claps['percentage']=table_claps.apply(lambda row: row['claps']/nb_post*100,axis=1)


np.cumsum(table_claps['percentage'])

cumsumtable=np.cumsum(table_claps['percentage'][::-1])[::-1] 
boxplot = df.boxplot(column=['claps'])
sns.distplot(df.claps>0)

plt.hist(df['claps'][(df.claps<600)&(df.claps>0)])
plt.hist(df['claps'],bins=[0,1,2,100,1000,10000,10000])


allTags=pd.concat([df['tag1'],df['tag2'],df['tag3'],df['tag4'],df['tag5']])
allTags.nunique()
allTags=allTags.str.lower()
allTags=pd.Series(data=allTags.unique()).tolist()


