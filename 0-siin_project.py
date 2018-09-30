# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 11:44:57 2018

@author: Graccolab
"""


import re,  ast, time
import os, glob #, sys
import argparse
import json
import requests
import pandas as pd
#import numpy as np
from bs4 import BeautifulSoup
from datetime import timedelta, date
from nltk.tokenize import MWETokenizer
from rake_nltk import Rake
import collections

#------------------------------------------
# arguments
#------------------------------------------
parser = argparse.ArgumentParser()

# add options
parser.add_argument("--download_articles", help="Download list of articles given range", nargs=6, type=int)
parser.add_argument("--get_response", help="Get response from list of articles. Option = 0, 1, 2, ..", nargs=1, type=int)
parser.add_argument("--get_userinfo", help="Get detailed user informations. Option = 0, 1, 2, ..", nargs=1, type=int)

# parse arguments
args = parser.parse_args()

if args.download_articles:
    sdy  = int(args.download_articles[0])
    sdm  = int(args.download_articles[1])
    sdd  = int(args.download_articles[2])
    edy =  int(args.download_articles[3])
    edm =  int(args.download_articles[4])
    edd =  int(args.download_articles[5])

if args.get_response:
    chunk_index = int(args.get_response[0])

if args.get_userinfo:
    chunk_index_userinfo = int(args.get_userinfo[0])

#------------------------------------------
# option for script
#------------------------------------------
DownloadArticleList = args.download_articles
GetResponses        = args.get_response
GetUserInfo         = args.get_userinfo
ExtractMostCommon   = False
DecorateGroup       = True




# url for MEDIUM
MEDIUM = 'https://medium.com'
query = [
    'data-science',
    'machine-learning',
    'artificial-intelligence',
    'deep-learning',
    'neural-networks',
    ]


def read_data(data):

    # list to hold individual data frame
    list_df_s = []

    # retrieve subreddits
    path_data = "data/%s" %data
    list_csv = os.listdir(path_data)

    # loop over subreddits
    for csv in list_csv:

        # retrieve csv file
        path_csv = glob.glob(os.path.join(path_data+"/"+csv))[0]

        # append to dataframe list if not empty
        list_df_s.append(pd.read_csv(path_csv,index_col=None, header=0))

    # concatenate dataframes and return
    return pd.concat(list_df_s)




def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def clean_json_response(response):
    return json.loads(response.text.split('])}while(1);</x>')[1])

# retrieve user id from user name
def get_user_id(username):
    print('Retrieving user ID..')
    url = MEDIUM + '/@' + username + '?format=json'
    response = requests.get(url)
    response_dict = clean_json_response(response)
    return response_dict['payload']['user']['userId']

# retrieve user information from user id
def get_userinfo(user_id):

    url = MEDIUM + '/_/api/users/' + user_id

    # maximum attempts to try
    max_attempts = 10

    # retrieve uesr information
    for attempt in range(max_attempts):

        # request
        response = requests.get(url)

        # check status code
        if response.status_code == 200:
            response_dict = clean_json_response(response)
            payload = response_dict['payload']
            break

        # for bad request, wait for next attempt
        else:
            print("Failed to retrieve user information for %s. Retry in 3 seconds.." % user_id)
            time.sleep(3)

    # retrive user information from dict
    try:
        name = payload['value']['name']
    except:
        name = ""
        pass

    try:
        username = payload['value']['username']
    except:
        username = ""
        pass

    try:
        bio = payload['value']['bio']
    except:
        bio = ""
        pass

    try:
        twitter = payload['value']['twitterScreenName']
    except:
        twitter = ""
        pass

    try:
        facebook = payload['value']['facebookAccountId']
    except:
        facebook = ""
        pass


    # dictionary of user information
    user_info = {
        'name': name,
        'username': username,
        'bio': bio,
        'twitterScreenName': twitter,
        'facebookAccountId': facebook,
        }

    return user_info

# retrieve all responses from the post
def get_post_responses(posts):
    print('Retrieving the post responses...')
    responses = []
    for post in posts:
        url = MEDIUM + '/_/api/posts/' + post + '/responses'

        # maximum attempts to try
        max_attempts = 10

        # retrieve uesr information
        for attempt in range(max_attempts):

            # request for post responses
            response = requests.get(url)

            # check status code
            if response.status_code == 200:

                response_dict = clean_json_response(response)
                try:
                    responses += response_dict['payload']['value']
                except:
                    pass

            else:
                time.sleep(3)

    return responses


def download_article_list(sdy, sdm, sdd, edy, edm, edd):

    # define start and end date
    sd = date(sdy, sdm, sdd)
    ed = date(edy, edm, edd)

    # initialize dataframe
    df = pd.DataFrame()

    # loop over each query
    for q in query:

        # loop over each date
        for d in daterange(sd, ed):

            print("scraping articles on %s for %s/%s/%s.." %(q, d.strftime("%Y"),d.strftime("%m"),d.strftime("%d")))

            # maximum attempts to try
            max_attempts = 10

            # retrieve uesr information
            for attempt in range(max_attempts):

                # retrieve single page
                url = MEDIUM + '/tag/%s/archive/%s/%s/%s' %(q, d.strftime("%Y"),d.strftime("%m"),d.strftime("%d"))
                response = requests.get(url)

                # check status code
                if response.status_code == 200:

                    bs = BeautifulSoup(response.content,'html.parser')

                    # find title and link
                    for tag in bs.find_all(attrs={"class": "streamItem streamItem--postPreview js-streamItem"}):

                        # require at least 1 comment
                        if (tag(text=re.compile('response'))):

                        # require at least 10 recommends
                        #if (response['virtuals']['recommends'] >= 10):

                            # retrieve title and link for each article
                            try:
                                #title = tag.h3.text
                                title = tag.find_all(attrs={"class":"section-content"})[0].text.strip()
                                link = tag.find_all(attrs={"class": "button button--smaller button--chromeless u-baseColor--buttonNormal"})[0]["href"]
                                post_id = tag.find_all(attrs={"class":"button button--smaller button--chromeless u-baseColor--buttonNormal"})[0]["data-post-id"]
                                response = tag(text=re.compile('response'))[0].split()[0]
                                claps = tag.find_all(attrs={"data-action":"show-recommends"})[0].text.strip()
                                post_time = tag.find_all("time")[0]["datetime"]

                                # append to dataframe
                                df = df.append(pd.DataFrame([{"title":title, "response":response, 
                                                                "link":link, "post_id":post_id,
                                                                "claps":claps, "post_time":post_time,
                                                                "topic":q 
                                                                }]))
                            except:
                                pass
                    # successfully retrieved response. Exit attempt loop
                    break

                # for bad request, wait for next attempt
                else:
                    print("Failed to scrap articles on %s for %s/%s/%s.." %(q, d.strftime("%Y"),d.strftime("%m"),d.strftime("%d")))
                    time.sleep(3)

    # save dataframe
    df.to_csv("data/list_articles/articles_%s-%s.csv" %(sd, ed), encoding='utf-8', index=False)
    print("Successfully scraped articles!")

    return


def get_user_responses():

    # read multiple csv
    df_article = read_data("list_articles")
    
    # drop duplicates
    df_article = df_article.drop_duplicates(subset=["post_id"], keep="first")
    
    # chunk size
    n = 500
    
    # split dataframe into subset
    list_df_article = [df_article[i:i+n] for i in range(0,df_article.shape[0],n)]
    
    print("Getting responses from dataframe %s / %s" % (chunk_index+1, len(list_df_article)))
    
    # sub dataframe of list of articles
    df_sub = list_df_article[chunk_index]

    # drop na
    df_sub = df_sub.dropna(subset=["post_id"])
    
    # get responses from all post_id
    responses = get_post_responses(df_sub["post_id"])
    
    # create dataframe
    df_user = pd.DataFrame()
    
    # loop over each responses, collect user id
    for r in responses:
        post_id = r["inResponseToPostId"]
        response_user_id = r["creatorId"]
    
        df_user = df_user.append(pd.DataFrame([{"user_id":response_user_id, "post_id":post_id}]))
    
    # save to csv
    df_user.to_csv("data/response/users_response_%s.csv" % chunk_index, encoding='utf-8', index=False)

    print("Successfully retrieved responses from dataframe %s / %s" % (chunk_index+1, len(list_df_article)+1))

    return



def get_user_information():

    # read dataframe with raw user information
    df = read_data("response")

    # merge rows of same user
    df = df.groupby(["user_id"]).agg({"post_id":lambda x: ', '.join(x)})

    # reset index
    df.reset_index(level=0, inplace=True)

    # chunk size
    n = 600
    
    # split dataframe into subset
    list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]
    
    print("Getting user information from dataframe %s / %s" % (chunk_index_userinfo+1, len(list_df)))
    
    # sub dataframe of list of articles
    df_sub = list_df[chunk_index_userinfo]
    
    # retrieve user information
    df_sub["userinfo"] = df_sub["user_id"].apply(get_userinfo)
    
    # save to csv
    df_sub.to_csv("data/user_detail/users_%s.csv" % chunk_index_userinfo, encoding='utf-8', index=False)

    print("Successfully retrieved user information from dataframe %s / %s" % (chunk_index_userinfo+1, len(list_df)+1))



def extract_most_common_keywords():

    # read dataframe containing detailed user information
    df = read_data("user_detail")

    # convert uesr info from string to dict
    df["userinfo"] = df.userinfo.apply(ast.literal_eval)

    # convert dict to columns
    df = pd.concat([df.drop(['userinfo'], axis=1), df['userinfo'].apply(pd.Series)], axis=1)

    # extract keywords from bio
    df["tag_all"] = df["bio"].apply(tag_extraction)

    # collect all keywords
    all_keywords = collections.Counter()
    for user_keyword in df["tag_all"]:
        for key in user_keyword:
            all_keywords[key] +=1

    # select top keywords from all users
    keywords_most_common = dict(all_keywords)

    # remove common words from keywords
    keyword_filter = ["co", "'", "com", "www", "io", "https :// www", "http :// www", "org",
                        "make", "love", "work", "working", "live", "trying", "views", "net", "time", "find",
                        "like","’", "“", "way", "everything", "know", "uk", "dreamer", "want", "maker", "one",
                        "read", "ly", "night", "gmail", "formerly", "get", "born", "lot","day","also",
                        "father", "life", "world", "write", "husband", "future", "writing", "things",
                        "head", "lover", "people", "passion", "web", "learn", "self", "follow", "living", "previously"
                        "human", "traveler", "internet", "reader", "think", "front", "interested", "passionate", "linkedin"
                        "blogger", "learning", "dad", "ex", "twitter", "travel", "blog", "thinker", "previously", "human",
                        "heart", "building", "full", "thoughts", "curious", "food", "interests", "share"]
    #keyword_add = ["phd", "graduate", "professor"]
    for common_words in keyword_filter:
        keywords_most_common.pop(common_words, None)

    # select top keywords from all users
    keywords_most_common = collections.Counter(keywords_most_common).most_common(80)

    # save most common keywords for visualization
    pd.DataFrame.from_dict(dict(keywords_most_common), orient="index").to_csv("data/keywords/df.csv")

    # save to csv
    print("Successfully extracted most common keywords from user profiles")

    return

def decorate_group():

    # read dataframe containing detailed user information
    df = read_data("user_detail")

    # method used for user classification
    method = "medium"

    # detailed user information to use
    user_detail = "bio"

    # convert uesr info from string to dict
    df["userinfo"] = df.userinfo.apply(ast.literal_eval)

    # convert dict to columns
    df = pd.concat([df.drop(['userinfo'], axis=1), df['userinfo'].apply(pd.Series)], axis=1)

    # add column to specify uer group. By default, all user belongs to group 3
    df["group_%s" % method] = 3

    # classfy users by bio
    group1a = "Data scientist|data scientist|Data Scientist"
    group2a = "Data science|Data Science|data science"
    group2b = "machine learning|Machine learning|Machine Learning"
    group2c = "engineering|engineer|Engineering|Engineer"
    group2d = "student|Student|candidate|Candidate|Amateur|amateur"


    # group 2
    df.loc[df[user_detail].str.contains(group2a), ["group_%s" % method]] = 2
    df.loc[df[user_detail].str.contains(group2b), ["group_%s" % method]] = 2
    df.loc[df[user_detail].str.contains(group2c), ["group_%s" % method]] = 2
    df.loc[df[user_detail].str.contains(group2d), ["group_%s" % method]] = 2


    # group 1
    df.loc[df[user_detail].str.contains(group1a), ["group_%s" % method]] = 1

    # sub dataframe for each group
    df1 = df.loc[df['group_%s' % method]==1]
    df2 = df.loc[df['group_%s' % method]==2]
    df3 = df.loc[df['group_%s' % method]==3]

    # sort by group number
    df = df.sort_values(by=['group_%s' % method])

    # extract keywords from bio
    df["keyword"] = df["bio"].apply(trim_bio)

    # save to csv
    df.to_csv("data/user_detail_medium/df.csv", encoding='utf-8', index=False)
    print("Successfully decorated dataframe with user group")

    return

# Extact keywords using Rake
def tag_extraction(x):
    if pd.isnull(x):
        return []

    r = Rake()                          # initialize rake
    r.extract_keywords_from_text(x)     # Extraction given the text.
    keywords = r.get_ranked_phrases()   # ranked keywords

    # special care for important words
    for index, word in enumerate(keywords):
        if "data scientist" in word:
            keywords[index] = "data scientist"
        if "machine learning" in word:
            keywords[index] = "machine learning"
    
    return keywords                 # return ranked phrases

# Extact keywords using Rake
def tag_most_common(x, top_keywords):
    r = Rake()                          # initialize rake
    r.extract_keywords_from_text(x)     # Extraction given the text.
    keywords = r.get_ranked_phrases()   # ranked keywords

    # special care for important words
    for index, word in enumerate(keywords):
        if "data scientist" in word:
            keywords[index] = "data scientist"
        if "machine learning" in word:
            keywords[index] = "machine learning"

    # return only keywords in top most common keywords
    return list(set(keywords) & set(top_keywords)) 


def trim_bio(text):

    # keywords to return
    keywords = []

    ## define important words
    #important_words = [ ["data", "science"],
    #                    ["data", "scientist"],
    #                    ["machine", "learning"],
    #                    ["data", "engineer"],
    #                    ["data", "analytics"],
    #                    ["artificial", "intelligence"],
    #                    ["ai"], ["phd"], ["founder"], ["professor"],["candidate"],["ceo"],
    #                    ["student"], ["engineer"], ["computer", "science"]
    #                    ]
 
    # load from file after custom edit
    df_keyword = pd.read_csv("data/keywords/df.csv")

    ## convert df to list
    important_words=df_keyword["Unnamed: 0"].tolist()

    ## format important words so that they can be registered to tokenizer
    important_words = [ x.split() for x in important_words]

    # initialize tokenizer
    tokenizer = MWETokenizer()              
    for iw in important_words:
        tokenizer.add_mwe([x for x in iw])  # add important words
        #tokenizer.add_mwe(iw)  # add important words

    # tokenize bio
    tokens = tokenizer.tokenize([word.lower() for word in text.split()])

    # find important words from tokens, append it to keyword
    for iw in important_words:
        iw_joined = "_".join(iw)
        if (iw_joined in tokens):
            keywords.append(iw_joined)

    return keywords


if __name__ == '__main__':

    # download list of articles on medium
    if (DownloadArticleList):
        download_article_list(sdy, sdm, sdd, edy, edm, edd)

    # get responses from list of articles on medium
    if (GetResponses):
        get_user_responses()

    # get user information from medium
    if (GetUserInfo):
        get_user_information()

    # extract most common keywords from corpus of user profile
    if (ExtractMostCommon):
        extract_most_common_keywords()

    # decorate dataframe with user groups by keyword matching
    if (DecorateGroup):
        decorate_group()
