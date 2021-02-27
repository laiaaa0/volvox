from geometry import Point
from geometry import Rectangle
import math

class Agent():
    def __init__(self, arena: Rectangle, speed : float, theta : float, pos : Point):
        self.__current_speed = speed
        self.__light_on_effect = 0.5
        self.__light_off_effect = 0.5
        self.__current_position = pos
        self.__direction_theta = theta
        self.__arena_rect = arena
        # While there is light on, it will slow down infinitely
        # While there is no light, it will remain the same
        # TODO : When there is no light, the first N frames, it regains speed, then it remains constant
    

    def position(self):
        return self.__current_position

    def rebound(self):        
        self.__direction_theta = self.__arena_rect.rebound(self.__current_position,self.__direction_theta)

    
    def update(self, light_on : bool):
        if (light_on):
            self.__current_speed = self.__current_speed*(1-self.__light_on_effect)
        #else:
        #    self.__current_speed = self.__current_speed*(1-self.__light_on_effect)


        self.__current_position.update(self.__current_speed, self.__direction_theta)
        if not self.__arena_rect.contains(self.__current_position):
            self.rebound()