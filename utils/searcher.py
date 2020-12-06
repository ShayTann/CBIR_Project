import numpy as np 
import csv 

class Searcher :
    def __init__(self,indexPath): # We store our index Path
        self.indexPath = indexPath
    # **Main function of our PROJECT**
    def search(self,queryFeatures,limit=10): 
        results = {} # Initialize the output dictionary
        with open(self.indexPath) as  f :
            reader = csv.reader(f) # Read the csv File
            for row in reader : # Loop over rows
                features = [float(x) for x in row[1:]] 
                # Here for each row we gonna extract the features associated with the indexed image and then
                # Compare them with the given image using the chi2_distance
                d = self.chi2_distance(features,queryFeatures)
                # Now after computing the distance of the current feature in X image with our given image we need to save that in our dictionary
                # The key here is the current image id and the value is the distance (How similar the images)
                results[row[0]] = d 
            f.close()
        # Now we need to sort our list of results ( the low values are the most similar pictures)
        results = sorted([(v,k) for (k,v) in results.items()])
        return results[:limit] #Here we return only one result with the lowest value , we will change that later in our web app
    def chi2_distance(self,histA,histB,eps=1e-10):
        d = 0.5 * np.sum([((a-b)**2)/(a+b+eps) for (a,b) in zip(histA,histB)]) #Compute the chi-squared distance
        return d