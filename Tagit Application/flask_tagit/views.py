from flask import render_template
from flask_tagit import app
#import pandas as pd
from flask import request
#from random import randint
import lolo_function as lolo
import datetime
#import os
#import pickle
#import matplotlib.pyplot as plt
import cv2
@app.route('/')
@app.route('/index')
def index():
       return render_template("index.html",
                              title = 'Home', user = { 'nickname': 'Lolo' },
                              )

@app.route('/input')
def tag_input():
       return render_template("input.html")

@app.route('/output')
def tag_output():
       
       # Parameters:
       model_name="word2vecDS_tag.model"      #model_name="word2vec_tag.model"
       pop_dict_name="popDict2"               #pop_dict_name="follower_nb_dictionnary"
       neighbour_nb=100
       
       # rename images(to work around cache pb)
       sorry_image_filename=lolo.rename('sorry','flask_tagit/static')
       
       
       # Load word2vec model  and popularity dictionary  
       model=lolo.load_model(model_name)
       word_vectors = model.wv 
       popularity_dictionary=lolo.get_dictionary(pop_dict_name)
       
       # Pull 'tag' from input field and convert input to lowercase
       #tag_input = request.args.get('tag_input')
       tag_input_raw=request.args.get('tag_input')
       tag_input = tag_input_raw.lower()
    
       if tag_input not in word_vectors.vocab: #The tag is not in our database
              # Case 1 : Not in database
              return render_template("output_unknown_tag.html",
                                     tag_input=tag_input_raw,
                                     img_name_sorry=sorry_image_filename
                                     )
      #The tag is in the database
       
       #Get neighbours
       most_similar_tags=lolo.most_similar(tag_input,model,neighbour_nb)
              
       #Check if tag_input is in popularity dictionary:                     
       if tag_input not in popularity_dictionary: # The tag is not in the popularity dictionary              
              # get the most populars tags around it even if we don't know if it's better than the one we have  
              
              # (ICI : quand meme afficher le nuage de voisins)
              return render_template("output_unknown_number.html",
                                     tag_input=tag_input_raw,                         
                                     tag_output=tag_output
                                     )                                                                
       # Case 2b: we have all info on the tag:
       # Get number of followers
       follower_nb_to_beat=popularity_dictionary[tag_input]  
       
       # Find better tags
       better_choices_pop,better_choices_dist,tag_dict=lolo.find_more_popular_tags(most_similar_tags,follower_nb_to_beat,popularity_dictionary)
       better_tags=[]
       better_followers=[]
       follower_nb_1=[]
       follower_nb_2=[]
       follower_nb_3=[]
       
       for tag, follower in better_choices_pop.items():
              better_tags.append(tag)
              better_followers.append(follower)
  
              #check if there are better possible tags        
       if len(better_tags)>=3:
              tag_output_1=better_tags[0]
              follower_nb_1=lolo.human_format(popularity_dictionary[tag_output_1])
              tag_output_2=better_tags[1]
              follower_nb_2=lolo.human_format(popularity_dictionary[tag_output_2])
              tag_output_3=better_tags[2]
              follower_nb_3=lolo.human_format(popularity_dictionary[tag_output_3])

       elif len(better_tags)==2:
              tag_output_1=better_tags[0]
              follower_nb_1=lolo.human_format(popularity_dictionary[tag_output_1])
              tag_output_2=better_tags[1]
              follower_nb_2=lolo.human_format(popularity_dictionary[tag_output_2])
              tag_output_3="_"
       elif len(better_tags)==1:
              tag_output_1=better_tags[0]
              follower_nb_1=lolo.human_format(popularity_dictionary[tag_output_1])
              tag_output_2="_"
              tag_output_3="_"
       else:
              happy_image_filename=lolo.rename('happy','flask_tagit/static')
              return render_template("output_no_better.html",
                       tag_input=tag_input_raw,
                       input_follower_nb=lolo.human_format(follower_nb_to_beat),
                       img_name_1=happy_image_filename)
              
  
       #doit etre maj:
       recommendation_image_filename=lolo.create_word_cloud(better_choices_pop)
       return render_template("output_recommendation.html",
                       tag_input=tag_input_raw,
                       input_follower_nb=lolo.human_format(follower_nb_to_beat),
                       tag_output_1 = tag_output_1,
                       tag_output_2 = tag_output_2,
                       tag_output_3 = tag_output_3,
                       follower_nb_1=follower_nb_1,
                       follower_nb_2=follower_nb_2,
                       follower_nb_3=follower_nb_3,
                       img_name_1=recommendation_image_filename)

