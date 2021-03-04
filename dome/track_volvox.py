import cv2
import numpy as np

def find_agents(img):
    contoursFiltered=[]
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (5,5),3)
    circles = cv2.HoughCircles(grey,cv2.HOUGH_GRADIENT_ALT,2,20,
                                param1=100,param2=0.1,minRadius=0,maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x,y,radius) in circles[:,0]:
            contoursFiltered.append([x,y,radius,radius,1,0])
    contoursFiltered=np.array(contoursFiltered)
    return contoursFiltered
