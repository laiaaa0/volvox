from simulation.agent import Agent
from simulation.geometry import Rectangle
import math
import random
import matplotlib.pyplot as plt


class Arena():
    def __init__(self, num_agents=5):
        self.__width = 10
        self.__height = 10
        self.__rectangle = Rectangle(-self.__width/2, -self.__height/2, self.__width, self.__height)
        self.__agent_list = []
        self.initialise_agents(num_agents)
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111, aspect='equal')
        self.__ax.set_autoscale_on(False)
        self.__ax.axis([-self.__width/2, self.__width/2, -self.__height/2, self.__height/2])
        print(self.__ax.get_autoscale_on())


    def initialise_agents(self, num_agents : int, seed=42):
        random.seed(seed)
        for _ in range(num_agents):
            self.__agent_list.append(Agent(self.__rectangle, speed =random.random(), theta=random.uniform(0,2*math.pi), pos = self.__rectangle.random_point(seed)))



    def update(self):
        for agent in self.__agent_list:
            agent.update(False)

    def plot(self):
        self.__ax.cla()
        x = [a.position().x() for a in self.__agent_list]
        y = [a.position().y() for a in self.__agent_list]
        self.__ax.plot(x, y, 'bo')
        self.__ax.axis([-self.__width/2, self.__width/2, -self.__height/2, self.__height/2])
        plt.pause(0.05)
