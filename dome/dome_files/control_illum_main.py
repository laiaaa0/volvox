import cv2 
# from picamera.array import PiRGBArray
# from picamera import PiCamera
# import RPi.GPIO as GPIO
import csv
import socket
import time
import numpy as np
import json
import pandas
import math
import glob
import random

#read camera-projector space calibration file
file = "dome/dome_files/matrix_parameters.txt"
with open(file) as f:
    csvreader = csv.reader(f, delimiter = ',', quotechar=None)
    for row in csvreader:
        dx_cam = float(row[0]) 
        dy_cam = float(row[1])
        theta = float(row[2])
        stretch_x = float(row[3])
        stretch_y = float(row[4])
        dx_proj = float(row[5])
        dy_proj = float(row[6]) 


#parameters for duration and relaxation period of light flashing
def update_global_light_params():
    light_duration_init=1
    light_relaxation_init=10
    return (light_duration_init,light_relaxation_init)

#send data to networked socket
def transmit(transmitMessage):
    msg = json.dumps(transmitMessage)
    #print(msg)
    clientsocket.send(bytes(msg, "utf-8"))

#send data to networked socket
def recieve():
    data = clientsocket.recv(10000)
    #provide an exception for when no data is received to avoid json expected value error
    if not data:
        byteDecode = "NONE"
    #otherwise load seralised data using json
    else:
        byteDecode = json.loads(data)
    return(byteDecode)


def centerPoint():
    with open("/home/pi/Documents/9xMag/Calibration/CentralPixel_file_.txt") as f:
        csvreader = csv.reader(f, delimiter = ',', quotechar = None)
        for row in csvreader:
            centerRow = int(row[0])
            centerColumn = int(row[1])
            centerRowLength= int(row[2])
            centerColumnlength = int(row[3])
    centerPoint=(centerRow, centerColumn, centerRowLength, centerColumnlength)
    return centerPoint            

def translate(rect, dx, dy):
    r2 = rect.copy()
    r2[0, :] = rect[0, :] + dx
    r2[1, :] = rect[1, :] + dy
    return r2

#transform camera coordinates into projector space 
def coordinateTransform(coordinate):
    cameraCoordinate = np.reshape(coordinate, (2,1))
    rotation_matrix = np.array([
        [np.cos(theta), np.sin(theta)],
        [-np.sin(theta),  np.cos(theta)]
    ])

    stretch_matrix = np.array([
        [(stretch_x), 0],
        [0, (stretch_y)]
    ])
    translated = translate(cameraCoordinate, -dx_cam, -dy_cam)
    rotated = np.matmul(rotation_matrix, translated)
    stretched = np.matmul(stretch_matrix, rotated)
    translatedFinal = translate(stretched, dx_proj, dy_proj)
    translatedCoordinate= [translatedFinal[0][0],translatedFinal[1][0]] 
    return translatedCoordinate

#identify agents in camera images
def image_analysis(img):
    contoursFiltered=[]
    #b,g,r = cv2.split(img)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh2 = cv2.threshold(grey,10,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour,True)
        if area > 50:
            compactness=(4*np.pi*area)/(perimeter**2)
            if compactness > 0.5:
                (x,y,w,h) = cv2.boundingRect(contour)
                contoursFiltered.append([x+int(w/2),y+int(h/2),w,h,1,0])
    #cv2.imshow("Threshold", thresh2)
    contoursFiltered=np.array(contoursFiltered)
    return contoursFiltered
    


def agent_location(centerPoint):
    #decides which agents are active in current frame
    counter = 0
    #empty list to store projection pixels
    projectionList=[]
    seed = False
    agent_list=[]
    for frame in glob.glob("C:/Users/Rize Kamishiro/Scripts/Control/012" +  '/*.png'):
    #for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
        img = cv2.imread(frame)
        #get image contours
        img_agents = image_analysis(img)
        #check if any agents are in FOV
        if len(img_agents) == 0:
            print("NO AGENTS DETECTED. PROGRAM TERMINATED")
            write_to_file(agent_list)
            exit()
        # for first instance of loop, initialise time zero
        if counter == 0:
            time_zero = time.time()
            for i in range(len(img_agents)):
                agent_list.append([])
        # for all other loop instances, match agents and calculate velocity or displacement
        else:
            time_difference = (time.time()-time_zero)*1000
            img_agents = agentMatching(past_agents, img_agents)
            agent_list = velocity_calculation(agent_list, past_agents, img_agents, time_difference, counter)
        agent_id = 0
        control_agents = []
        #check if agents are active, both in the individual frame and in longer term tracking
        if counter != 0:
            for agent in img_agents:
                if len(agent_list[agent_id])>0: #check we have at least 1 previous entry
                    for data_point in agent_list[agent_id]:#find counter location in data point
                        if data_point[2] == counter:
                            agent_params = data_point
                            break
                    else:
                        pass
                    #print(agent_params)
                    #print(agent)
                    active_status = agent[4]
                    long_term_status =agent[5]
                    light_duration = agent_params[3]
                    light_relaxation = agent_params[4]
                    timer = agent_params[5]
                    if long_term_status > -3:
                        #print("AGENT:", agent_id)
                        #print(light_duration, light_relaxation, timer)
                        if timer < (light_duration):
                            control_agents.append(agent)
                        if timer == int(light_duration): #check if light duration time frame has ended
                            #print("END OF ILLUMINATION PERIOD FOR AGENT ", agent_id)
                            agent_params[3]=agent_params[3] #+ random.randint(-1,1)
                        if timer > (light_duration + light_relaxation):
                            agent_params[5]=0              
                agent_id += 1
        #send agent coordinates to projector
        for points in control_agents:
            coordinate = (points[0],points[1])
            transformedRadius = (points[2]*stretch_x, points[3]*stretch_y)
            transformedCoordinate = coordinateTransform(coordinate)
            projectionList.append([int(transformedCoordinate[0]),int(transformedCoordinate[1]), int(transformedRadius[0]), int(transformedRadius[1])])
            #transmit projection list to projector and wait for response to verify message recieved
        transmit(projectionList)
        recieve()
        past_agents = img_agents
        counter += 1
        projectionList = []
        cv2.imshow("Image", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    return agent_list

def agentMatching(past_contours, img_contours):
    #to match agents in the current frame to the correct ID based on position
    matched_agents = np.copy(past_contours)
    #set propagating agents to 1
    #caculate length of deactivity, becomes increasingly negative the more frames are dropped
    #note that if the countour is matched in the subsequent section, is will reset to zero
    for agent in matched_agents:
        agent[5]=agent[5]+(agent[4]-1)
    #set current activity to deactice for all agents
    matched_agents[0:len(matched_agents), 4]=0
    for agent in img_contours:
        position_difference_match = 10000
        agent_id = 0
        for past_agent in past_contours:
            #excludes long term deactivated agents
            if past_agent[5] > -3:
                position_difference=(abs(agent[0]-past_agent[0]), abs(agent[1]-past_agent[1]))
                position_difference=sum(position_difference)
                if position_difference < position_difference_match:
                    contour_match = agent
                    past_contours_match = past_agent
                    matched_agent_id = agent_id
                    position_difference_match=position_difference  
            else:
                pass
            agent_id+=1
        #if the agent falls outside of a given confidence inteval, assume new agents and append to the end of the array 
        if position_difference_match > 35:
            contour_match = np.array([contour_match])
            matched_agents= np.append(matched_agents, contour_match, axis = 0)
        else:
            matched_agents[matched_agent_id]=contour_match
    #carry over propogation number
    return matched_agents


def velocity_calculation(agent_list, past_contours, img_contours, time_difference, counter):
    #calculate velocity and update light parameters
    new_agents = len(img_contours)- len(past_contours)
    if new_agents > 0:
        for i in range(new_agents):
            agent_list.append([])
    for i in range(len(img_contours)-new_agents):
        if img_contours[i][5]>-3: #checks if active 
            (x,y) = img_contours[i][0], img_contours[i][1]
            (x_past, y_past) = past_contours[i][0], past_contours[i][1]
            #velocity_direction=[img_contours[i][0]-past_contours[i][0], img_contours[i][1]-past_contours[i][1]]
            displacement=(x-x_past , y- y_past)
            total_displacement = math.sqrt(displacement[0]**2+displacement[1]**2)
            velocity = total_displacement/time_difference
            (light_duration,light_relaxation)=update_global_light_params()
            timer = 0
            if len(agent_list[i])>0: #checks if has been active for longer than 1 frame so past data can be accessed 
                past_index = len(agent_list[i])-1
                light_duration =  agent_list[i][past_index][3]+random.randint(-1,1)
                light_relaxation =  agent_list[i][past_index][4]+random.uniform(-1,1)
                timer = agent_list[i][past_index][5]+1
                past_velocity = agent_list[i][past_index-1][0]
                current_velocity = agent_list[i][past_index][0]
                velocity_change = current_velocity - past_velocity
            #each time step, agent has these 6 parameters associated with it, all are stored in an expanding array over time
            #time is local, counter is global timer 
            agent_list[i].append([velocity, time_difference, counter, light_duration, light_relaxation, timer])

    return agent_list

def write_to_file(agent_list):
    df = pandas.DataFrame(agent_list)
    df.to_csv('agent_list.csv')
    print("Data written")
 
if __name__=="__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind(('localhost', 65455))
        serversocket.listen()
        clientsocket, addr = serversocket.accept()
        print("LISTENING ON 65455")
        with clientsocket:
            agent_list = agent_location(centerPoint)
            transmit("NONE")
            acceptmsg = recieve()
            print(acceptmsg)
            #terminate socket connection where no messages are being recieved
            if not acceptmsg or "NONE" in acceptmsg:
                print("BREAK")
                
    write_to_file(agent_list)
