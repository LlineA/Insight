# Tag it –  Get your story seen
Tag it is a recommender system for tag selection on medium

## Summary
Tag it is a web app that uses a word embedding model to recommend relevant and popular tags to medium blogpost writers
This repository- Tagit Development-  contains all the development steps of tag it.
The repository - Tagit Application - contains the code for the web app.

## Introduction
Medium is an online publishing platform for amateurs and professionals who want to share their ideas. With the large number of daily publications and the rigidity of the platform, writers might have a hard time reaching their audience. To maximize the number of readers, writers must optimally choose up to 5 tags to describe the content of the article. To optimize the tag selection process, I developed Tag it a web app that uses a word embedding model to recommend relevant and popular tags to medium blogpost writers.

## Data Collection
Source code for this section is available in [Tagit Development](https://github.com/LlineA/Insight/tree/master/Tagit%20Development) 

Data is collected by web scraping from medium.com. 
Two scrapers are used :
 - the first scaper gets information on articles published with specified tags. 
 - the second scraper gets the number of followers of specified tags.
 
I used Python request, BeautifulSoup, selenium, and json libraries to scrape and parse the html and json data.

## Exploratory analysis
# Number of articles

My database originally included 1 million of rows, with the following information (columns) about articles:
- post id
- author id
- number of claps
- detected language
- list of tags
- url link
- title
After data cleaning (removing duplicates, keeping posts published in English only), it is now constituted of 155k articles.

# Number of authors
There are  unique authors. On average authors published articles.

# Comments, claps
# Tags
# Tag followers
## Recommendation system
# Tag embedding model
# Tag popularity
## Web application
## Conclusion
## Authors
