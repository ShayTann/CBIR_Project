from colordescriptor import ColorDescriptor
import argparse
import glob
import cv2

# Construct the argument parser and parse the arguments

#After when we gonna deploy this on our web app we gonna change these argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-d","--dataset",required = True, help = "dataset\data1")
ap.add_argument("-i","--index",required = True, help = "Search Engine\indexes")
args = vars(ap.parse_args())

# Initialize the color descriptor 

cd = ColorDescriptor((8,12,3))

output = open(args["index"],"w") #Output file

# We gonna use glob to loop over images : 
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    # First we need something to identify every picture , let's use the image Path 
    imageID = imagePath[imagePath.rfind("/") + 1 :]
    image = cv2.imread(imagePath)
    #No we gonna use our descriptor function to get the features :
    features = cd.describe(image)
    #Save our features into a file .
    #Every feature is 288 entries , with the 5 regions we gonna have 1440 dimensionality for each picture
    features = [str(f) for f in features] 
    output.write("%s,%s\n" %(imageID,",".join(features)))
    
output.close