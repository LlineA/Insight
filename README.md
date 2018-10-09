# TagIt –  Get your story seen
TagIt is a recommender system designed to improve user experience on medium.com 
You can view the slides I made to describe the project here : [TagIt Presentation](https://github.com/LlineA/Insight/blob/master/TagIt_Presentation.pdf)

## Summary
TagIt is a web app that uses a word embedding model to recommend relevant and popular tags to medium blogpost writers.
[TagIt Development](https://github.com/LlineA/Insight/tree/master/Tagit%20Development)  - contains all the development steps of TagIt.
[TagIt Application](https://github.com/LlineA/Insight/tree/master/Tagit%20Application)  - contains the source code for the web app.

## Context and Use case
Medium is an online publishing platform for amateurs and professionals who want to share their ideas. With the large number of daily publications and the rigidity of the platform, writers might have a hard time reaching their audience. To maximize the number of readers, writers must optimally choose up to 5 tags to describe the content of the article. 
To optimize the tag selection process, I developed TagIt a web app that uses a word embedding model to recommend relevant and popular tags to medium blogpost writers.

## Data Collection
Source code for this section is available in [TagIt Development](https://github.com/LlineA/Insight/tree/master/Tagit%20Development) 

Data is collected by web scraping from medium.com. 
Two scrapers are used :
 - the first scraper gets information on articles published with specified tags. 
 - the second scraper gets the number of followers of specified tags.
 
I used Python request, BeautifulSoup, selenium, and json libraries to scrape and parse the html and json data.

## Exploratory analysis
### Description of the database
My database originally included 1 million of rows, with the following information (columns) about articles:
 - post id
 - post publication time
 - author id
 - number of claps
 - number of comments
 - detected language
 - list of tags
 - URL link
 - title

### Data Cleaning 
I removed duplicates, kept posts published in English only, lower-cased the tags, curated the formatting of numbers.

After these steps, the database is constituted of 155k articles.

### Numbers
In the database there are:
 - 71,000 unique authors
 - 55,000 unique tags
 
Claps:
 - 38% of articles have 0 clap
 - 77% of articles have 10 claps or less
 - only 20% of articles have 20 claps or more

## Recommendation System
The goal of TagIt is to recommend tags to the writer that are relevant and popular.

### Current user experience
Currently medium recommends tags based on auto-completion of what the writer is typing, for instance if the user types "c... o... d..." (to talk about code) medium recommends **code** and **coding**.
TagIt recommends tags that are close in meaning to what the writer is typing, for instance **programming**.

### Tag Embedding Model : How to Recommend Relevant Tags
To find tags that are relevant I trained a tag embedding model using word2vec. The input data is the list of tags used in the 155k articles in the database.

### Tag Popularity Dictionary : How to Recommend Popular Tags
To recommend popular tags I chose to recommend tags that have a higher number of followers than the tag the writer had in mind. The data was acquired using the second scraper. 

### Visualization of the recommendation
The output is displayed as a bubble graph designed to improve readabilty of the results by the users.

## Web Application
I built a web application to demonstrate the recommender system. The web app is built using Python and Flask. The source coude can be found in [TagIt Application](https://github.com/LlineA/Insight/tree/master/Tagit%20Application).

## Conclusion
In conclusion, with TagIt we can improve the user experience on medium.com by helping the writer choose tags that are relevant and accurate to describe the content of their blogpost so that their targeted audience can find them. 
