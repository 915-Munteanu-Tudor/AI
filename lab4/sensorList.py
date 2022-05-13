from const import *
from domain import *
import random


class SensorList:
    def __init__(self, dmap):
        self.__sensorList = []
        self.__map = dmap

        self.__placeSensors()

        # distance from every sensor to all the other sensors
        self.__distancesBetweenSensors = [[0 for _ in range(SENSOR_COUNT)] for _ in range(SENSOR_COUNT)]

        # get the matrix of distances between all the sensors
        self.__computeDistanceBetweenSensors()

        for sensor in self.__sensorList:
            # for every sensor, get it's maximum possible energy, and the chosen one
            sensor.detectMaxEnergy()
            sensor.computeMaxEnergyLevel()

    def validCoord(self, x, y):
        return -1 < x < MAP_HEIGHT and -1 < y < MAP_WIDTH and self.__map.getSurface()[x][y] != 1

    def BFS(self, startX, startY, endX, endY):
        # bfs to find the distance between 2 points on map; returns infinity if there is bot a way between them
        distance = {(startX, startY): 0}
        visited = [(startX, startY)]

        while visited:
            currentX, currentY = visited.pop(0)
            for d in dir:
                newX = currentX + d[0]
                newY = currentY + d[1]
                if self.validCoord(newX, newY) and (newX, newY) not in distance:
                    distance[(newX, newY)] = distance[(currentX, currentY)] + 1
                    visited.append((newX, newY))

                    if newX == endX and newY == endY:
                        return distance[(endX, endY)]
        return INFINITY

    def __placeSensors(self):
        # search a valid position to put each sensor on map until finding them and append them to the sensors list
        # mark the position with the corresponding value for the sensors
        self.__sensorList.clear()

        for s in range(SENSOR_COUNT):
            newX, newY = random.randint(0, MAP_HEIGHT - 1), random.randint(0, MAP_WIDTH - 1)
            while self.__map.getSurface()[newX][newY] != 0:
                newX, newY = random.randint(0, MAP_HEIGHT - 1), random.randint(0, MAP_WIDTH - 1)

            self.__map.setValueOnPos(newX, newY, SENSOR_POSITION)
            self.__sensorList.append(Sensor(newX, newY, self.__map))

    def __computeDistanceBetweenSensors(self):
        # compute the distances between all the sensors and put it in the matrix of distances at [i][j] and [j][i]
        for i in range(len(self.__sensorList)):
            self.__distancesBetweenSensors[i][i] = 0
            newX, newY = self.__sensorList[i].getX(), self.__sensorList[i].getY()
            for j in range(i + 1, len(self.__sensorList)):
                dist = self.BFS(newX, newY, self.__sensorList[j].getX(), self.__sensorList[j].getY())
                self.__distancesBetweenSensors[i][j] = self.__distancesBetweenSensors[j][i] = dist

    def getSensorList(self):
        return self.__sensorList

    def getDistBetweenSensors(self):
        return self.__distancesBetweenSensors
