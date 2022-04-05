# -*- coding: utf-8 -*-

import pickle
from domain import *


class repository:
    def __init__(self):
        self.__population = None
        self.cmap = Map()

    def initRandomMap(self):
        self.cmap.randomMap()

    def createPopulation(self, args):
        # args = [populationSize, individualSize] -- you can add more args    
        self.__population = Population(args[0], args[1])
        return self.__population

    def saveMapToFile(self, fileName="../sources/test.map"):
        self.cmap.saveMap(fileName)

    def loadFile(self, fileName="../sources/test.map"):
        self.cmap.loadMap(fileName)

    def getPopulation(self):
        return self.__population

    def getIndividualsForPopulation(self):
        return self.__population.getIndividuals()
