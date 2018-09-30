# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 12:01:17 2018

@author: Graccolab
"""
import numpy as np

def number_of_follower(list_of_tags,dict_follower):
       tag_follower=[]
       for tag in list_of_tags:
              tag_follower.append(int(dict_follower[tag]))
       return(tag_follower)

def get_most_popular_among_10(most_similar_10,dict_follower):
       most_similar_list=[tag for i, (tag, distance) in enumerate(most_similar_10)]
       tag_follower_list=number_of_follower(most_similar_list,dict_follower)
       tag_follower_list[1]=tag_follower_list[7]
       max_follower_number=max(tag_follower_list)
       
       idx_max = np.argwhere(tag_follower_list == np.amax(tag_follower_list)).flatten().tolist()
       idx_max = np.argwhere(tag_follower_list == np.amax(tag_follower_list)).flatten()
       most_similar_list[idx_max]# ERREUR ICI ! 
       
       return max_follower_number,idx_max
###################################################
max_follower_number,idx_max=get_most_popular_among_10(most_similar_10,dict_follower)

#load dict_follower
if max_follower_number>dict_follower[tag_query]:
       print("There is a better tag with  %s followers : %s" %max_follower_number)

#%%
def find_more_popular_tags(tag_output,input_follower_nb,tag_follower_dict):
       better_choices={}
       for tag in tag_output:
              tag_follower_temp=tag_follower_dict[tag[0]]
              if tag_follower_temp>input_follower_nb:
                     better_choices[tag[0]]=tag_follower_temp             
       return better_choices

def find_more_popular_tags2(tag_output,input_follower_nb,tag_follower_dict):
       better_choices={}
       for tag in tag_output:
              tag_follower_temp=int(tag_follower_dict[tag[0]])
              if tag_follower_temp>input_follower_nb:
                     better_choices[tag[0]]=tag_follower_temp             
       return better_choices
tag_output=most_similar_10.copy()
#input_follower_nb=45

better_choices=find_more_popular_tags2(tag_output,input_follower_nb,dict_df_follower)
print(better_choices)
