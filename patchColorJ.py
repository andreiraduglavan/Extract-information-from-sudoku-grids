#This file implements the code for getting the zones out of the colored jigsaw grids


import cv2 as cv
import numpy as np

class patch_colorJ:
    def __init__(self, color):
        self.color=color
        self.zone=None
        self.down=None
        self.left=None
        self.right=None
        self.up=None

def get_zones_colorJ(self, zone):
    #this function allocs recursively a zone to un unzoned patch

    if self.zone is None:
        self.zone=zone
        if self.left is not None:
            if self.color==self.left.color:
                get_zones_colorJ(self.left, zone)
        if self.down is not None:
            if self.color==self.down.color:
                get_zones_colorJ(self.down, zone)
        if self.right is not None:
            if self.color==self.right.color:
                get_zones_colorJ(self.right, zone)
        if self.up is not None:
            if self.color==self.up.color:
                get_zones_colorJ(self.up, zone)

def get_zones_pattern_colorJ(patches):
    #this function returns the zones of the sudoku grid

    colors=[[203, 181, 146],[146, 182, 178],[155, 161, 188]]
    mat=[]
    l=[]

    #store the zones grid pattern in a matrix
    for i in range(len(patches)):
        median=cv.medianBlur(patches[i], 21)
        color=median[27][27]
        distances=[]
        for c in colors:
            distances.append(np.linalg.norm(color-c))
        color_index=np.argmin(distances)
        if color_index==0:
            l.append(patch_colorJ("blue"))
        if color_index==1:
            l.append(patch_colorJ("yellow"))
        if color_index==2:
            l.append(patch_colorJ("red"))
        if i%9==8:
            mat.append(l)
            l=[]

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

    #get the zones with get_zones_colorJ function
    zone_counter=1
    for i in range(9):
        for j in range(9):
            if mat[i][j].zone is None:
                get_zones_colorJ(mat[i][j],zone_counter)
                zone_counter+=1
            
    zones=[]
    for i in range(81):
        zones.append(mat[i//9][i%9].zone)

    return zones