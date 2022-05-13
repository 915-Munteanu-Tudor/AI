import random
from const import *

import numpy as np


class Drone:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def setCoords(self, x, y):
        self.__x = x
        self.__y = y


class Map:
    def __init__(self):
        self.surface = np.zeros((MAP_HEIGHT, MAP_WIDTH))
        self.randomMap()

    def randomMap(self, fill=0.2):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if random.random() <= fill:
                    self.surface[i][j] = 1

    def setValueOnPos(self, x, y, val):
        self.surface[x][y] = val

    def __str__(self):
        string = ""
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def getSurface(self):
        return self.surface


class Sensor:
    def __init__(self, x, y, dmap):
        # self.__x = randint(0,MAP_HEIGHT)
        # self.__y = randint(0,MAP_WIDTH)
        self.__x = x
        self.__y = y
        self.__accPositions = [0 for _ in range(6)]  # energy value
        self.__map = dmap
        self.__maxEnergyLevel = 0

    def validCoord(self, x, y):
        return -1 < x < MAP_HEIGHT and -1 < y < MAP_WIDTH and self.__map.getSurface()[x][y] != 1

    def detectMaxEnergy(self):
        # find the greatest energy, on all the 4 directions from a point and save in accPos
        blocked = [False for _ in range(4)]

        # energy value between 1-5
        for i in range(1, 6):
            self.__accPositions[i] = self.__accPositions[i - 1]
            for d in range(4):
                if not blocked[d]:
                    newX = self.__x + dir[d][0] * i
                    newY = self.__y + dir[d][1] * i
                    if self.validCoord(newX, newY):
                        self.__accPositions[i] += 1
                    else:
                        blocked[d] = True

    def computeMaxEnergyLevel(self):
        # establish the max energy level, overall for the sensor; searches for redundant usage of energy in that if
        for energy in range(5):
            if self.__accPositions[energy] == self.__accPositions[energy + 1]:
                self.__maxEnergyLevel = energy
                return
        self.__maxEnergyLevel = 5

    def getMaxEnergy(self):
        return self.__maxEnergyLevel

    def getAccessiblePositions(self):
        return self.__accPositions

    def getCoords(self):
        coord = (self.__x, self.__y)
        return coord

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y


class Ant:
    def __init__(self):
        self.__size = SENSOR_COUNT
        self.__path = [random.randint(0, SENSOR_COUNT - 1)]
        self.__fitness = 0
        self.__battery = BATTERY

    def __getPossibleMoves(self, distances):
        # distances is a table containing distances from one sensor to another
        moves = []
        # for sensors, we will work with indexes
        currentSensor = self.__path[-1]

        for nextSensor in range(SENSOR_COUNT):
            if nextSensor != currentSensor and distances[currentSensor][nextSensor] != INFINITY and \
                    nextSensor not in self.__path and self.__battery >= distances[currentSensor][nextSensor]:
                moves.append(nextSensor)
        return moves

    def __computeProbabilityOfChoosingNextSensor(self, moves, alpha, beta, distances, pheromones):
        currentSensor = self.__path[-1]
        nextSensorProb = [0 for _ in range(SENSOR_COUNT)]

        for i in moves:
            distanceNextSensor = distances[currentSensor][i]
            # if there were pheromones used
            if distanceNextSensor <= self.__battery:
                pheromoneNextSensor = pheromones[currentSensor][i]
                if pheromoneNextSensor != 0:
                    # (the pheromone concentration on that distance) ^ alpha
                    # multiplied with
                    # (the static probability that the ants choose that distance)^beta
                    nextSensorProb[i] = (pheromoneNextSensor ** alpha) * (distanceNextSensor ** beta)


        return nextSensorProb

    def nextMove(self, distances, pheromones, q0, alpha, beta):
        # q0 = probability that the ant chooses the best possible move
        # param alpha: coefficient that controls the trail importance (how many ants have visited that edge)
        # param beta: coefficient that controls the visibility importance (how close is the next node / city / ...)
        moves = self.__getPossibleMoves(distances)
        if not moves:
            return False  # the move wasn't completed successfully

        nextNodeProb = self.__computeProbabilityOfChoosingNextSensor(moves, alpha, beta, distances, pheromones)
        # try to choose the best move, depending on the probability
        if random.random() < q0:
            bestProb = max(nextNodeProb)
            selectedNode = nextNodeProb.index(bestProb)
        else:
            selectedNode = self.__roulette(nextNodeProb)

        # put the node in the path and take the remaining battery
        self.__battery -= distances[self.__path[-1]][selectedNode]
        self.__path.append(selectedNode)

        return True

    def __roulette(self, nextNodeProb):
        # sum of probs of all nex moves
        probSum = sum(nextNodeProb)

        # if is 0, choose randomly
        if probSum == 0:
            return random.randint(0, len(nextNodeProb) - 1)

        # compute and put in list, report of first elem/sum, first 2 elems/sum, and so on
        pSum = [nextNodeProb[0] / probSum]
        for i in range(1, len(nextNodeProb)):
            pSum.append(pSum[i - 1] + nextNodeProb[i] / probSum)

        # choose randomly a position
        r = random.random()
        position = 0
        while r > pSum[position]:
            position += 1
        return position

    def computeFitness(self, distances):
        # sum of distances between every 2 consecutive sensors from the path => len of full path
        length = 0
        for i in range(1, len(self.__path)):
            length += distances[self.__path[i - 1]][self.__path[i]]

        self.__fitness = length

    def getFitness(self):
        return self.__fitness

    def getPath(self):
        return self.__path

    def getBattery(self):
        return self.__battery
