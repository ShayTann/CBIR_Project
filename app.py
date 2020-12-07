from flask import Flask , render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from shutil import copyfile
#Import for processing : 
from utils.colordescriptor import ColorDescriptor
from utils.searcher import Searcher
import argparse
import cv2



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

app.config['IMAGE_DATASET'] = "F://MASTER MBD S3//Analysis Mining and indexing in big multimedia system//Mini-projet//Mini-proj1//dataset"
app.config['IMAGE_UPLOADS'] = "F://MASTER MBD S3//Analysis Mining and indexing in big multimedia system//Mini-projet//Mini-proj1//Search Engine//static//img//uploads"
app.config['IMAGE_RESULTS'] = "F://MASTER MBD S3//Analysis Mining and indexing in big multimedia system//Mini-projet//Mini-proj1//Search Engine//static//img//results"
app.config['IMAGE_INDEX'] = "F://MASTER MBD S3//Analysis Mining and indexing in big multimedia system//Mini-projet//Mini-proj1//Search Engine//indexes"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ['PNG','JPG','JPEG']
app.config["MAX_IMAGE_SIZE"] = 0.5 * 1024 * 1024 #In bytes

def allowed_image(filename) : 
    if not "." in filename :
        return False
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"] : 
        return True 
    else :
        return False
def allowed_image_filesize(filesize):
    if int(filesize) < app.config["MAX_IMAGE_SIZE"] : 
        return True
    else :
        return False


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        if request.files :
            if not allowed_image_filesize(request.cookies.get("filesize")):
                print("Size of image to big")
                return redirect(request.url)
            image = request.files['image']
            if image.filename == "":
                print("Image Must have a filename")
                return redirect(request.url)
            if not allowed_image(image.filename):
                print("Extension is not allowed")
                return redirect(request.url)
            else : 
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['IMAGE_UPLOADS'],filename))
                copyfile(os.path.join(app.config['IMAGE_UPLOADS'],filename),os.path.join(app.config['IMAGE_RESULTS'],filename)) #DELETE THIS LATER USELESS
                print("Image (",filename,") Saved")
                link = '/results/'+image.filename
                print("You'll be redirected to  ",link)
            return redirect(link)
    else :
        return render_template('index.html')

@app.route('/results/<filename>',methods=['POST','GET'])
def results(filename):
    input_file = filename
    cd = ColorDescriptor((8,12,3)) #Use same number of bins in the index.py

    #Load the given image and describe it
    query = cv2.imread(os.path.join(app.config['IMAGE_UPLOADS'],filename))
    features = cd.describe(query)

    #Search for similairs pictures using the searcher.py
    searcher = Searcher(os.path.join(app.config['IMAGE_INDEX'],"index.csv"))
    results = searcher.search(features)

    for (score,resultID) in results : 
    #Load the result image 
        print(resultID)


    return render_template('result.html',input_file=input_file)

if __name__ == "__main__":
    app.run(debug=True)
