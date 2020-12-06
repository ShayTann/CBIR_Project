from colordescriptor import ColorDescriptor
from searcher import Searcher
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--index",required = True , help="Path to where the computed index will be stored")
ap.add_argument("-q","--query",required = True , help="Path to the query image")
ap.add_argument("-r","--result-path",required = True , help="Path to the result path")

args = vars(ap.parse_args())

cd = ColorDescriptor((8,12,3)) #Use same number of bins in the index.py

#Load the given image and describe it
query = cv2.imread(args["query"])
features = cd.describe(query)

#Search for similairs pictures using the searcher.py
searcher = Searcher(args["index"])
results = searcher.search(features)

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