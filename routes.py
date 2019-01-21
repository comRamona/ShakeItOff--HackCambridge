
import requests
import numpy as np
import json
import random
from flask import Flask, render_template, request, jsonify
from forms import LoginForm
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
from fitbit_goal import set_goal, calories_to_steps
import cloudinary
import cloudinary.api
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from food_classification import *
import os

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

app = Flask(__name__)
app.config.from_object('config')

'''
Download GloVe file from
https://nlp.stanford.edu/projects/glove/
'''
gloveName = 'glove.6B.50d.txt'
if os.path.isfile(gloveName):
   with open(gloveName, 'r') as f:
       vectors = {}
       for line in f:
           vals = line.rstrip().split(' ')
           vectors[vals[0]] = [float(x) for x in vals[1:]]


@app.route('/', methods=['GET', 'POST'])
def home():
    upload_result = None
    thumbnail_url1 = None
    thumbnail_url2 = None
    if request.method == 'POST':
        file_to_upload = request.files['file']
        if file_to_upload:
            upload_result = upload(file_to_upload)
            image_url = upload_result['url']
            stuff = process_image(image_url)
            set_goal(stuff['total'])
            stuff['steps'] = int(calories_to_steps(stuff['total']))
            thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=200,
                                                     height=400)
            thumbnail_url2, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=200,
                                                     height=400, radius=20, effect="sepia")
            return render_template('login.html', stuff=stuff, thumbnail_url1=thumbnail_url1,
                           thumbnail_url2=thumbnail_url2, image_url=image_url)
    return render_template('login.html')


@app.route('/word_embedding', methods = ['POST'])
def word_embedding():
   s = request.json['word']
   vecs = [np.array(vectors[w]).reshape(1,-1) for w in s.split() if w in vectors and len(vectors[w]) == 50]
   if(len(vecs)==0):
       vecs = np.zeros(50).reshape(1,-1)
   mn = list(np.mean(vecs, 0).reshape(-1))
   return json.dumps(mn)

def process_image(image_url):
    analysis = send_request(image_url)
    items = clean_info(parse_result(analysis))
    results = classify_food(items)
    foods = match_classification(items, results)
    return compute_calories(foods)

    
@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                           title='Upload',
                           form=form)

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)
