#This file implements the code for getting the zones out of the gray jigsaw grids


import cv2 as cv
import numpy as np


class patch_J():
    def __init__(self, patch):
        self.patch=np.array(patch)
        self.zone=None
        self.down=None
        self.left=None
        self.right=None
        self.up=None
        self.downWall=False
        self.leftWall=False
        self.rightWall=False
        self.upWall=False

def get_zones(self, zone):
    #this function allocs recursively a zone to un unzoned patch

    if self.zone is None:
        self.zone=zone
        if self.left is not None:
            if not self.leftWall:
                get_zones(self.left, zone)
        if self.right is not None:
            if not self.rightWall:
                get_zones(self.right, zone)
        if self.up is not None: 
            if not self.upWall:
                get_zones(self.up, zone)
        if self.down is not None: 
            if not self.downWall:
                get_zones(self.down, zone)

def get_walls(self):
    #function to detect the walls of a patch

    wall=np.ones((55,7))*255
    verticalWall=np.ones((55,9))*255
    if (sum(self.patch[:,0:9]==verticalWall)>27).any():
        self.leftWall=True
    if (sum(self.patch[:,-8:-1]==wall)>27).any():
        self.rightWall=True
    if (sum(self.patch[-10:-1, :].T==verticalWall)>27).any():
        self.downWall=True
    if (sum(self.patch[0:7, :].T==wall)>27).any():
        self.upWall=True

def get_zones_pattern_J(patches):
    #this function returns the zones of the sudoku grid

    mat=[]

    #store the zones grid pattern in a matrix
    for i in range(81):
        if i%9==0:
            l=[]
        l.append(patch_J(patches[i]))
        if i%9==8:
            mat.append(l)

    #get the neighbors of every patch
    for i in range(9):
            for j in range(9):
                if i<8:
                    mat[i][j].down=mat[i+1][j]
                if j<8:
                    mat[i][j].right=mat[i][j+1]
                if j>0:
                    mat[i][j].left=mat[i][j-1]
                if i>0:
                    mat[i][j].up=mat[i-1][j]
                get_walls(mat[i][j])

    #if one patch gas a wall than it's neighbor must have as well
    for i in range(9):
            for j in range(9):
                if i<8 and mat[i][j].downWall:
                    mat[i+1][j].upWall=True
                if j<8 and mat[i][j].rightWall:
                    mat[i][j+1].leftWall=True
                if j>0 and mat[i][j].leftWall:
                    mat[i][j-1].rightWall=True
                if i>0 and mat[i][j].upWall:
                    mat[i-1][j].downWall=True

     #get the zones with get_zones function
    zone_counter=1
    for i in range(9):
        for j in range(9):
            if mat[i][j].zone is None:
                get_zones(mat[i][j],zone_counter)
                zone_counter+=1

    zones=[]
    for i in range(81):
        zones.append(mat[i//9][i%9].zone)
    
    return zones, mat

if __name__ == "__main__":
    #use for debugging purposes
    import sys
    from utils import preprocess_image
    from utils import get_patches
    from utils import show_image
    #np.set_printoptions(threshold=sys.maxsize)

    dir="training/jigsaw/"
    for i in range(16,17):
        print("!!", i)
        if i<10:
            filename=f"0{str(i)}.jpg"
        else:
            filename=f"{str(i)}.jpg"
        image = cv.imread(dir+filename)
        image = cv.resize(image,(0,0),fx=0.2,fy=0.2)
        image=preprocess_image(image)
        
        gray=cv.cvtColor(image.copy(), cv.COLOR_BGR2GRAY)
        median=cv.medianBlur(gray, 7)
        _, thresh = cv.threshold(median, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        patches=get_patches(thresh)
        zones, mat=get_zones_pattern_J(patches)
        i,j=(8,1)
        show_image(patches[i*9+j])
        print(patches[i*9+j][:,0:10])
        print(mat[i][j].downWall, mat[i][j].rightWall)
        zones_pat=""
        for i in range(81):
            if i%9==0 and i!=0:
                zones_pat+="\n"
            zones_pat+=str(zones[i])

        print(zones_pat)
        #show_image(image)
