# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 12:57:40 2018
Lline - Insight Project 
       Scraper 2 : 
              - Using Selenium, the scraper gets the number of tag follower from the writer publishing page (needs to have a login link)
              - Input : date, list of tags with missing number (pickled object)
              - Output : tag & number of tag followers + auto complete responses
@author: Lline
"""

##############################################################################
#Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import pickle
import datetime
import sys

##############################################################################
# INPUT
csv_file_name='followerCount.csv'
missing_tag_follower_filename='missing_TFF3'
draft_link="https://medium.com/p/abc123def456/edit" #


##############################################################################
#Local FUNCTIONS

def press_tab(browser):
       actions = ActionChains(browser)
       actions.send_keys(Keys.TAB)
       actions.perform()
       time.sleep(0.5)
       del actions
       return 1


def press_enter(browser):
       actions = ActionChains(browser)
       actions.send_keys(Keys.ENTER)
       actions.perform()
       time.sleep(0.5)
       del actions
       return 1

def press_down(browser):
       actions = ActionChains(browser)
       actions.send_keys('\ue015') #down arrow
       actions.perform()
       time.sleep(0.7)
       del actions
       return 1

def press_letter(browser,letter):
       actions = ActionChains(browser)
       actions.send_keys(letter)
       actions.perform()
       time.sleep(0.62)
       del actions
       return 1

def press_escape(browser):
       actions = ActionChains(browser)
       actions.send_keys(Keys.ESCAPE)
       actions.perform()
       time.sleep(1.1)
       del actions
       return 1

def write_df_to_csv(csv_file_name,df, follower_nb_list, tag_list):
       with open(csv_file_name, 'a') as f:
              try:
                     df.to_csv(f,header=False,encoding='utf-8-sig')
              except:
                     # possible encoding error in tag_name:
                     try:
                            for idx,tag_name in enumerate(df['tag']):
                                   df.iloc[idx].tag=tag_name.encode(sys.stdout.encoding, errors='replace')
                                   df.to_csv(f,header=False,encoding='utf-8-sig')
                                   print("charmap error, tag name encoded in bytes")
                     except:
                            # possible encoding error in query:                            
                            try:
                                   for idx,tag_name in enumerate(df['tag']):
                                          df.iloc[idx].tag=tag_name.encode(sys.stdout.encoding, errors='replace')
                                          df.iloc[idx].original_query=query.encode(sys.stdout.encoding,errors='replace')
                                          df.to_csv(f,header=False,encoding='utf-8-sig')
                                          print("charmap error, query encoded in bytes")                          
                            except:
                                   follower_nb_list=[0]
                                   tag_list=['queryerror']
                                   df = pd.DataFrame(
                                       {'tag': [''],
                                        'follower_count': [''],
                                        'original_query': [''],
                                        'date':datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S')
                                       }) 
                                   df.to_csv(f,header=False,encoding='utf-8-sig')
                                   print("encoding error, move on")
       return follower_nb_list, tag_list
##############################################################################
# load
dict_object=open(missing_tag_follower_filename,'rb') # 3
missing_tf = pickle.load(dict_object)  

# authentification link:
medium_access_link="https://medium.com/ .... " # here goes your unique identification link

# open Firefox
browser = webdriver.Firefox()
time.sleep(4)

## go to authentificaiton link
browser.get(medium_access_link)
time.sleep(2)

# go to draft:
browser.get(draft_link)
time.sleep(3)

##############################################################################
# FOR LOOP ON QUERIES
idx_query=0
for tag in missing_tf:
       print(tag)      
       query=tag
       
       ####################################
       # NAVIGATE IN PAGE AND GET INFO
       # 1 - Tab x 3 + enter
       press_tab(browser)
       press_tab(browser)
       press_tab(browser)
       press_enter(browser)
 
       # 2 - Click on publish (so that browser html updates)
       element = browser.find_element_by_xpath('//*[@data-action="show-tags-popover"]')
       element.click()
       time.sleep(0.7)
       
       # 3 - DOWN ARROW x2
       press_down(browser)
       press_down(browser)
       
       #% 4- TYPE QUERY key by key and wait, and DOWN ARROW to "block" menu
       for letter in query:
              press_letter(browser,letter)              
       press_down(browser)
       
       #% 5 - GET INFO
       # Get tag names
       popup_tags=browser.find_elements_by_xpath('//*[@data-action="typeahead-populate"]')
       tag_list=[popup_tags[ii].get_attribute('data-action-value') for ii, elements in enumerate(popup_tags)]
       
       # Get follower numbers
       follower_tags=browser.find_elements_by_class_name("typeahead-score")
       follower_nb_list=[follower_tags[ii].text[1:-1] for ii, elements in enumerate(follower_tags)]
       
       # 6- ESCAPE x 2
       press_escape(browser)
       press_escape(browser)
       ####################################       
       
       ####################################
       # SAVE
       # If no follower
       if follower_nb_list==[]:
              follower_nb_list=[0]
              tag_list=[query]
              
       # STORE IN DATAFRAME
       df = pd.DataFrame(
           {'tag': tag_list,
            'follower_count': follower_nb_list,
            'original_query': [query]*len(tag_list),
            'date':datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S')
           })       
       
       # WRITE IN CSV FILE       
       follower_nb_list, tag_list = write_df_to_csv(csv_file_name, df, follower_nb_list, tag_list)
                                                                                                 
       idx_query=idx_query+1
       print(tag_list)
       print(follower_nb_list)
       print("-----> tag '%s' query [%s] done \n" %(query,idx_query))
       print(datetime.datetime.now())
