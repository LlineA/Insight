# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 11:59:46 2018
Lline - Insight Project 
       Create Popularity Dictionary
       - load csv data
       - clean data:
              - keep English posts only      
              - drop post duplicates, keep most recently published 
              - Replace empty by 0, change format of number of responses & claps
       - extract data:
              - get the 5 x 2 columns of tags and number of followers
              - combine them as a series, keep unique tags
              - convert to dictionary
       - save data
@author: Lline
"""
##############################################################################
# Import libraries  
import os
import glob
import pandas as pd
import re
import pickle

##############################################################################
# INPUT /OUTPUT
tag_follower_data_folder="2 - input data - csv/tag_follower"
output_file_name="pop_dictionary_1"

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

def create_popularity_dictionary(df):   
       df_follower=pd.DataFrame()
       
       # Extract Tags
       df_follower['tag']=pd.concat([df['tag1'],df['tag2'],df['tag3'],df['tag4'],df['tag5']])
       df_follower['tag_follower'] = pd.concat([df['tag1_follower'], df['tag2_follower'],df['tag3_follower'],df['tag4_follower'], df['tag5_follower']])
       
       # Keep unique tags
       df_follower.sort_values(by=['tag', 'tag_follower'],inplace=True)
       df_follower.drop_duplicates(['tag'], keep='last', inplace=True)
       
       # Convert to dictionary
       dict_df_follower= dict(zip(df_follower['tag'], df_follower['tag_follower'])) 
       return dict_df_follower

##############################################################################
# BEGIN

# Read data       
df=read_csv_data(tag_follower_data_folder)

# Preprocess data (keep English posts only, drop duplicates, remplace empty by 0, change number formatting)
df=clean_df(df)

# Create dictionary with tag and number of tag follower
dict_df_follower=create_popularity_dictionary(df)

# Save
file_object = open(output_file_name,'wb') 
pickle.dump(dict_df_follower,file_object)
file_object.close()
