import glob
import os
from shutil import copy
import datetime

dir_src = r"F:\\MASTER MBD S3\\Analysis Mining and indexing in big multimedia system\\Mini-projet\\Mini-proj1\\dataset\\101_ObjectCategories\\101_ObjectCategories"
dir_dst = r"F:\\MASTER MBD S3\\Analysis Mining and indexing in big multimedia system\\Mini-projet\\Mini-proj1\\dataset\\data1"



for root, _, files in os.walk(dir_src):
    for file in files:
        if file.endswith('.jpg'):
            base, extension = os.path.splitext(file)
            new_name = os.path.join(dir_dst, file)
            if not os.path.exists(new_name):
                copy(os.path.join(root, file), new_name)
            else :
                print("Already Exist , creating a new name")
                ii = 1
                while True :
                    new_name = os.path.join(dir_dst,base + "_" + str(ii) + extension)
                    if not os.path.exists(new_name):
                        print("Trying to copy")
                        copy(os.path.join(root, file), new_name)
                        print("Coppied")
                        break
                    ii += 1

            