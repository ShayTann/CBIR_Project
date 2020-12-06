from flask import Flask , render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


app.config['IMAGE_UPLOADS'] = "F://MASTER MBD S3//Analysis Mining and indexing in big multimedia system//Mini-projet//Mini-proj1//Search Engine//static//img//uploads"
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
    print(filesize)
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
                print("Image (",filename,") Saved")
            return redirect(request.url)
    else :
        return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
