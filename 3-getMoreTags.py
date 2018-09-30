# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 14:15:13 2018
Generate list of new tags based on scraped data    

@author: Graccolab
"""
# Generate list of new tags based on scraped data      
import os
import glob
import pandas as pd


def read_data(data): # read csv files and concatenate
    # list to hold individual data frame
    list_df_s = []

    # retrieve subreddits
    path_data = "data/%s" %data
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

# Get Data
data="data science v2"
df=read_data(data)
outputFileName="tags_data_science_2.csv"

# Add an index, display unique values , count unique post values etc.
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


# Get original tags, and create list of tags that does not contain original tags
originalTags=df['original_tag']
originalTags=pd.Series(data=originalTags.unique()).tolist()
uniqueTags=[tag for tag in allTags if tag not in originalTags]
#tags_with_followers=df_follower['tag'].tolist()
#tag_with_no_follower_nb=[tag for tag in uniqueTags if tag not in tags_with_followers]
# 5771 tags sur 11305 où on n'a pas le nombre de followers

#%%
uniqueTags=pd.DataFrame(data=uniqueTags,columns=['tag'])
uniqueTags.sort_values('tag',inplace=True)
uniqueTags.to_csv(outputFileName, encoding='utf-8-sig', index=False)


