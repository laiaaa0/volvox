import numpy as np

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
