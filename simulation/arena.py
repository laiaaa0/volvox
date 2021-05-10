from simulation.agent import Agent
from simulation.geometry import Rectangle, Point
from simulation.light_updater import new_pattern
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import enum


class Pattern(enum.Enum):
    SQUARE = 1
    CIRCLE = 2
    DYNAMIC = 3


class Arena():
    def __init__(self, num_agents=5, pattern=Pattern.SQUARE):
        self.__width = 100
        self.__height = 100
        self.__rectangle = Rectangle(-self.__width / 2, -
                                     self.__height / 2, self.__width, self.__height)
        self.__agent_list = []
        self.initialise_agents(num_agents)
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111, aspect='equal')
        self.__ax.set_autoscale_on(False)
        self.__ax.axis([-self.__width / 2, self.__width /
                        2, -self.__height / 2, self.__height / 2])

        self.__dynamic_updates = (pattern==Pattern.DYNAMIC)
        self.__pattern = np.zeros(
            (self.__width, self.__height), dtype=np.uint8)
        if pattern == Pattern.SQUARE:
            self.__pattern[int(self.__width /
                               3):int(2 *
                                      self.__width /
                                      3), int(self.__height /
                                              3):int(2 *
                                                     self.__height /
                                                     3)] = 1
        elif pattern == Pattern.CIRCLE:
            (x, y) = np.ogrid[0:self.__width, 0:self.__height]

            (center_x, center_y) = (self.__width / 2, self.__height / 2)
            radius = 20
            # create a circle mask which is centered in the middle of the
            # image, and with radius 100
            circle_mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2
            self.__pattern[circle_mask] = 1


    def initialise_agents(self, num_agents: int, seed=42):
        random.seed(seed)
        for _ in range(num_agents):
            self.__agent_list.append(
                Agent(
                    self.__rectangle,
                    speed=10 * random.random(),
                    theta=random.uniform(
                        0,
                        2 * math.pi),
                    pos=self.__rectangle.random_point(seed),
                    frames_on=random.randint(
                        10,
                        20),
                    frames_off=random.randint(
                        3,
                        5)))

    def image_from_pattern(self):
        coloured_pattern = np.ones(
            (self.__width, self.__height, 4), dtype=np.uint8) * 255
        coloured_pattern[:, :, 2] = 0
        coloured_pattern[:, :, 3] = self.__pattern * 255
        img = Image.fromarray(coloured_pattern, mode="RGBA")
        return img

    def agent_pos_to_light_index(self, position:Point):
        # position range from -width/2 to +width/2, -height/2 to +height/2
        # numpy range from 0 to width and from 0 to height
        transformed_position = position + \
            Point(self.__width / 2, self.__height / 2)
        x = min(max(0,int(transformed_position.x())), self.__width - 1)
        y = self.__height - max(1,min(int(transformed_position.y()), self.__height))

        return (y,x) # change (x,y) to (row,column)

    def is_position_illuminated(self, position: Point):
        (row,column) = self.agent_pos_to_light_index(position)
        return self.__pattern[row,column]

    def update(self):
        if self.__dynamic_updates:
            positions =[self.agent_pos_to_light_index(a.position()) for a in self.__agent_list]

            self.__pattern = new_pattern(self.__pattern.shape, positions)
        for agent in self.__agent_list:
            agent.update(self.is_position_illuminated(agent.position()))
        

    def plot(self):
        self.__ax.cla()
        x = [a.position().x() for a in self.__agent_list]
        y = [a.position().y() for a in self.__agent_list]
        self.__ax.plot(x, y, 'bo')
        self.__ax.axis([-self.__width / 2, self.__width /
                        2, -self.__height / 2, self.__height / 2])
        self.__ax.imshow(self.image_from_pattern(), extent=(self.__ax.axis()))
        plt.pause(0.05)
