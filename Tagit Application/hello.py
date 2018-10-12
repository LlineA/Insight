# -*- coding: utf-8 -*-

# import the Flask class from the flask module
from flask import Flask, render_template, request
import lolo_function as lolo

# create the application object
app = Flask(__name__)


@app.route('/',methods=["GET","POST"])
def home():
    return render_template('index.html')  # render a template

@app.route('/output')
def tag_output():

       # Load word2vec model  and popularity dictionary  
       model=lolo.load_model("word2vecDS_tag.model")
       popularity_dictionary=lolo.get_dictionary("popDict2")
       
       # Pull 'tag' from input field and convert input to lowercase
       tag_input =request.args.get('tag_input')      
       
       
       # Case if empty
       if tag_input.lower() == '':             
              return render_template("index.html",
                                     tag_input = tag_input,
                                     form_result="None")
       elif tag_input.lower() not in model.vocab:              
              return render_template("index.html",
                                     tag_input = tag_input,
                                     form_result="not_found")
       elif tag_input.lower() not in popularity_dictionary:              
              return render_template("index.html",
                                     tag_input = tag_input,
                                     form_result="unknown_followers")
       else:  
              # We have all the info we need:
              #Get neighbours
              most_similar_tags=lolo.most_similar(tag_input.lower(),model)                   
              # Get number of followers
              follower_nb_to_beat=popularity_dictionary[tag_input.lower()]                
              # Find better tags
              better_choices_pop, better_choices_dist, sorted_tag_dict, list_better_choices_pop = lolo.find_more_popular_tags(most_similar_tags,
                                                                                                                            follower_nb_to_beat,
                                                                                                                            popularity_dictionary)
              if len(better_choices_pop)==0:              
                     return render_template("index.html",
                                      tag_input=tag_input,
                                      input_follower_nb=lolo.human_format(follower_nb_to_beat),                              
                                      form_result="found_best"
                                      )      
                     
              recommendation_image_filename=lolo.create_word_cloud(better_choices_pop)
              return render_template("index.html",
                              tag_input=tag_input,
                              tag_list=list_better_choices_pop,
                              input_follower_nb=lolo.human_format(follower_nb_to_beat),
                              img_name_1=recommendation_image_filename,
                              form_result="found_not_best")
      
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
    
    
