import numpy as np 
import cv2 

class ColorDescriptor :
    def __init__(self,bins):
        self.bins = bins 
    def describe(self,image) :
        image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) # Convert the image given to HSV color space
        features = [] # Initialize the list of features
        (h,w) = image.shape[:2] # Grab dimensions of the picture
        (cX,cY) = (int(w*0.5),int(h*0.5)) # Compute the center of the image
        # Regions-based :
        segments = [(0,cX,0,cY),(cX,w,0,cY),(cX,w,cY,h),(0,cX,cY,h)] #Top-left ,Top-right , bottom-right , bottom-left
        # We'll need to construct a elliptical mask to represent the center of the image .
        # We'll do this by defining an ellipse radius that is 75% of the width and height of the image :
        (axesX,axesY) = (int(w*0.7)// 2, int(h*0.75)// 2)
        ellipMask = np.zeros(image.shape[:2],dtype="uint8")
        cv2.ellipse(ellipMask,(cX,cY),(axesX,axesY),0,0,360,255,-1) # Used to draw a actual ellipse in the image .
        # The last parameters are : 
        # 0 : Rotation of the ellipse  , 0 : The starting angle of the ellipse , 360 : The ending angle of the ellipse , 255 : The color of the ellipse we use white , -1 the border size
        
        # Now for every segments of the image we gonna construct a mask and substract the center eliptical mask from it :
        for (startX,endX,startY,endY) in segments :
            cornerMask = np.zeros(image.shape[:2],dtype="uint8")
            cv2.rectangle(cornerMask,(startX,startY),(endX,endY),255,-1)
            cornerMask = cv2.subtract(cornerMask,ellipMask)
            # Now for every segment we gonna extract the color histogram and update our list of features :
            hist = self.histogram(image,cornerMask)
            features.extend(hist) # Here we add the list of hist in our features list
        # Finally there still one region we didnt extract the color histogram and it is the elliptical region : 
        hist = self.histogram(image,ellipMask)
        features.extend(hist)
        return features # A list of 5 lists contains features for every segments and the center.
    def histogram(self,image,mask) :
        #This function is used to extract the 3D color Histogram from the masked region of the image 
        hist = cv2.calcHist([image],[0,1,2],mask,self.bins,[0,180,0,256,0,256])
        #Normalize the histogram :  
        # It is very important that you normalize your color histograms so each histogram is represented by the relative 
        # percentage counts for a particular bin and not the integer counts for each bin.
        hist = cv2.normalize(hist,hist).flatten()
        return hist