import numpy as np 
import csv 

class Searcher :
    def __init__(self,indexPath_color,indexPath_texture,indexPath_shape): # Paths for descriptors
        self.indexPath_color = indexPath_color
        self.indexPath_texture = indexPath_texture
        self.indexPath_shape = indexPath_shape
    # **Main function of our PROJECT**
    #Here we need to have the query (input) features of every descriptor, then the descriptors to use and the weights, limits for the number of results
    def search(self,queryFeatures_color,queryFeatures_texture,queryFeatures_shape,limit=10,descriptors=['Color','Texture','Shape'],w=[1/3,1/3,1/3]): 
        results = {} # Initialize the output dictionary
        with open(self.indexPath_color) as  f1,open(self.indexPath_texture) as  f2,open(self.indexPath_shape) as  f3 :
            reader_color = csv.reader(f1) # Read the csv File
            reader_texture = csv.reader(f2)
            reader_shape = csv.reader(f3)

            for (row_color,row_texture,row_shape) in zip(reader_color,reader_texture,reader_shape): # Loop over rows
                d_t = 0 #We gonna store the results of distance between input and our datasets respect the weights
                # We're using the same function of similarity for every descriptor
                for descriptor in descriptors : #Loop over descriptors to compute the distance
                    if descriptor == 'Color':
                        features_color = [float(x) for x in row_color[1:]]
                        d_color = self.chi2_distance(features_color,queryFeatures_color) 
                        d_t += d_color * w[0]
                    if descriptor == 'Texture':
                        features_texture = [float(x) for x in row_texture[1:]]
                        d_texture = self.chi2_distance(features_texture,queryFeatures_texture)
                        d_t += d_texture * w[1]
                    if descriptor == 'Shape':
                        features_shape = [float(x) for x in row_shape[1:]]
                        d_shape = self.chi2_distance(features_shape,queryFeatures_shape)
                        d_t += d_shape * w[2]
                results[row_color[0]] = d_t  #Here row_color can be changed by texture or just the id of current picture
        f1.close()
        f2.close()
        f3.close()
        # Now we need to sort our list of results ( the low values are the most similar pictures)
        results = sorted([(v,k) for (k,v) in results.items()])
        return results[:limit] #Here we return only one result with the lowest value , we will change that later in our web app
    
    def chi2_distance(self,histA,histB,eps=1e-10):
        d = 0.5 * np.sum([((a-b)**2)/(a+b+eps) for (a,b) in zip(histA,histB)]) #Compute the chi-squared distance
        return d
