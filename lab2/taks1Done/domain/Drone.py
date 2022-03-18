import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from sources.common import *


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPosition(self):
        return self.x, self.y

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < SIZE_LINES - 1:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < SIZE_COLUMNS - 1:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("I:\\materiale\\an2\\sem2\\AI\\lab2\\taks1Done\\images\\drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))

        return mapImage

    def mapWithDroneAndEndPoint(self, mapImage, endPoint):
        drona = pygame.image.load("I:\\materiale\\an2\\sem2\\AI\\lab2\\taks1Done\\images\\drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))
        b = pygame.image.load("I:\\materiale\\an2\\sem2\\AI\\lab2\\taks1Done\\images\\mountain.png")
        mapImage.blit(b, (endPoint[1] * 20, endPoint[0] * 20))

        return mapImage
