import cv2 as cv
import numpy as np
import os
from patchColorJ import *
from patchJ import *
from patchJ import get_zones_pattern_J

def show_image(image):
    cv.imshow("", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def preprocess_image(image):
    #this function returns a preprocessed image with the sudoku grid

    gray = cv.cvtColor(image.copy(),cv.COLOR_BGR2GRAY)
    image_m_blur = cv.medianBlur(gray, 3)
    image_g_blur = cv.GaussianBlur(image_m_blur, (0, 0), 5)
    image_sharpened = cv.addWeighted(image_m_blur, 1.2, image_g_blur, -0.8, 0)
    _, thresh = cv.threshold(image_sharpened, 20, 255, cv.THRESH_BINARY)

    
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv.erode(thresh, kernel)
    
    #_, thresh = cv.threshold(normalized, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

    edgels =  cv.Canny(thresh ,150,400)
    contours, _ = cv.findContours(edgels,  cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0
   
    for i in range(len(contours)):
        if(len(contours[i]) >3):
            possible_top_left = None
            possible_bottom_right = None
            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point

                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + possible_bottom_right[1] :
                    possible_bottom_right = point

            diff = np.diff(contours[i].squeeze(), axis = 1)
            possible_top_right = contours[i].squeeze()[np.argmin(diff)]
            possible_bottom_left = contours[i].squeeze()[np.argmax(diff)]
    
            
            if cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left

    #image_contour=image.copy()
    #cv.drawContours(image_contour, contours, -1, (0,255,0), 3)
    #show_image(image_contour)
    
    #first rotation
    radians=np.arctan((top_right[1]-top_left[1])/(top_right[0]-top_left[0]))
    angle=np.degrees(radians)
    
    height, width, _ = np.shape(image)
    center=(width//2, height//2)
    
    transformationMatrix=cv.getRotationMatrix2D(center, angle, 1)
    croped_image=cv.warpAffine(image, transformationMatrix, (width, height))
    
    top_left=np.int0(transformationMatrix[:,:2]@top_left+transformationMatrix[:,2])
    top_right=np.int0(transformationMatrix[:,:2]@top_right+transformationMatrix[:,2])
    bottom_right=np.int0(transformationMatrix[:,:2]@bottom_right+transformationMatrix[:,2])
    bottom_left=np.int0(transformationMatrix[:,:2]@bottom_left+transformationMatrix[:,2])

    #second rotation
    radians=np.arctan((bottom_right[1]-bottom_left[1])/(bottom_right[0]-bottom_left[0]))
    angle=np.degrees(radians)
    
    height, width, _ = np.shape(croped_image)
    center=(width//2, height//2)
    
    transformationMatrix=cv.getRotationMatrix2D(center, angle, 1)
    croped_image=cv.warpAffine(croped_image, transformationMatrix, (width, height))

    top_left=np.int0(transformationMatrix[:,:2]@top_left+transformationMatrix[:,2])
    top_right=np.int0(transformationMatrix[:,:2]@top_right+transformationMatrix[:,2])
    bottom_right=np.int0(transformationMatrix[:,:2]@bottom_right+transformationMatrix[:,2])
    bottom_left=np.int0(transformationMatrix[:,:2]@bottom_left+transformationMatrix[:,2])
    croped_image=croped_image[top_left[1]:bottom_left[1],top_left[0]:top_right[0]]

    croped_image=cv.resize(croped_image, (495, 495))
    return croped_image

if __name__=="__main__":
    dir="antrenare/clasic/"
    for i in range(6,7):
        if i<10:
            filename="0"+str(i)+".jpg"
        else:
            filename=str(i)+".jpg"
        image = cv.imread(dir+filename)
        image = cv.resize(image,(0,0),fx=0.2,fy=0.2)
        image=preprocess_image(image)
        #show_image(image)

def getLines():
    lines_vertical=[]
    for i in range(0,496,55):
        l=[]
        l.append((i,0))
        l.append((i,494))
        lines_vertical.append(l)

    lines_horizontal=[]
    for i in range(0,496,55):
        l=[]
        l.append((0,i))
        l.append((494,i))
        lines_horizontal.append(l)
    return lines_vertical, lines_horizontal

def get_patches(img):
    #this function receive an image with the sudoku grid and returns an array with 81(9x9) patches
    patches=[]
    lines_vertical, lines_horizontal=getLines()
    for i in range(len(lines_horizontal)-1):
        for j in range(len(lines_vertical)-1):
            y_min = lines_vertical[j][0][0]
            y_max = lines_vertical[j + 1][1][0]
            x_min = lines_horizontal[i][0][1]
            x_max = lines_horizontal[i + 1][1][1]
            patch = img[x_min:x_max, y_min:y_max].copy()
            patches.append(patch)
            #show_image("patch", patch)
            #cv.imwrite("!!poza "+filename+" patch "+str(i*9+j)+".jpg", patch)
    return patches

def remove_all(list, element):
    while True:
        if (element in list):
            list.remove(element)
        else:
            break

def predict_digit_PM(image,color,type):
    gray= cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    h,w=np.shape(thresh)
    logits=np.zeros(9)
    for j in range(1,44):
        if type=='clasic':
            dir="masks/clasic/set"+str(j)+"/"
        if type=='jigsaw' and color==False:
            dir="masks/jigsawbw/set"+str(j)+"/"
        if type=='jigsaw' and color:
            dir="masks/jigsawcolor/set"+str(j)+"/"
        masks=[]
        for i in range(1,10):
            mask=cv.imread(dir+str(i)+".jpg")
            gray_mask= cv.cvtColor(mask,cv.COLOR_BGR2GRAY)
            gray_mask=cv.resize(gray_mask, (w,h))
            _, thresh_mask = cv.threshold(gray_mask, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
            masks.append(gray_mask)
        values=[]
        for mask in masks:
            values.append(np.abs(cv.matchTemplate(gray, mask, cv.TM_CCOEFF_NORMED)[0][0]))
        logits[np.argmax(values)]+=1
    return np.argmax(logits)+1


def get_results(patches, color=False, type='clasic'):
    if type=='clasic':
        wmin=5
        wmax=30
        hmin=5
        hmax=35
    elif type=='jigsaw' and color:
        wmin=5
        wmax=30
        hmin=5
        hmax=35
    else:
        wmin=4
        wmax=30
        hmin=9
        hmax=35
    
    result=""
    result_bonus=""
    for i in range(len(patches)):
        if i%9==0 and i!=0:
            result+="\n"
            result_bonus+="\n"
        patch=patches[i]
        gray= cv.cvtColor(patch.copy(),cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        thresh[0:10,:]=0
        thresh[46:56,:]=0
        thresh[:, 0:10]=0
        thresh[:,46:56]=0
        contours, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        imcnts=patch.copy()
        check=False
        for c in contours:
            x,y, w,h=cv.boundingRect(c)
            if (w>wmin and w<wmax) and (h>hmin and h<hmax):
                cdigit=c
                check=True
        
        if check:
            x,y, w,h=cv.boundingRect(cdigit)
            crop=imcnts[y:y+h,x:x+w,:]
            digit=predict_digit_PM(crop, color, type)
            result+="x"
            result_bonus+=str(digit)
        else:
            result+="o"
            result_bonus+="o"
    return result, result_bonus

def get_results_J(preprocessed_image, color=False, type='clasic'):
    
    if color:
        patches=get_patches(preprocessed_image)
        zones=get_zones_pattern_colorJ(patches)
    else:
        gray=cv.cvtColor(preprocessed_image.copy(), cv.COLOR_BGR2GRAY)
        median=cv.medianBlur(gray, 7)
        _, thresh = cv.threshold(median, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        patches=get_patches(thresh)
        zones, _=get_zones_pattern_J(patches)
        patches=get_patches(preprocessed_image)
    
    result, result_bonus=get_results(patches, color=color, type=type)
    result=list(result)
    remove_all(result, "\n")
    result_bonus=list(result_bonus)
    remove_all(result_bonus, "\n")
    
    result_with_zones=""
    bonus_result_with_zones=""
    for i in range(81):
        result_with_zones+=str(zones[i])
        result_with_zones+=result[i]
        bonus_result_with_zones+=str(zones[i])
        bonus_result_with_zones+=result_bonus[i]
        if i%9==8 and i!=0 and i!=80:
            result_with_zones+="\n"
            bonus_result_with_zones+="\n"
    
    return result_with_zones, bonus_result_with_zones

def get_grid_color(image):
    #funtion used to check wether a sudoku grid is colored or not

    gray=cv.cvtColor(image.copy(), cv.COLOR_BGR2GRAY)
    mat=[]
    for i in range(np.shape(gray)[0]):
        l=[]
        for j in range(np.shape(gray)[1]):
            p=gray[i,j]
            l.append([p,p,p])
        mat.append(l)
    mat0=np.zeros(image.shape)
    if sum(sum(sum(np.abs(mat0-mat+image))))>2000000:
        color=True
    else:
        color=False
    return color

#the following 2 functions were used to extract the masks digits and its labels

def get_train_images(patches, mat, counter, color):
    result=""
    result_bonus=""
    for i in range(len(patches)):
        if i%9==0 and i!=0:
            result+="\n"
            result_bonus+="\n"
        patch=patches[i]
        gray= cv.cvtColor(patch.copy(),cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        thresh[0:10,:]=0
        thresh[46:56,:]=0
        thresh[:, 0:10]=0
        thresh[:,46:56]=0
        contours, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        imcnts=patch.copy()
        check=False
        for c in contours:
            x,y, w,h=cv.boundingRect(c)
            if (w>5 and w<30) and (h>5 and h<40):
                cdigit=c
                check=True
        if check:
            x,y, w,h=cv.boundingRect(cdigit)
            crop=imcnts[y:y+h,x:x+w,:]
            #digit=predict_digit(crop)
            result+="x"
            result_bonus+=str(0)
            true_value=mat[i//9][i%9]
            if color:
                counter[0][true_value-1]+=1
                dir="masks/jigsawcolor/set"+str(int(counter[0][true_value-1]))+"/"
            else:
                counter[1][true_value-1]+=1
                dir="masks/clasic/set"+str(int(counter[1][true_value-1]))+"/"
            try:
                os.mkdir(dir)
            except FileExistsError:
                pass
            if true_value!=0:
                cv.imwrite(dir+str(true_value)+".jpg", crop)
        else:
            result+="o"
            result_bonus+="o"
    return result, result_bonus, counter

def get_masks_folder():  
    dir="traininig/clasic/"
    counter=np.zeros((2,9))
    for i in range(1,41):
        print(i)
        if i<10:
            filename="0"+str(i)+".jpg"
            textfilename="0"+str(i)+"_bonus_gt"+".txt"
        else:
            filename=str(i)+".jpg"
            textfilename=str(i)+"_bonus_gt"+".txt"
        image = cv.imread(dir+filename)
        image = cv.resize(image,(0,0),fx=0.2,fy=0.2)
        image=preprocess_image(image)
        color=get_grid_color(image)
        patches=get_patches(image)
        f=open(dir+textfilename)
        elements=list(f.read())
        f.close()
        remove_all(elements, '\n')
        mat=[]
        l=[]
        for i in range(len(elements)):
            try:
                l.append(int(elements[i]))
            except:
                l.append(0)
            if len(l)==9:
                mat.append(l)
                l=[]
        mat.append(l)
        l=[]
        _, _, counter=get_train_images(patches, mat, counter, color)