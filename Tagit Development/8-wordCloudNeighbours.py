# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 18:12:39 2018

@author: Graccolab
"""

# Libraries
import matplotlib.pyplot as plt
from wordcloud import WordCloud


 
# Create a list of word
text=("Python Python Python Matplotlib Matplotlib Seaborn Network Plot Violin Chart Pandas Datascience Wordcloud Spider Radar Parrallel Alpha Color Brewer Density Scatter Barplot Barplot Boxplot Violinplot Treemap Stacked Area Chart Chart Visualization Dataviz Donut Pie Time-Series Wordcloud Wordcloud Sankey Bubble")
 
# Create the wordcloud object
wordcloud = WordCloud(width=680, height=680, margin=0, prefer_horizontal=1, min_font_size=12,normalize_plurals=False, background_color="white").generate(text)
 
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()

wordcloud = WordCloud(width=680, height=680, margin=0, prefer_horizontal=1)
wordcloud2=wordcloud.fit_words({'aa':1,'bb':10})


plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.savefig('tags/test.png')

