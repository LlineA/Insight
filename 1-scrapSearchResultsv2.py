# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:20:42 2018

@author: Graccolab
"""

from bs4 import BeautifulSoup
import requests
import re #  ast
import time
import json
import pandas as pd
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
def remove_escape_character(json_txt):
       while json_txt.find('\\x')!=-1:
             escape_position=json_txt.find('\\x')
             json_txt=json_txt[0:escape_position]+json_txt[escape_position+4:]
             print("escape character deleted")
       return(json_txt)
       
def get_tag_info(json_article):
       tag_list=[]
       detected_language=[]
       tag_follower=[]
       tag_post_count=[]
       
       for post in json_article:             
           for post_number,post_info_value in post['references']['Post'].items():                                                                
                  detected_language.append(post_info_value['detectedLanguage'])                 
                  tag_list_temp=[]
                  tag_follower_temp=[]
                  tag_post_count_temp=[]
                  
                  for idx_post_tags,post_tags in enumerate(post_info_value['virtuals']['tags']):                             
                         try:
                                tag_list_temp.append(post_tags['name'])
                         except:
                                tag_list_temp.append('tag_error')
                                print('tag_error')
                         try:
                                tag_follower_temp.append(post_tags['metadata']['followerCount'])
                         except: #this does not work anymore...
                                tag_follower_temp.append('tag_follower_error')
                                #print('tag_follower_error')
                         try:
                                tag_post_count_temp.append(post_tags['metadata']['postCount'])
                                
                         except:
                                tag_post_count_temp.append('tag_post_count_error')
                                print('post_count')
                  diff_len=5-len(tag_list_temp)
                  
                  for missingTag in range(0,diff_len):                         
                         tag_list_temp.append('')
                         tag_follower_temp.append('')
                         tag_post_count_temp.append('')
                         
                  tag_list.append(tag_list_temp)
                  tag_follower.append(tag_follower_temp)
                  tag_post_count.append(tag_post_count_temp)            
       return detected_language,tag_list,tag_follower,tag_post_count
           
def get_blog_info(bs,tag_list,df):      
       for idx,tag in enumerate(bs.find_all(attrs={"class": "streamItem streamItem--postPreview js-streamItem"})):                                   
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
            
            # append to dataframe
              df = df.append(pd.DataFrame([{"title":title, "response":response, 
                       "link":link, "post_id":post_id,
                       "claps":claps, "post_time":post_time,
                       "original_tag":query, "author_id":author_id, "tag1":tag_list[idx][0],
                       "tag2":tag_list[idx][1],"tag3":tag_list[idx][2],
                       "tag4":tag_list[idx][3],"tag5":tag_list[idx][4],
                       "detected language":detected_language[idx],"tag1_follower":tag_follower[idx][0],
                       "tag2_follower":tag_follower[idx][1],"tag3_follower":tag_follower[idx][2],
                       "tag4_follower":tag_follower[idx][3],"tag5_follower":tag_follower[idx][4],
                       "tag1_postCount":tag_post_count[idx][0],"tag2_postCount":tag_post_count[idx][1],
                       "tag3_postCount":tag_post_count[idx][2],"tag4_postCount":tag_post_count[idx][3],
                       "tag5_postCount":tag_post_count[idx][4],
                       }]))
       return df

##############################################################################
# INPUT for query
# input :  file with tags to import ("seed") and start and end date
#seed_file = pd.read_csv('tags_19000_utf8.csv',encoding='utf-8-sig')
#start_date = date(2018, 5, 23)
#end_date = date(2018, 5, 24)

seed_file=pd.read_csv('tags_data_science_2.csv',encoding='utf-8-sig')
start_date=date(2017,1,1)
end_date=date(2017,1,10)
num=26 # in case it stops,index of file


##############################################################################

# DATA PREPROCESSING
df = pd.DataFrame()
df_erreur=pd.DataFrame()
error=[]
#query="data analysis"

error_file = open('log_error_DS_%s.txt' %num,'a')
error_file.write("\nQuery Start\n")    

# Maximum attempts to try toget html
max_attempts = 10
idx_query=-1

for query in seed_file.tag:                     
       # Loop over defined period
       for day in daterange(start_date, end_date):
              #if idx_query<=150403: 
                    # idx_query=idx_query+1
                     #pass
             # else:
              date_str=day.strftime("%Y") + '/' + day.strftime("%m") +'/' + day.strftime("%d")
              print("scraping articles on %s for date %s.." %(query,date_str))
              # Retrieve information
              idx_query=idx_query+1
              for attempt in range(max_attempts):
                     # access to search page
                     url = 'https://medium.com' + '/tag/%s/archive/%s' %(query, date_str)                                  
                     response = requests.get(url)
                     
                     if response.status_code == 200:                                      
                            bs = BeautifulSoup(response.content,'html.parser',from_encoding='windows-1255')   
                            # Get tags in bottom script of the page
                            json_script = bs.select('script')[-3] 
                            json_txt=json_script.get_text()
                            json_txt="["+json_txt[31:-8]+"]"                                   
                            json_txt=remove_escape_character(json_txt)
                    
                            try:
                                   json_article=json.loads(json_txt)                                                 
                                   detected_language, tag_list, tag_follower,tag_post_count = get_tag_info(json_article)                                                                                                   
                                   df=get_blog_info(bs,tag_list,df) 
                                   
                                   if idx_query%1000==0:
                                          df.to_csv("temp_articles_%s-%s-%s_%s.csv" %(start_date, end_date,idx_query,query), encoding='utf-8-sig', index=False)       
                                   # Successfully retrieved response. Exit attempt loop
                                   
       
                                   break
                            except :
                                   print("\nFailed to load json on tag %s" %(query))
                                   error_file.write("\nFailed to load json on tag %s for %s" %(idx_query, date_str))
                                   error.append(idx_query)
                                   break
                     else:
                           print("Failed to scrap articles on %s for %s.." %(query,date_str ))
                           print("Due to error response : %s" %(response.status_code))
                           print("It was tentative = %s " %(attempt))
                           error_file.write("\nFailed to scrap articles on %s for %s.." %(query, date_str))
                           error_file.write("\nDue to error response : %s \nattempt : %s " %(response.status_code,attempt)) 
                           time.sleep(3)                 
                     
       # save dataframe
df.to_csv("articles_%s-%s-%s.csv" %(start_date, end_date,num), encoding='utf-8-sig', index=False)
error_df=pd.DataFrame(data=error)
error_df.to_csv("error_%s_%s-%s.csv" %(num,start_date, end_date), encoding='utf-8-sig', index=False)
error_file.close()
print("End of scraping")

