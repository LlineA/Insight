# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 14:15:13 2018
Lline - Insight Project 
       Generate list of new tags comparing new csv data and previous dictionary
              - Load Data (csv input data and dictionary)
              - Clean Data: Keep English Posts only, reset index, 
              - Get tags from 5 columns of tags and concatenate all tags to list of unique tags
              - Get original tags, and create list of tags that does not contain original tags
@author: Lline
"""

##############################################################################
#Import libraries
import os
import glob
import pandas as pd

##############################################################################
# INPUT/OUTPUT
data_folder="2 - input data - csv/data science v2/data"
output_file_name="tags_data_science_2.csv"

##############################################################################
# local FUNCTIONS

def read_data(data): # read csv files and concatenate
    # list to hold individual data frame
    list_df_s = []

    # retrieve subreddits
    path_data = "%s" %data
    list_csv = os.listdir(path_data)

    # loop over subreddits
    for csv in list_csv:

        # retrieve csv file
        path_csv = glob.glob(os.path.join(path_data+"/"+csv))[0]
        print(path_csv)
        # append to dataframe list if not empty
        list_df_s.append(pd.read_csv(path_csv,index_col=None, header=0,engine="python",encoding='utf-8-sig'))

    # concatenate dataframes and return
    return pd.concat(list_df_s)

def clean_df(df):
       # Keep English posts only
       df.rename(inplace=True,columns={'detected language': 'detected_language'})
       df=df[df.detected_language == 'en']

       # Drop post duplicates, keep most recently published
       df.reset_index(inplace=True)
       df.rename(inplace=True,columns={'index': 'original_index'}) 
       return df

def extract_tags(df):
       # Get tags from 5 columns of tags and concatenate all tags to list of unique tags
       all_tags=pd.concat([df['tag1'],df['tag2'],df['tag3'],df['tag4'],df['tag5']])
       all_tags=all_tags.str.lower()
       all_tags=pd.Series(data=all_tags.unique()).tolist()
       return all_tags

def get_original_tags(df):
       original_tags=df['original_tag']
       original_tags=pd.Series(data=original_tags.unique()).tolist()
       return original_tags
##############################################################################
# BEGIN
# Get Data
df=read_data(data_folder)

# Preprocess data (keep English posts only, drop duplicates)
df=clean_df(df)

# Extract Tags
all_tags=extract_tags(df)

# Get original tags
original_tags=get_original_tags(df)

# Create list of new tags excluding original tags
unique_tags=[tag for tag in all_tags if tag not in original_tags]

# Save file
unique_tags=pd.DataFrame(data=unique_tags,columns=['tag'])
unique_tags.sort_values('tag',inplace=True)
unique_tags.to_csv(output_file_name, encoding='utf-8-sig', index=False)


