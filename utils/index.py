from colordescriptor import ColorDescriptor
from texturedescriptor import TextureDescriptor
from fourierdescriptor import ShapeDescriptor
import numpy as np
import argparse
import glob
import cv2

# Construct the argument parser and parse the arguments

#After when we gonna deploy this on our web app we gonna change these argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-d","--dataset",required = True, help = "dataset\data1")
ap.add_argument("-c","--color",required = True, help = "Path to save features from Color descriptor")
ap.add_argument("-t","--texture",required = True, help = "Path to save features from Texture descriptor")
ap.add_argument("-s","--shape",required = True, help = "Path to save features from Fourier descriptor")
args = vars(ap.parse_args())

# Initialize the color descriptor 

cd = ColorDescriptor((8,12,3))
td = TextureDescriptor()
sd = ShapeDescriptor()

output_color = open(args["color"],"w") #Output file for every descritpor
output_texture = open(args["texture"],"w")
output_shape = open(args["shape"],"w")


# We gonna use glob to loop over images : 
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    # First we need something to identify every picture , let's use the image Path 
    imageID = imagePath[imagePath.rfind("/") + 1 :]
    image = cv2.imread(imagePath)
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #No we gonna use our descriptor function to get the features :
    features_color = cd.describe(image)
    features_texture = td.lbp(image_grey)         #np.concatenate([features, td.lbp(image_grey)])
    features_shape = sd.extractFeatures(image_grey)  #np.concatenate([features, sd.extractFeatures(image_grey)])
    #Save our features into a file .
    #Every feature is 288 entries , with the 5 regions we gonna have 1440 dimensionality for each picture
    features_color = [str(f) for f in features_color] 
    features_texture = [str(f) for f in features_texture] 
    features_shape = [str(f) for f in features_shape] 
    output_color.write("%s,%s\n" %(imageID,",".join(features_color)))
    output_texture.write("%s,%s\n" %(imageID,",".join(features_texture)))
    output_shape.write("%s,%s\n" %(imageID,",".join(features_shape)))
    
output_color.close
output_texture.close
output_shape.close