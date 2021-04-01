import cv2
import numpy as np
import copy
from dome.detection import Detection

def find_agents(img):
    detected_agents=[]
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (5,5),3)
    circles = cv2.HoughCircles(grey,cv2.HOUGH_GRADIENT_ALT,2,20,
                                param1=100,param2=0.1,minRadius=0,maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x,y,radius) in circles[:,0]:
            detected_agents.append(Detection(x,y,radius,1,0))
    return np.array(detected_agents)


def match_detections(past_detections, current_detections):
    #to match agents in the current frame to the correct ID based on position
    matched_detections = copy.deepcopy(past_detections)
    #set propagating agents to 1
    #caculate length of deactivity, becomes increasingly negative the more frames are dropped
    #note that if the countour is matched in the subsequent section, is will reset to zero
    for d in matched_detections:
        d.update_deactivity()
        #set current activity to deactive for all agents
        d.reset_deactivity()

    for current_detection in current_detections:
        position_difference_match = 10000
        detection_id = 0
        # Try to match with any of the past detections
        for past_detection in past_detections:
            #excludes long term deactivated agents
            if past_detection.is_active():
                position_difference= current_detection.distance(past_detection)
                if position_difference < position_difference_match:
                    matched_detection_id = detection_id
                    position_difference_match=position_difference  
            else:
                pass
            detection_id+=1
            
        #if the agent falls outside of a given confidence inteval, assume new agents and append to the end of the array 
        if position_difference_match > 35:
            matched_detections.append(current_detection)
        else:
            matched_detections[matched_detection_id]=current_detection # update the detection

    #carry over propogation number
    return matched_detections