from __future__ import division, print_function
from flask import *
from flask import Flask,jsonify
from fastai import *
from fastai.vision import *
from fastai.callbacks.hooks import *
from flask_cors import CORS,cross_origin
import os
import shutil
import pickle
from pathlib import Path
from lshashpy3 import LSHash
import tqdm
from tqdm import tqdm_notebook
from numpy import transpose
from PIL import Image
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Define a flask app
app = Flask(__name__)

def convert_vec(vec):
    convert=PoolFlatten()
    vec=convert(tensor(vec)).detach().numpy().flatten()
    return vec
def hook(module, input, output):
    outputs.append(output)


def get_activations(img):
    outputs.clear()
    xb,yb=learn.data.one_item(img)
    n=[7]
    for i in n:
        handle=encoder[i].register_forward_hook(hook)
        y=encoder.eval()(xb)
        handle.remove()
    return outputs
def save_matches(response):
    filenames.clear()
    shutil.rmtree(dst_dir)
    os.makedirs(dst_dir)
    for i in range(0,len(response)):
        string=str(response[i][0][1])
        string2=string.split("\\")
        string2=string2[7]
        #filenames.append(string2+ ' Score: '+ str(round(1-response[i][1],3)))
        similarity_score.append(str(round(1-response[i][1],3)))
        shutil.copy(os.path.join(src_dir, string2), dst_dir)
        fpath=os.path.join(dst_dir,string2)
        filenames.append(fpath[37:])
    dictionary=dict(zip(filenames,similarity_score))
    return dictionary
    
# load the learner, features and hash tables
path = Path(r"C:\Users\chant\Desktop\CM\New folder")
lsh_all=pickle.load(open(path/'finalLshtables5.p','rb'))
learn = load_learner(path)
encoder=learn.model[0]
def LSH(option):
    if option=="All":
        lsh=lsh_all
    elif option=="Necklaces":
        #feature_dict=feature_dict_necklaces
        lsh=lsh_necklaces
    elif option=="Bracelets":
        #feature_dict=feature_dict_bracelets
        lsh=lsh_bracelets
    elif option=="Rings":
        #feature_dict=feature_dict_rings
        lsh=lsh_rings
    elif option=="Earrings":
        #feature_dict=feature_dict_earrings
        lsh=lsh_earrings
        
    return lsh 

#Get similar images function
filenames=[]
similarity_score=[]
outputs=[]
f_response=[]
src_dir = r"C:\Users\chant\Desktop\CM\New folder\Jewellery App\Final_data"
dst_dir = r"C:\Users\chant\Desktop\CM\New folder\static\pics"
bracelets_list=pickle.load(open(path/'Bracelets_List.p','rb'))
earrings_list=pickle.load(open(path/'Earrings_List.p','rb'))
necklaces_list=pickle.load(open(path/'Necklaces_List.p','rb'))
rings_list=pickle.load(open(path/'Rings_List.p','rb'))

n_results=10

def find_category(response,option,n_results):
    f_response.clear()
    if option=="All":
        response=response[:n_results]
    if option=="Necklaces":
        for i in range(0,len(response)):
            trial_string=str(response[i][0][1]).split("\\")[-1]
            for j in range(len(necklaces_list)):
                if trial_string in necklaces_list[j]:
                    f_response.append(response[i])
        response=f_response[:n_results]
    
    if option=="Bracelets":
        for i in range(0,len(response)):
            trial_string=str(response[i][0][1]).split("\\")[-1]
            for j in range(len(bracelets_list)):
                if trial_string in bracelets_list[j]:
                    f_response.append(response[i])
        response=f_response[:n_results]
    
    if option=="Earrings":
        for i in range(0,len(response)):
            trial_string=str(response[i][0][1]).split("\\")[-1]
            for j in range(len(earrings_list)):
                if trial_string in earrings_list[j]:
                    f_response.append(response[i])
        response=f_response[:n_results]
    
    if option=="Rings":
        for i in range(0,len(response)):
            trial_string=str(response[i][0][1]).split("\\")[-1]
            for j in range(len(rings_list)):
                if trial_string in rings_list[j]:
                    f_response.append(response[i])
        response=f_response[:n_results]
    
    return response
        

        

def get_similar_images(input_img_path,option,n_results):
    img=Image.open(input_img_path)
    newsize=(480,480)
    img=img.resize(newsize)
    img.save(str(input_img_path))
    input_img=open_image(Path(input_img_path))
    #_ = learn.predict(input_img)
    vect = get_activations(input_img)[-1]
    #n_items=no_items
    n_items=10
    vect=convert_vec(vect)
    response = lsh_all.query(vect, num_results=500, distance_func="cosine")
    response=find_category(response,option,n_results)
    #FileNames
    filenames=save_matches(response)
    return filenames
    
  

@app.route('/', methods=['GET','POST'])
def index():
    # Main page
    return render_template('index.html')
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        #g = request.form.get("Category")
        f = request.files['file']
        g = request.form['value']
        g=str(g)
        g=g[1:-1]
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        # Make prediction
        preds = get_similar_images(file_path,g,n_results)
        return jsonify({'filenames':list(preds.keys()),'score':list(preds.values())})
        #return str(g=='Bracelets')
        #return jsonify(preds)
    return None


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=50000, debug=True)