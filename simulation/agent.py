from simulation.geometry import Point, Rectangle
import math


class Habituation():
    def __init__(self,frames : int):
        self.__is_habituated = False 
        self.__frames_since_change = 0
        self.__frames_to_habituate = frames

    def reset(self):
        self.__is_habituated = False
        self.__frames_since_change = 0
    
    def increase(self):
        self.__frames_since_change = self.__frames_since_change+1
        if self.__frames_since_change > self.__frames_to_habituate:
            self.__is_habituated = True 
        
    def is_habituated(self):
        return self.__is_habituated

class Agent():
    def __init__(self, arena: Rectangle, speed : float, theta : float, pos : Point, frames_on : int, frames_off:int):
        self.__base_speed = speed
        self.__current_speed = speed
        self.__current_position = pos
        self.__direction_theta = theta
        self.__arena_rect = arena
        
        # When the light is turned on, it will stop immediately, then after #frames_on it will habituate
        self.__frames_to_habituate_on = frames_on
        # When the light is off, it will start moving, but will not stop with light until after #frames_off
        self.__frames_to_habituate_off = frames_off

        self.__habituated_dark = Habituation(self.__frames_to_habituate_off)
        self.__habituated_light = Habituation(self.__frames_to_habituate_on)


    def position(self):
        return self.__current_position

    def rebound(self):        
        self.__direction_theta = self.__arena_rect.rebound(self.__current_position,self.__direction_theta)

    
    def update(self, light_on : bool):
        if light_on:
            if self.__habituated_light.is_habituated(): 
                # There's been light for a while       
                self.__current_speed = self.__base_speed
            else:
                if self.__habituated_dark.is_habituated():
                    # We're zapping
                    self.__current_speed = 0
            self.__habituated_light.increase()
            self.__habituated_dark.reset()

        else:
            self.__habituated_dark.increase()
            self.__habituated_light.reset()           
            self.__current_speed = self.__base_speed



        self.__current_position.update(self.__current_speed, self.__direction_theta)
        if not self.__arena_rect.contains(self.__current_position):
            self.rebound()
