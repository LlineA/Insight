# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 22:38:07 2018

@author: Graccolab
"""


#%%
import pickle
import os
import glob
import pandas as pd
import io
import re
#from math import isnan
# save it
# get old dictionary
fileName="follower_nb_dictionnary"

dictObject=open(fileName,'rb')
popDict1 = pickle.load(dictObject)  

#%%
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

def replace_empty(df):
       df['claps'].replace('[]','0',inplace=True)
       df['response'].replace('[]','0',inplace=True)
       return df
                  
def replace_multiplier(df):   
       df['followerCount'] = df['followerCount'].apply(lambda x: convert_multiplier(x))
      
       return df

def lower_tags(df):
       column_string=['tag','originalQuery']
       for column in column_string:
              df[column]=df[column].str.lower()
       
       return df

#%%
data_folder='6 - tag follower round 2- csv'
df=read_csv_data(data_folder)
df=lower_tags(df)

#%%
# treat duplicates (within df)
df = df.sort_values('timestamp').drop_duplicates(['tag'], keep='last')
df.reset_index(inplace=True)
df=df.rename(columns={'index':'indexQuery','level_0':'index'})
df.sort_values('index',inplace=True)

# delete rows with NaN values
# replace multiplier
df.dropna(subset=['followerCount'],inplace=True)
df=replace_multiplier(df)
df['followerCount'] = df['followerCount'].apply(pd.to_numeric, errors='coerce')

#%%
# popDict1 comes from first scraping step
# we update it with dictDS
# output popDict2

dictDS= dict(zip(df['tag'], df['followerCount'])) 
# notre dictionnaire de base est popDict1
popDict2={}
popDict2.update(popDict1)
popDict2.update(dictDS)

fileNameDict="popDict2"
fileObject = open(fileNameDict,'wb')
pickle.dump(popDict2,fileObject)   
fileObject.close() 



