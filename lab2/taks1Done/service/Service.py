import queue
from math import sqrt
import random
import math


class Service:
    def __init__(self, drone, droneMap):
        self.__drone = drone
        self.__droneMap = droneMap

    def searchAStar(self, finalX, finalY):
        start = self.__drone.getPosition()
        end = (finalX, finalY)
        print("Start: ", start, "End: ", end)
        path = self.__bestFirstSearch(start, end, lambda current: self.euclideanDistance(current, end) + self.euclideanDistance(start, current))

        if not path[0]:
            return []
        else:
            return self.computePath(path[1], end)

    def searchGreedy(self, finalX, finalY):
        start = self.__drone.getPosition()
        end = (finalX, finalY)
        print("Start: ", start, "End: ", end)
        path = self.__bestFirstSearch(start, end, lambda current: self.euclideanDistance(current, end))
        if not path[0]:
            return []
        else:
            return self.computePath(path[1], end)

    def computePath(self, dict, end):
        path = []
        while end != -1:
            path.append(end)
            end = dict[end]
        path.reverse()
        return path

    def getMap(self):
        return self.__droneMap

    def getDrone(self):
        return self.__drone

    def __getNeighbours(self, node):
        pos = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        arr = [self.addCoordinates(node, pos[pos.index(x)]) for x in pos]
        arr = [x for x in arr if not self.__droneMap.isBrickOrOut(x)]
        return arr

    @staticmethod
    def addCoordinates(x, y):
        return x[0] + y[0], x[1] + y[1]

    def __bestFirstSearch(self, start, element, priorityFunction):
        found = False
        visited = []
        toVisit = queue.PriorityQueue()
        toVisit.put((priorityFunction(start), start))
        predecessor = {start: -1}
        while not toVisit.empty() and not found:
            if toVisit.empty():
                return False, []
            node = toVisit.get(block=False)[1]
            if node not in visited:
                visited.append(node)
            else:
                continue
            if node == element:
                found = True
            else:
                for child in self.__getNeighbours(node):
                    if child not in visited:
                        toVisit.put((priorityFunction(child), child))
                        predecessor[child] = node

        return found, predecessor

    @staticmethod
    def euclideanDistance(x, y):
        return sqrt((y[0] - x[0]) * (y[0] - x[0]) + (y[1] - x[1]) * (y[1] - x[1]))

    def loadMap(self):
        self.__droneMap.loadMap("sources/test1.map")

    def randomMap(self):
        self.__droneMap.randomMap()
