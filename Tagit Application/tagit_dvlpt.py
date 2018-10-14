#from flask import render_template
#from flask_tagit import app
import pandas as pd
#from flask import request
#from random import randint
import tagit_functions as tagit
#import datetime
#import os
#import pickle
import matplotlib.pyplot as plt
#import cv2
import numpy as np


from sklearn.manifold import TSNE
# Parameters:
model_name="word2vecDS_tag.model"      #model_name="word2vec_tag.model"
pop_dict_name="popDict2"               #pop_dict_name="follower_nb_dictionnary"
neighbour_nb=100

# rename images(to work around cache pb)
sorry_image_filename=tagit.rename('sorry','flask_tagit/static')


# Load word2vec model  and popularity dictionary  
model=tagit.load_model(model_name)
word_vectors = model.wv 
popularity_dictionary=tagit.get_dictionary(pop_dict_name)

# Pull 'tag' from input field and convert input to lowercase
#tag_input = request.args.get('tag_input')
#tag_input_raw=request.args.get('tag_input')
tag_input_raw='code'
tag_input = tag_input_raw.lower()
    
if tag_input not in word_vectors.vocab:
       print('case1')#The tag is not in our database
       # Case 1 : Not in database
#       return render_template("output_unknown_tag.html",
#                              tag_input=tag_input_raw,
#                              img_name_sorry=sorry_image_filename
#                              )
      #The tag is in the database

#Get neighbours
neighbour_nb=200
most_similar_tags=tagit.most_similar(tag_input,model,neighbour_nb)
       
#Check if tag_input is in popularity dictionary:                     
if tag_input not in popularity_dictionary: # The tag is not in the popularity dictionary    
       print('case2')          
       # get the most populars tags around it even if we don't know if it's better than the one we have  
       
       # (ICI : quand meme afficher le nuage de voisins)
#       return render_template("output_unknown_number.html",
#                              tag_input=tag_input_raw,                         
#                              tag_output=tag_output
#                              )                                                                
# Case 2b: we have all info on the tag:
# Get number of followers
follower_nb_to_beat=popularity_dictionary[tag_input]  

# Find better tags
better_choices_pop,better_choices_dist,tag_dict=tagit.find_more_popular_tags(most_similar_tags,follower_nb_to_beat,popularity_dictionary)



print(tag_dict)
tag_dict['popularity'] = tag_dict['popularity'].apply(pd.to_numeric)
#ax1 = tag_dict.plot.scatter(x='distance', y='popularity')

arr = np.empty((0,100), dtype='f')
pop = np.empty((0,1), dtype='f')
tag_labels = [tag_input]
    
# add the vector for each of the closest words to the arra
arr = np.append(arr, np.array([model[tag_input]]), axis=0)
pop = np.append(pop, np.full((1,1),follower_nb_to_beat), axis=0)

for tag in better_choices_pop:
       tag_labels.append(tag)
       tag_vector = model[tag]
       tag_pop=better_choices_pop[tag]
       
       arr = np.append(arr, np.array([tag_vector]), axis=0)
       pop = np.append(pop,np.full((1,1),tag_pop))
       
    # find tsne coords for 2 dimensions
tsne = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
Y = tsne.fit_transform(arr)
x_coords = Y[:, 0]
y_coords = Y[:, 1]

# display scatter plot
c= pop
#ax=plt.scatter(x_coords, y_coords,c='white')       
ax=plt.scatter(x_coords, y_coords,s=pop) #,c=c,cmap='cool')
for label, x, y in zip(tag_labels, x_coords, y_coords):
       plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points', ha='center',fontsize=25)
offset_x=0.1*abs(x_coords.max()-x_coords.min())
offset_y=0.1*abs(y_coords.max()-y_coords.min())
plt.xlim(x_coords.min()-  offset_x, x_coords.max() + offset_x)
plt.ylim(y_coords.min() - offset_y, y_coords.max() + offset_y)
plt.axis('off')
ax.set_facecolor('xkcd:salmon')
plt.show()
#ax=plt.scatter(x_coords, y_coords,c='white')       

fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig('test2png.png', dpi=500)

##%%
#better_tags=[]
#better_followers=[]
#follower_nb_1=[]
#follower_nb_2=[]
#follower_nb_3=[]
#
#for tag, follower in better_choices_pop.items():
#       better_tags.append(tag)
#       better_followers.append(follower)
#  
#       #check if there are better possible tags        
#if len(better_tags)>=3:
#       tag_output_1=better_tags[0]
#       follower_nb_1=tagit.human_format(popularity_dictionary[tag_output_1])
#       tag_output_2=better_tags[1]
#       follower_nb_2=tagit.human_format(popularity_dictionary[tag_output_2])
#       tag_output_3=better_tags[2]
#       follower_nb_3=tagit.human_format(popularity_dictionary[tag_output_3])
#
#elif len(better_tags)==2:
#       tag_output_1=better_tags[0]
#       follower_nb_1=tagit.human_format(popularity_dictionary[tag_output_1])
#       tag_output_2=better_tags[1]
#       follower_nb_2=tagit.human_format(popularity_dictionary[tag_output_2])
#       tag_output_3="_"
#elif len(better_tags)==1:
#       tag_output_1=better_tags[0]
#       follower_nb_1=tagit.human_format(popularity_dictionary[tag_output_1])
#       tag_output_2="_"
#       tag_output_3="_"
#else:
#       happy_image_filename=tagit.rename('happy','flask_tagit/static')
#       print('case3')
##       return render_template("output_no_better.html",
##                tag_input=tag_input_raw,
##                input_follower_nb=tagit.human_format(follower_nb_to_beat),
##                img_name_1=happy_image_filename)
#       
#  
##doit etre maj:
#recommendation_image_filename=tagit.create_word_cloud(better_choices)
#return render_template("output_recommendation.html",
#                tag_input=tag_input_raw,
#                input_follower_nb=tagit.human_format(follower_nb_to_beat),
#                tag_output_1 = tag_output_1,
#                tag_output_2 = tag_output_2,
#                tag_output_3 = tag_output_3,
#                follower_nb_1=follower_nb_1,
#                follower_nb_2=follower_nb_2,
#                follower_nb_3=follower_nb_3,
#                img_name_1=recommendation_image_filename)
#
