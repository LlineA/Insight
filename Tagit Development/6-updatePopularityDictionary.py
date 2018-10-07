# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 22:38:07 2018
       Lline - Insight Project 
       Update the popularity dictionary with new information coming from second step of scraping
              e.g. fill in the number of tag follower when it was missing
  
@author: Lline
"""

##############################################################################
#Import libraries
import pickle
import os
import glob
import pandas as pd
import io
import re

##############################################################################
# INPUT
# get old dictionary
dict_name="pop_dictionary_1"
data_folder='6 - tag follower round 2- csv'

##############################################################################
# Local FONCTIONS

def read_csv_data(data_folder):
    list_df_s = []
    path_data = "%s" %data_folder
    list_csv = os.listdir(path_data)

    # loop over csv_files
    for csv in list_csv:
        # retrieve csv file       
        path_csv = glob.glob(os.path.join(path_data+"/"+csv))[0]
        path_csv=io.open(path_csv, encoding='latin-1')
        print(path_csv)
        # append to dataframe list if not empty
        list_df_s.append(pd.read_csv(path_csv,index_col=None, header=0,engine="python",encoding='utf-8-sig'))

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
      # lower case of df columns tag and original_query
       df=lower_df_columns(df,['tag','original_query'])
       
       # treat duplicates (within df): only keep most recent duplicates, reindex df
       df = df.sort_values('timestamp').drop_duplicates(['tag'], keep='last')
       df.reset_index(inplace=True)
       df=df.rename(columns={'index':'indexQuery','level_0':'index'})
       df.sort_values('index',inplace=True)
       
       # delete rows with NaN values, replace multiplier, convert follower_count to numeric
       df.dropna(subset=['follower_count'],inplace=True)
       df=replace_multiplier_in_df_columns(df,['follower_count'])
       df['follower_count'] = df['follower_count'].apply(pd.to_numeric, errors='coerce')
       
       return df
##############################################################################
# BEGIN
       
# Load data
dict_object=open(dict_name,'rb')
pop_dictionary_1 = pickle.load(dict_object)  
df=read_csv_data(data_folder)

# Clean Data
df=clean_df(df)

# Update Dictionary
       # input: pop_dictionary_1 comes from scraping1, we update it with ds_dictionary_1
       # output: combined_dictionary_1
combined_dictionary_1={}
combined_dictionary_1.update(pop_dictionary_1)

ds_dictionary_1= dict(zip(df['tag'], df['follower_count'])) 
combined_dictionary_1.update(ds_dictionary_1)

# Save
file_nameDict="combined_dictionary_1"
fileObject = open(file_nameDict,'wb')
pickle.dump(combined_dictionary_1,fileObject)   
fileObject.close() 



