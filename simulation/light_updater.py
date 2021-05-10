import numpy as np
from simulation.geometry import Point


def add_square(array, square_center, square_size:int):
    top_left_x = int(max(0, square_center.x()-square_size/2))
    top_left_y = int(max(0, square_center.y()-square_size/2))
    bottom_left_x = int(min(array.shape[0]-1, top_left_x+square_size))
    bottom_left_y = int(min(array.shape[1]-1, top_left_y+square_size))
    array[top_left_x:bottom_left_x,top_left_y:bottom_left_y]=1

def new_pattern(size, agent_positions):
    pattern = np.zeros(size)
    for (posx,posy) in agent_positions:
        point = Point(int(posx),int(posy))
        add_square(pattern,point,10)
    return pattern