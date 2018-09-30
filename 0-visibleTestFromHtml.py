# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 15:29:51 2018

@author: Graccolab
"""
from bs4 import BeautifulSoup
from bs4.element import Comment
#import urllib.request
from urllib.request import Request, urlopen

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)


req = Request('https://towardsdatascience.com/why-so-many-data-scientists-are-leaving-their-jobs-a1f0329d7ea4', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
print(text_from_html(webpage))

#html = urllib.request.urlopen('https://medium.com/s/youthnow/youth-what-your-attachment-style-means-in-adulthood-self-improvement-awareness-f2e9ac4c4848').read()
#print(text_from_html(html))