# TagIt –  Get your story seen
TagIt is a recommender system designed to improve user experience on medium.com 

## Summary
TagIt is a web app that uses a word embedding model to recommend relevant and popular tags to medium blogpost writers.
[Tagit Development](https://github.com/LlineA/Insight/tree/master/Tagit%20Development)  - contains all the development steps of TagIt.
[Tagit Application](https://github.com/LlineA/Insight/tree/master/Tagit%20Application)  - contains the source code for the web app.

## Context and Use case
Medium is an online publishing platform for amateurs and professionals who want to share their ideas. With the large number of daily publications and the rigidity of the platform, writers might have a hard time reaching their audience. To maximize the number of readers, writers must optimally choose up to 5 tags to describe the content of the article. 
To optimize the tag selection process, I developed TagIt a web app that uses a word embedding model to recommend relevant and popular tags to medium blogpost writers.

## Data Collection
Source code for this section is available in [Tagit Development](https://github.com/LlineA/Insight/tree/master/Tagit%20Development) 

Data is collected by web scraping from medium.com. 
Two scrapers are used :
 - the first scaper gets information on articles published with specified tags. 
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
- url link
- title

### Data cleaning 
I removed duplicates, kept posts published in English only, lower-cased the tags, curated the formatting of numbers.

After these steps, the database is constituted of 155k articles.

### A few numbers
In the database there are:
- 71,000 unique authors
- 55,000 unique tags

- 38% of articles have 0 clap
- 77% of articles have 10 claps or less
- only 20% of articles have 20 claps or more

## Recommendation system
The goal of TagIt is to recomment tags to the writer that are relevant and popular.
### Current user experience
Currently medium recommends tags based on auto-completion of what the writer is typing, for instance if the user types "c... o... d..." (to talk about code) medium recommends **code** and **coding**.
TagIt recommends tags that are close in meaning to what the writer is typing, for instance **programming**.

### Tag embedding model : how to recommend relevant tags
To find tags that are relevant I trained a tag embedding model using word2vec. The input data is the list of tags used in the 155k articles in the database.

### Tag popularity dictionary : how tp recommend popular tags
To recommend popular tags I chose to recommend tags that have a higher number of followers than the tag the writer had in mind. The data was acquired using the second scraper. 

## Web application
I built a web application to demonstrate the recommender system. The web app is built using Python and Flask. The source coude can be found in [Tagit Application](https://github.com/LlineA/Insight/tree/master/Tagit%20Application).

## Conclusion
In conclusion, with TagIt we can improve the user experience on medium.com by helping the writer choose tags that are relevant and accurate to describe the content of their blogpost so that their targeted audience can find them. 
