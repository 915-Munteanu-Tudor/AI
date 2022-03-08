from random import randint

from Drone import Drone
from DroneMap import DMap
from Environment import Environment
from Variables import *


class Service:
    def __init__(self):
        self.__environment = Environment(SIZE, SIZE)
        self.__droneMap = DMap()
        self.__drone = Drone(randint(0, SIZE - 1), randint(0, SIZE - 1))
        self.__environment.loadEnvironment("test2.map")

    def getEnvironmentImage(self):
        return self.__environment.image()

    def getDroneMapImage(self):
        return self.__droneMap.image(self.__drone.x, self.__drone.y)

    def droneCanStillMove(self):
        return self.__drone.canMove()

    def moveDFS(self):
        return self.__drone.moveDSF(self.__droneMap)

    def markDetectedWalls(self):
        self.__droneMap.markDetectedWalls(self.__environment, self.__drone.x, self.__drone.y)
