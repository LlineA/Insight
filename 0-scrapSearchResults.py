# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:20:42 2018

@author: Graccolab
"""
#%% 1) IMPORT libraries
from bs4 import BeautifulSoup
import requests
import re #  ast
import time
#import pickle
#import os, glob #, sys
#import argparse
import json

import pandas as pd
#import numpy as np
#
from datetime import timedelta, date
#from nltk.tokenize import MWETokenizer
#from rake_nltk import Rake
#import collections

#%% 2) INPUT for query

MEDIUM = 'https://medium.com'
# read file with 1000 most popular tags in 2017

#tags_1000 = pd.read_csv('medium_top_1000_tags_utf8.csv',encoding='utf8')
tags_19000 = pd.read_csv('tags_19000_utf8.csv',encoding='utf-8-sig')
#tags_11000 = pd.read_csv('tags_11000_utf8.csv',encoding='utf-8-sig')
#tags_1000 = pd.read_excel('tags_1000.xlsx')
#tags_23000= pd.read_csv('tags_23000.csv')
# define start and end date
sd = date(2018, 5, 21)
ed = date(2018, 5, 22)
textfile = open('logerror.txt','w')

#3eme essai, depart de tags_1000 avec nouveaux labels
#21-22 mai ok pour iteration 1000
#21-22 mai pour iteration2: 11000 tags

#2eme essai:
#20-21:

#21-22  ok
#22-23 ok
#23-24 ok
# avec erreur postId et AuthorID...
#20-21 ok
#21-22 ok
#22-23 ok
#23-24 ok

# Define date range from start and end date
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
#url example: url="https://medium.com/tag/event-planning/archive/2018/08/28"

# dernier item : junk kar, a priori erreur a kid videos
#%% 3) DATA PREPROCESSING
# Initialize dataframe
df = pd.DataFrame()

# Loop over 1000 2017 most popular tags
#for q in tags_1000.tag_name:
textfile.write("\nC'est parti!\n")
#%%
#for idxq,q in enumerate(tags_23000.tag)


erreur=[]
for idxq,q in enumerate(tags_19000.tag): # HERE CHANGE INDEX WHEN NECESSARY
#for idxq in range(0,1):
 #      q=tags_1000.tag_name[0]
       
#       if (idxq<433): # or idxq>12010):

#       if (idxq<=11964 or idxq>12101):
       #if (idxq<=12103):
       if False:
              pass
       else:
              try:
                     
                     print("scraping articles on %s .." %(q))
                     # Loop over defined period
                     for d in daterange(sd, ed):
              #              print("scraping articles on %s for %s/%s/%s.." %(q, d.strftime("%Y"),d.strftime("%m"),d.strftime("%d")))
                            # Maximum attempts to try
                            max_attempts = 10
                            # Retrieve information
                            for attempt in range(max_attempts):
                                   # access to search page
                                   url = MEDIUM + '/tag/%s/archive/%s/%s/%s' %(q, d.strftime("%Y"),d.strftime("%m"),d.strftime("%d"))
                                   
                                   response = requests.get(url)
                                   # PAGE DE RESULTATS
                                   # Check status code
                                   if response.status_code == 200:
                                          
                                          bs = BeautifulSoup(response.content,'html.parser',from_encoding='windows-1255')
                                          
                                    #%% TEMP Optionnel: si besoin, sauver la quête en pickle pour s'en servir plus tard
                                          #file_Name="articleSearchExample" # CHANGER
                                          #fileObject = open(file_Name,'wb') # CREER FICHIER/OBJET
                                          #pickle.dump(bs,fileObject)   # SAUVE FICHIER
                                          #fileObject.close() #CLOSE
                                          
                                          ##%% si besoin recupere objet pickled
                                          ## we open the file for reading
                                          #fileObject = open(file_Name,'rb')  
                                          #bs = pickle.load(fileObject)  
                                          #fileObject.close()    
              #%%    
                                          # Get tags in bottom script of the page
       #                                   bs.original_encoding
                                          item = bs.select('script')[-3] # ERREUR POSSIBLE ICI SI PAS TOUJOURS SCRIPT = -3!
                                          json_str=item.get_text()
                                          json_str="["+json_str[31:-8]+"]"
                                          
                                          while json_str.find('\\x')!=-1:
                                                position_pb=json_str.find('\\x')
                                                json_str=json_str[0:position_pb]+json_str[position_pb+4:]
                                                print("delete weird character ")
       
                                      
                                          
                                          
                                      
                                          #%%
                                          try:
                                                 json_article=json.loads(json_str)
                                          
                                                 #%%
                                                 #post_number=0
                                                 tags_list=[]
                                                 detected_language=[]
                                                 tag_follower=[]
                                                 tag_post_count=[]
                                                 for post in json_article:
                                                     for post_info_key,post_info_value in post['references']['Post'].items():                                              
                                                            
                                                            detected_language.append(post_info_value['detectedLanguage'])
                                                            tags_temp=[]
                                                            tag_follower_temp=[]
                                                            tag_post_count_temp=[]
                                                            for idx_post_tags,post_tags in enumerate(post_info_value['virtuals']['tags']):
                                                                   
                                                                   tags_temp.append(post_tags['name'])
                                                                   tag_follower_temp.append(post_tags['metadata']['followerCount'])
                                                                   tag_post_count_temp.append(post_tags['metadata']['postCount'])
                                                            diff_len=5-len(tags_temp)
                                                            for missingTag in range(0,diff_len):
                                                                   tags_temp.append('')
                                                                   tag_follower_temp.append('')
                                                                   tag_post_count_temp.append('')
                                                            tags_list.append(tags_temp)
                                                            tag_follower.append(tag_follower_temp)
                                                            tag_post_count.append(tag_post_count_temp)
                                                            # post_number=post_number+1    
                                                                                    
                      #%%                          
              #                                   #%% # LOOP SUR LES DIFFERENTS ARTICLES
              #                                   for idxArticle, elements in enumerate(item.text.split('versionId')):
              #                                          if idxArticle==0:
              #                                                 pass
              #                                          else:
              #                                                 tags_temp=[]
              #                                                 #listeIdx=[]
              #       #                                         Boucle sur tags
              #                                                 for idxTag in range(1,6):
              #                                                        try:                                                       
              #                                                               tags_temp.append(elements.split('{"slug":"')[idxTag].split('"')[0])
              #                                                                                                                       
              #                                                        except:
              #                                                               tags_temp.append("")
              #                                                               #listeIdx.append(idxArticle)
              #                                                               pass 
              #                                                 tags_list.append(tags_temp)   
              #                                   
                                                 #%%
                                                 # find blog title, blog link, postID, # responses, # claps, post_time
                                                 #2)  LOOP ON ALL ARTICLES "VIGNETTES"   à partir du code de siin                                       
                                                 #follower number (for people and tag) #related tags to tag
                                                 #check unicode problem
                                                 # start from 1000 most popular again
                                                 for idx,tag in enumerate(bs.find_all(attrs={"class": "streamItem streamItem--postPreview js-streamItem"})):                                   
                                                        if True: #(tag(text=re.compile('response'))): 
                                                               title=[]
                                                               link=[]
                                                               post_id=[]
                                                               response=[]
                                                               claps=[]
                                                               post_time=[]
                                                               author_id=[]
                                                               
                                                               try:
                                                                      author_id =tag.find_all(attrs={"class":"link u-baseColor--link avatar"})[0]["data-user-id"]                                              
                                                               except:
                                                                      pass
                                                               try:
                                                                      title = tag.find_all(attrs={"class":"section-content"})[0].text.strip()
                                                               except:
                                                                      pass
                                                                             
                                                               try:
                                                                      link = tag.find_all(attrs={"class": "button button--smaller button--chromeless u-baseColor--buttonNormal"})[0]["href"]
                                                               except:
                                                                      pass
                                                               try:
                                                                      post_id = tag.find_all(attrs={"class":"button button--smaller button--chromeless u-baseColor--buttonNormal"})[0]["data-post-id"]
                                                               except:
                                                                      pass
                                                               try:
                                                                      response = tag(text=re.compile('response'))[0].split()[0]
                                                               except:
                                                                      pass
                                                               try:                                                 
                                                                      claps = tag.find_all(attrs={"data-action":"show-recommends"})[0].text.strip()
                                                                      
                                                                      
                                                               except:
                                                                      pass
                                                               try:
                                                                      post_time = tag.find_all("time")[0]["datetime"]
                                                               except:
                                                                      pass       
                                                             # author id
                                                             # append to dataframe
                                                               df = df.append(pd.DataFrame([{"title":title, "response":response, 
                                                                        "link":link, "post_id":post_id,
                                                                        "claps":claps, "post_time":post_time,
                                                                        "original_tag":q, "author_id":author_id, "tag1":tags_list[idx][0],
                                                                        "tag2":tags_list[idx][1],"tag3":tags_list[idx][2],
                                                                        "tag4":tags_list[idx][3],"tag5":tags_list[idx][4],
                                                                        "detected language":detected_language[idx],
                                                                        "tag1_follower":tag_follower[idx][0],
                                                                        "tag2_follower":tag_follower[idx][1],
                                                                        "tag3_follower":tag_follower[idx][2],
                                                                        "tag4_follower":tag_follower[idx][3],
                                                                        "tag5_follower":tag_follower[idx][4],
                                                                        "tag1_postCount":tag_post_count[idx][0],
                                                                        "tag2_postCount":tag_post_count[idx][1],
                                                                        "tag3_postCount":tag_post_count[idx][2],
                                                                        "tag4_postCount":tag_post_count[idx][3],
                                                                        "tag5_postCount":tag_post_count[idx][4],
                                                                        }]))
                                                               if idxq%1000==0:
                                                                      df.to_csv("temp_articles_%s-%s-%s.csv" %(sd, ed,str(idxq)), encoding='utf-8-sig', index=False)
                     
                                                                      
                     
                                                         
                                                  # successfully retrieved response. Exit attempt loop
                                                 break
                                          except :
                                                 print("erreur chargement json pour %s" %(q))
                                                 textfile.write("\nFailed to load json on tag %s for %s/%s/%s.." %(str(idxq), d.strftime("%Y"),d.strftime("%m"),d.strftime("%d")))
                                                 erreur.append(idxq)
                                                 #textfile.write("Failed to load json on %s for %s/%s/%s.." %(q, d.strftime("%Y"),d.strftime("%m"),d.strftime("%d"))) 
                                                 break
                                   else:
                                         print("Failed to scrap articles on %s for %s/%s/%s.." %(q, d.strftime("%Y"),d.strftime("%m"),d.strftime("%d")))
                                         print("Due to error response :")
                                         print(response.status_code)
                                         print("It was tentative = ")
                                         print(attempt) 
                                         textfile.write("\nFailed to scrap articles on %s for %s/%s/%s.." %(q, d.strftime("%Y"),d.strftime("%m"),d.strftime("%d")))
                                         textfile.write("\nDue to error response : ")
                                         textfile.write(str(response.status_code))
                                         textfile.write("\nattempt : ")
                                         textfile.write(str(attempt))
#                                         textfile.write("%n")
              
                                         
                                         time.sleep(3)
                     
                  
              except:
                     textfile.write("\n Unknown error Failed to scrap articles on tag %s for %s/%s/%s.." %(str(idxq), d.strftime("%Y"),d.strftime("%m"),d.strftime("%d")))
                     #pass
              
              # save dataframe
df.to_csv("articles_%s-%s.csv" %(sd, ed), encoding='utf-8-sig', index=False)
erreurdf=pd.DataFrame(data=erreur)
erreurdf.to_csv("erreurs_%s-%s.csv" %(sd, ed), encoding='utf-8-sig', index=False)

textfile.close()
print("End of scraping")