# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:56:42 2018
Lline - Insight Project 
       Get data and identify the most frequently used tags whose number of followers are missing
       - Input : csv files and dictionary
              - Load Data
              - Clean Data:
                     - Keep only posts published in English
                     - Drop post duplicates, keep most recently published
                     - Replace empty by 0, change format of number of responses & claps
                     - Get sequences of tags
                     - Identify tags with missing follower number
                     - Get frequency of tags
       -Output :  Pickle list of tags whose number of followers is missing and have a certain frequency
  
@author: Lline
"""


##############################################################################
#Import libraries
import os
import glob
import pandas as pd
import re
from collections import defaultdict 
import pickle


##############################################################################
# # INPUT/OUTPUT
#Data Input
data_path= "2 - input data - csv"

# version 1 - pop
#data_folder= data_path + "/tags_19000/data" 

# version 2 - ds
data_folder= data_path + "/data science v2/data"

# version 3 - ds+pop
#data_folder= data_path + "/combined" 

#Parameter
frequency_criteria=2 # find tags whose number of follower is missing and frequency of use = 2

# Data output : 
output_file_name="missing_tag_follower_2"
current_dictionary="pop_dictionary_1"

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

def calculate_frequency(tag_list):
      tag_frequency = defaultdict(int)
      for tag_row in tag_list:
             for tag in tag_row:
                    tag_frequency[tag] += 1
      return tag_frequency

def count_missing_follower_nb(frequent_tag_frequency,dict_follower):
       count_yes=0
       count_no=0
       for tag in frequent_tag_frequency.keys():
              if tag in dict_follower.keys():
                     count_yes=count_yes+1
              else:
                     count_no=count_no+1
       print(count_yes)
       print(count_no)
       return count_yes, count_no
       #%%
##################################################
# Load CSV Data and popularity dictionary
df=read_csv_data(data_folder)
dictObject=open(current_dictionary,'rb') # get current dictionary
dict_follower = pickle.load(dictObject) 

##################################################
# Raw Data Cleaning  # Raw Data (df) -> Cleaned Data (df)
# Preprocess data (keep English posts only, drop duplicates, remplace empty by 0, change number formatting)
df=clean_df(df)

##################################################
# Get sequences of tags # Cleaned Data (df) -> tag_list
tag_list=extract_tags(df)

#####################################################
# Calculate frequency of use of tags
tag_frequency = calculate_frequency(tag_list)

#####################################################
## Get list of tags with no tag follower number pickle them for future use
# get tags with no TF whose frequency > frequency criteria
frequent_tag_list = [[token for token in tag_row if tag_frequency[token] == frequency_criteria ] for tag_row in tag_list]
frequent_tag_frequency = calculate_frequency(frequent_tag_list)
count_missing_follower_nb(frequent_tag_frequency, dict_follower)             
missing_tag_follower_frequent=[tag for tag in frequent_tag_frequency.keys() if tag not in dict_follower.keys()]

#####################################################
# Save
file_object = open(output_file_name,'wb') 
pickle.dump(missing_tag_follower_frequent,file_object)   
file_object.close()


