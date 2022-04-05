# -*- coding: utf-8 -*-
import pickle
from random import *
from utils import *
import numpy as np


# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation

class gene:
    def __init__(self, x=-2, y=-2):
        if x == -2 or y == -2:
            ind = randint(0, 3)
            self.__direction = Util.v[ind]
        else:
            self.__direction = (x, y)

    @property
    def direction(self):
        return self.__direction

    def __getitem__(self, item):
        return self.__direction[item]

    def __repr__(self) -> str:
        return "Gene {" + str(self.__direction) + "}"


class Individual:
    def __init__(self, size=0):
        self.__size = size
        self.__x = [gene() for _ in range(self.__size)]
        self.__visited = []
        self.__initialValue = Util.initialPosition
        self.__map = Map()
        self.__map.loadMap("talk.map")
        self.move()
        self.__f = None

    def getFitnessValue(self):
        self.fitness()
        return self.__f

    def fitness(self):
        self.__f = -len(set(self.__visited))

    def move(self):
        self.__visited.clear()
        current = self.__initialValue
        self.__visited.append(current)
        for i in range(0, len(self.__x)):
            this = self.__x[i]
            if self.__map.isWall(Util.addDirections(current, this)):
                break
            current = Util.addDirections(current, this)
            self.__visited.append(current)

    def getVisited(self):
        return self.__visited

    def mutate(self, mutateProbability=0.04):
        if random() < mutateProbability:
            direction = choice(Util.v)
            self.__x[randint(0, len(self.__x) - 1)] = direction
            self.move()

    def crossover(self, otherParent, crossoverProbability=0.8):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)
        if random() < crossoverProbability:
            for i in range(len(otherParent.__x) // 2, len(otherParent.__x)):
                self.__x[i] = otherParent.__x[i]
            self.move()
        return offspring1, offspring2

    def __getitem__(self, item):
        return self.__x[item]

    def __repr__(self):
        return "Individual {" + str(self.__x) + "}"


class Population:
    def __init__(self, ps=Util.populationSize, indS=Util.individualSize):
        self.__populationSize = ps
        self.__v = [Individual(indS) for _ in range(ps)]
        self._individualSize = indS

    def evaluate(self):
        # evaluates the population
        for x in self.__v:
            x.fitness()

    def averageFitness(self):
        return np.average([x.getFitnessValue() for x in self.__v])

    def freeUnavailable(self, map):
        self.__v = [x for x in self.__v if not map.containsWalls(x)]

    def selection(self, k=0):
        # perform a selection of k individuals from the population
        # and returns that selection
        self.__v.sort(key=lambda v: v.getFitnessValue())
        self.__v = self.__v[:min(k, self.__populationSize)]
        return self.__v

    def getIndividuals(self):
        return self.__v

    def bestFitness(self):
        arr = sorted(self.__v, key=lambda v: v.getFitnessValue())
        arr = [x.getFitnessValue() for x in arr]
        return -arr[0]

    def extendPopulation(self):
        if len(self.__v) == 0:
            self.__v = [Individual(self._individualSize) for _ in range(self.__populationSize)]
        res = []
        for i in range(len(self.__v) // 2):
            res.append(choice(self.__v).crossover(choice(self.__v)))

        for i in res:
            self.__v.append(i[0])
            self.__v.append(i[1])
        self.selection(self.__populationSize)
        for i in self.__v:
            i.mutate()

    def __repr__(self):
        return "Population{" + str(self.__v) + "}"


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def saveMap(self, numFile="../sources/test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def nrZeroes(self):
        zero = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 0:
                    zero += 1
        return zero

    def containsWalls(self, path):
        for var in path:
            if var[0] < 0 or var[0] > Util.mapLength - 1 or \
                    var[1] < 0 or var[1] > Util.mapLength - 1 or self.surface[var[0]][var[1]] == 1:
                return True
        return False

    def isWall(self, var):
        if var[0] < 0 or var[0] > Util.mapLength - 1 or \
                var[1] < 0 or var[1] > Util.mapLength - 1 or self.surface[var[0]][var[1]] == 1:
            return True

        return False

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
