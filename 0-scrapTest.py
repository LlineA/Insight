# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 14:24:21 2018

@author: Graccolab
"""
# 1) Import libraries

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv
import pickle

#%% 2) Get the html of the webpage
urlpage='https://towardsdatascience.com/why-so-many-data-scientists-are-leaving-their-jobs-a1f0329d7ea4'
req = Request(urlpage, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

#%% 3) Parse the html using beautiful soup
soup = BeautifulSoup(webpage, 'html.parser')

#%% 4) save the html of the article
file_Name = "article1" # HERE CHANGE the name
# open the file for writing
fileObject = open(file_Name,'wb') 
# this writes the object a to the
# file named 'testfile'
pickle.dump(soup,fileObject)   

fileObject.close()
# we open the file for reading
fileObject = open(file_Name,'rb')  
# when you need: load the object from the file into var b
soup = pickle.load(fileObject)  

# Function to get text or link elements
def find_text(element):
       text=element.findAll(text=True)
       texts=[t for t in text]
       return texts
def find_link(element):
       link=element.findAll('a')
       links = [l.get('href') for l in link]
       return links

# Get the tags, the number of claps (arrondi), and the link of the profile of the author
tagObjects=soup.find("ul", {"class":"tags tags--postTags tags--borderless"}) #['href']
tags=find_text(tagObjects)
#print(tagObjects)
clapObjects=soup.find("span", {"class":"u-textAlignCenter u-relative u-background js-actionMultirecommendCount u-marginLeft10"})
claps=find_text(clapObjects)
claps=claps[0]

#profileObjects=soup.find("div",{"u-lineHeightTightest"})
#profileLink=find_link(profileObjects)


#%%
#import StringIO
#s = StringIO.StringIO(claps[0])
with open('test.csv', "w",newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([claps])
        writer.writerow(tags)
        toto=claps
        toto=toto.append([t for t in tags])
        writer.writerow(toto)
#        writer.writerow(claps ,[t for t in tags])
        #writer.writerow(trucitruc)
       # writer.writerow([claps])