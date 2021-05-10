import numpy as np
from simulation.geometry import Point


def add_square(array, square_center, square_size:int):
    startx = int(max(0, square_center.x()-square_size/2))
    starty = int(max(0, square_center.y()-square_size/2))
    endx = int(min(array.shape[0], square_center.x()+square_size/2))
    endy = int(min(array.shape[1], square_center.y()+square_size/2))
    array[startx:endx,starty:endy]=1

def new_pattern(size, agent_positions):
    pattern = np.zeros(size)
    for (posx,posy) in agent_positions:
        point = Point(int(posx),int(posy))
        add_square(pattern,point,10)
    return pattern