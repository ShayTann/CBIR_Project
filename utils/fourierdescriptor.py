import cv2
import numpy as np



class ShapeDescriptor:
    def invertBinaryImage(self,binary_image):
        return cv2.bitwise_not(binary_image)

    def findOutline(self,image, find_thresh=True):
        # when find thresh is set to FALSE, then the image is the threshold image and we just set thresh_image to image
        if find_thresh:
            _, thresh_image = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Look for threshold  
        else:
            thresh_image = image.copy()

        img_floodfill = thresh_image.copy() #Create a copy
        h, w = thresh_image.shape[:2]  #Get the height and weight

        contour, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #We're looking for shapes

        contour = max(contour, key=cv2.contourArea)

        return contour

    def convert1D(self,contour, no_samples, contour_centroids=None):
        # we use the centroid distance shape signature

        if contour_centroids is None:
            contour_centroids = np.squeeze(contour.mean(axis=0))

        # we first sample to the number of points we want
        sample_points = np.squeeze(cv2.ximgproc.contourSampling(contour, no_samples))

        # invariant to translation
        return np.sqrt(np.sum((sample_points - contour_centroids) ** 2, axis=1))

    def normalise(self,magnitudes):
        #Normalization and flatten

        half_samples = (len(magnitudes) // 2) + 1

        return (magnitudes[1:half_samples] / magnitudes[0]).flatten()

    # we extract the given images using the fourier extractor
    def fourierDescriptor(self,contour, contour_centroids=None, no_samples=64):

        # convert contour 2d co-ordinates to 1d co-ordinates
        contour1d = self.convert1D(contour, contour_centroids=contour_centroids, no_samples=no_samples)

        # contour1d represents the points after they have been sampled and they have been reduced
        # using a certain shape signature

        fourier_transform = cv2.dft(contour1d, flags=cv2.DFT_COMPLEX_OUTPUT)
        magnitudes = cv2.magnitude(fourier_transform[:, :, 0], fourier_transform[:, :, 1])

        return self.normalise(magnitudes)

    def extractFeatures(self,image, find_thresh=True): #Main function that compute our fourier descriptor

        contour = self.findOutline(image, find_thresh=find_thresh)

        return self.fourierDescriptor(contour)