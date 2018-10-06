# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 12:57:40 2018
Lline - Insight Project 
Scraper 2 : 
       - Using Selenium, the scraper gets the number of tag follower from the writer publishing page (needs to have a login link)
       - Input : date, tag
       - Output : tag, number of tag followers (and auto complete responses too)
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
missing_tag_follower_filename='missingTFF3'
draft_link="https://medium.com/p/abc123def456/edit" #

# load
dictObject=open(missing_tag_follower_filename,'rb') # 3
missingTFF = pickle.load(dictObject)  

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
for tag in missingTFF:
       print(tag)      
       query=tag
       
       # NAVIGATE IN PAGE AND GET INFO
       # 1- PRESS tab x 3 + ENTER WAIT
       actions = ActionChains(browser)
       actions.send_keys(Keys.TAB) # down arrow
       actions.perform()
       time.sleep(0.5)
       del actions
       actions = ActionChains(browser)
       actions.send_keys(Keys.TAB) # down arrow
       actions.perform()
       time.sleep(0.5)
       del actions       
       actions = ActionChains(browser)
       actions.send_keys(Keys.TAB) # down arrow
       actions.perform()
       time.sleep(0.5)
       del actions
       actions = ActionChains(browser)
       actions.send_keys(Keys.ENTER) # down arrow
       actions.perform()
       time.sleep(0.5)
       del actions

 
       # 2- click on publish (so that browser html updates)
       element = browser.find_element_by_xpath('//*[@data-action="show-tags-popover"]')
       element.click()
       time.sleep(0.7)
       
       # 3- DOWN ARROW  then WAIT x2
       actions = ActionChains(browser)
       actions.send_keys('\ue015') # down arrow
       actions.perform()
       time.sleep(0.651)
       del actions
       actions = ActionChains(browser)
       actions.send_keys('\ue015') #down arrow
       actions.perform()
       time.sleep(0.9)
       del actions
       
       #% 4- TYPE QUERY key by key and wait, and DOWN ARROW to "block" menu
       for letter in query:
              actions = ActionChains(browser)
              actions.send_keys(letter)
              actions.perform()
              time.sleep(0.62)
              del actions
       
       actions = ActionChains(browser)
       actions.send_keys('\ue015') #DOWN arrow
       actions.perform()
       time.sleep(1.2)
       
       #% 5 - GET INFO
       # tag names
       popup_tags=browser.find_elements_by_xpath('//*[@data-action="typeahead-populate"]')
       tag_list=[popup_tags[ii].get_attribute('data-action-value') for ii, elements in enumerate(popup_tags)]
       
       #follower number
       follower_tags=browser.find_elements_by_class_name("typeahead-score")
       ft_list=[follower_tags[ii].text[1:-1] for ii, elements in enumerate(follower_tags)]
       
       # 6- ESCAPE x 2
       actions = ActionChains(browser)
       actions.send_keys(Keys.ESCAPE)
       actions.perform()
       time.sleep(1.1)
       
       actions = ActionChains(browser)
       actions.send_keys(Keys.ESCAPE)
       actions.perform()
       time.sleep(1.18)
       
       # if no follower
       if ft_list==[]:
              ft_list=[0]
              tag_list=[query]
              
       # STORE IN DATAFRAME
       df = pd.DataFrame(
           {'tag': tag_list,
            'followerCount': ft_list,
            'originalQuery': [query]*len(tag_list),
            'date':datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S')
           })       
       
       # WRITE IN CSV FILE
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
                                          df.iloc[idx].originalQuery=query.encode(sys.stdout.encoding,errors='replace')
                                          df.to_csv(f,header=False,encoding='utf-8-sig')
                                          print("charmap error, query encoded in bytes")                          
                            except:
                                   ft_list=[0]
                                   tag_list=['queryerror']
                                   df = pd.DataFrame(
                                       {'tag': [''],
                                        'followerCount': [''],
                                        'originalQuery': [''],
                                        'date':datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S')
                                       }) 
                                   df.to_csv(f,header=False,encoding='utf-8-sig')
                                   print("encoding error, move on")

                                                 
                                                 
       idx_query=idx_query+1
       print(tag_list)
       print(ft_list)
       print("-----> tag '%s' query [%s] done \n" %(query,idx_query))
       print(datetime.datetime.now())
