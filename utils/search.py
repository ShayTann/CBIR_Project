from colordescriptor import ColorDescriptor
from texturedescriptor import TextureDescriptor
from fourierdescriptor import ShapeDescriptor
from searcher import Searcher
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-c","--color",required = True , help="Path to where the computed index will be stored")
ap.add_argument("-t","--texture",required = True , help="Path to where the computed index will be stored")
ap.add_argument("-s","--shape",required = True , help="Path to where the computed index will be stored")
ap.add_argument("-q","--query",required = True , help="Path to the query image")
ap.add_argument("-r","--result-path",required = True , help="Path to the result path")

args = vars(ap.parse_args())

cd = ColorDescriptor((8,12,3)) #Use same number of bins in the index.py
td = TextureDescriptor()
sd = ShapeDescriptor()

#Load the given image and describe it
query = cv2.imread(args["query"])
query_grey = cv2.cvtColor(query, cv2.COLOR_BGR2GRAY)
features_color = cd.describe(query)
feature_texture = td.lbp(query_grey)
feature_shape = sd.extractFeatures(query_grey)
#features = np.concatenate([features, td.lbp(image_gry)])
#features = np.concatenate([features, sd.extractFeatures(image_gry)])

#Search for similairs pictures using the searcher.py
searcher = Searcher(args["color"],args["texture"],args["shape"])
results = searcher.search(features_color,feature_texture,feature_shape)

#Display the given image : 
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 500, 500)
cv2.imshow("image",query)

for (score,resultID) in results : 
    #Load the result image 
    print(resultID)
    result = cv2.imread(args["result_path"]+"/"+resultID)
    cv2.imshow("image",result)
    cv2.waitKey(0)