from flask import Flask , render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from shutil import copyfile
#Import for processing : 
from utils.colordescriptor import ColorDescriptor
from utils.fourierdescriptor import ShapeDescriptor
from utils.texturedescriptor import TextureDescriptor
from utils.searcher import Searcher
from utils.generator import generate_weights,reset_weights
import argparse
import cv2
import numpy as np


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #Initialize our database
db = SQLAlchemy(app)

#Static parameters that we'll be using in our project
app.config['IMAGE_DATASET'] = "F://MASTER MBD S3//Analysis Mining and indexing in big multimedia system//Mini-projet//Mini-proj1//dataset"
app.config['IMAGE_UPLOADS'] = "F://MASTER MBD S3//Analysis Mining and indexing in big multimedia system//Mini-projet//Mini-proj1//Search Engine//static//img//uploads"
app.config['IMAGE_RESULTS'] = "F://MASTER MBD S3//Analysis Mining and indexing in big multimedia system//Mini-projet//Mini-proj1//Search Engine//static//img//results"
app.config['IMAGE_INDEX'] = "F://MASTER MBD S3//Analysis Mining and indexing in big multimedia system//Mini-projet//Mini-proj1//Search Engine//indexes"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ['PNG','JPG','JPEG']
app.config["MAX_IMAGE_SIZE"] = 0.5 * 1024 * 1024 #In bytes

def allowed_image(filename) : #For security reason we're checking if its is an allowed image extension
    if not "." in filename :
        return False
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"] : 
        return True 
    else :
        return False
def allowed_image_filesize(filesize): #Check the size of the image
    if int(filesize) < app.config["MAX_IMAGE_SIZE"] : 
        return True
    else :
        return False


@app.route('/',methods=['POST','GET'])
def index():
    reset_weights() #To empty the file weights.txt from old generated weights
    if request.method == 'POST':
        descriptors_list = request.form.getlist('mycheckbox') #Get the seletected descriptors
        descriptors = '' #Initializing
        for descrip in descriptors_list:
            descriptors += str(descrip)+',' #Stock descriptors in a string to pass it as an argument 
        if request.files :
            if not allowed_image_filesize(request.cookies.get("filesize")): #If the input image size is to big
                print("Size of image to big")
                return redirect(request.url)
            image = request.files['image']
            if image.filename == "": #If the input image has no name
                print("Image Must have a filename")
                return redirect(request.url)
            if not allowed_image(image.filename): #Case extension of the input image not allowed
                print("Extension is not allowed")
                return redirect(request.url)
            else : 
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['IMAGE_UPLOADS'],filename)) #Saving the input image to upload file
                print("Image (",filename,") Saved")
                link = '/results/'+image.filename+'/'+descriptors[:-1] # -1 to take off the last ','
            return redirect(link)
    else :
        return render_template('index.html')

@app.route('/results/<filename>/<descriptors>',methods=['POST','GET'])
def results(filename,descriptors):
    input_file = filename #Name of input image 'the file name in static/img/upload/filename'
    cd = ColorDescriptor((8,12,3)) #Use same number of bins in the index.py
    td = TextureDescriptor() 
    sd = ShapeDescriptor()
    #Load the given image and describe it
    query = cv2.imread(os.path.join(app.config['IMAGE_UPLOADS'],filename)) #Read the input image
    query_grey = cv2.cvtColor(query, cv2.COLOR_BGR2GRAY) #Get the gray image to run it for Texture and shape descriptor
    features_color = cd.describe(query) #Apply color descriptor to get the features of the input image
    feature_texture = td.lbp(query_grey) #Apply texture descriptor to get the features of the input image
    feature_shape = sd.extractFeatures(query_grey) #Apply shape descriptor to get the features of the input image
    #Search for similairs pictures using the searcher.py
    searcher = Searcher(os.path.join(app.config['IMAGE_INDEX'],"color.csv"),os.path.join(app.config['IMAGE_INDEX'],"texture.csv"),os.path.join(app.config['IMAGE_INDEX'],"shapes.csv"))
    descriptors = descriptors.split(',') #To get a list of descriptors
    print(descriptors)
    if request.method == 'POST': # In case we're in search again 
        good_list = request.form.getlist('checkgood') #Get the good result from the last time
        good_path = [] #To stock path of the good result from the last time
        good_score = [] #To stock path of the score of good result from the last time
        for elemen in good_list : 
            good_path.append(elemen.split(',')[0]) #Because good_list was like : ['1.png,0.9556','3.jpg,0.0545454']
            good_score.append(elemen.split(',')[1]) 
        weights = generate_weights() #This function from generator.py that generator new weights for out searcher
        print("New weights : "+str(weights))
        results = searcher.search(features_color,feature_texture,feature_shape,descriptors=descriptors,w=weights) #Look for similar pictures with the new weights of the descriptors
        paths_results = [] #To save the new results
        score_results = []
        for i,(score,resultID) in enumerate(results) : 
        #Load the result image 
            #print(i,": ",resultID)
            newfile = str(i+1)+".jpg"
            paths_results.append(newfile)
            score_results.append(score)
            if newfile not in good_path : #If it's wasn't selected as good result for the last time then copy it to the result folders
                copyfile(os.path.join(app.config['IMAGE_DATASET'],resultID),os.path.join(app.config['IMAGE_RESULTS'],newfile))
      
        good_path.extend(paths_results) #Add new results to old ones
        good_score.extend(score_results)
        good_path = list(dict.fromkeys(good_path))[:10] #take only the top 10 since we're having more because we concat the good results from last time to the 10 new results
        good_score = list(dict.fromkeys(good_score))[:10]
        return render_template('result.html',input_file=input_file,results=zip(good_path,good_score))
    else : #Case of get request means first results no feed back yet
        results = searcher.search(features_color,feature_texture,feature_shape,descriptors=descriptors) #Search for similar pictures with default weights = 1/3
        paths_results = []
        score_results = []
        for i,(score,resultID) in enumerate(results) : 
        #Load the result image 
            #print(i,": ",resultID)
            newfile = str(i+1)+".jpg"
            paths_results.append(newfile)
            score_results.append(score)
            copyfile(os.path.join(app.config['IMAGE_DATASET'],resultID),os.path.join(app.config['IMAGE_RESULTS'],newfile))

        return render_template('result.html',input_file=input_file,results=zip(paths_results,score_results))

# contact route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# No caching at all for API endpoints.
@app.after_request
def add_header(response): #Just to fix a bug (the results didnt get updated because they got stored on the browser cache)
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == "__main__":
    app.run(debug=True)
    
