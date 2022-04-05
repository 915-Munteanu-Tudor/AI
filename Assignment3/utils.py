# -*- coding: utf-8 -*-
import math


class Util:
    @staticmethod
    def addDirections(x, y):
        return (x[0] + y[0]), (x[1] + y[1])

    # Creating some colors
    BLUE = (0, 0, 255)
    GRAYBLUE = (50, 120, 120)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # define directions
    UP = 0
    DOWN = 2
    LEFT = 1
    RIGHT = 3

    # define indexes variations
    v = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    # define mapsize

    mapLength = 20

    initialPosition = (7, 12)
    batteryCapacity = 100
    populationSize = 80
    individualSize = 200
    maxIterations = 5

