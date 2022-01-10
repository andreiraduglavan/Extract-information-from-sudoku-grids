import cv2 as cv
import numpy as np
from utils import *
from tqdm import trange

#Get results for classic grids
dir="training/clasic/"
for i in trange(1,21):
    if i<10:
        filename="0"+str(i)+".jpg"
    else:
        filename=str(i)+".jpg"
    try:
        image = cv.imread(dir+filename)
        image = cv.resize(image,(0,0),fx=0.2,fy=0.2)
        image=preprocess_image(image)
        patches=get_patches(image)
        result, result_bonus=get_results(patches)
        f=open("results/clasic/"+str(i)+"_predicted"+".txt", "w")
        f.write(result)
        f.close()
        f=open("results/clasic/"+str(i)+"_bonus_predicted"+".txt", "w")
        f.write(result_bonus)
        f.close()
    except:
        print("error on photo ", str(i))
        f=open("results/clasic/"+str(i)+"_predicted"+".txt", "w")
        f.write("error")
        f.close()
        f=open("results/clasic/"+str(i)+"_bonus_predicted"+".txt", "w")
        f.write("error")
        f.close()


#Get results for jigsaw grids
dir="training/jigsaw/"
for i in trange(1,41):
    if i<10:
        filename="0"+str(i)+".jpg"
    else:
        filename=str(i)+".jpg"
    try:
        image = cv.imread(dir+filename)
        image = cv.resize(image,(0,0),fx=0.2,fy=0.2)
        image=preprocess_image(image)
        color=get_grid_color(image)
        result, result_bonus=get_results_J(image, color, type='jigsaw')
        f=open("results/jigsaw/"+str(i)+"_predicted"+".txt", "w")
        f.write(result)
        f.close()
        f=open("results/jigsaw/"+str(i)+"_bonus_predicted"+".txt", "w")
        f.write(result_bonus)
        f.close()
    except:
        print("error on photo ", str(i))
        f=open(str(i)+"_predicted"+".txt", "w")
        f.write("error")
        f.close()
        f=open(str(i)+"_bonus_predicted"+".txt", "w")
        f.write("error")
        f.close()