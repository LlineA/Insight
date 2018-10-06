read me data

data science iteration 1 (1 month DS tags)
data science iteration 2 (3000 tags)
=> 1,085,450 rows, 24 columns

remove non English rows:
=> 979,350

remove duplicates:
=>152,166

tag_list= sequence of 0 to 5 tags (152,166 rows, 5 columns)

frequency = > frequency of each tag: 51672 tags, frequency
remove tags if appear only 0,1 or 2 => 17566 tags
=> 10258 tags in our dictionary, 7308 not there...

152166 rows, with 17566 different tags:
Word2Vec(vocab=11998, size=100, alpha=0.025)
