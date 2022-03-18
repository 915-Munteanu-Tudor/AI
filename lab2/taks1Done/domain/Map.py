import pickle
from random import random
import numpy as np
import pygame
from sources.common import *


class Map:
    def __init__(self, n=SIZE_LINES, m=SIZE_COLUMNS):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

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

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((SIZE_COLUMNS * 20, SIZE_LINES * 20))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

    def isBrickOrOut(self, x):
        if x[0] < 0 or x[1] < 0:
            return True
        if x[0] >= self.n or x[1] >= self.m:
            return True
        if self.surface[x[0]][x[1]] == 1:
            return True
        return False
