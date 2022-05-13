import pygame
from controller import *
from const import *
from pygame.constants import KEYDOWN


class GUI:
    def __init__(self, service):
        self.__initPygame()
        self.__screen = pygame.display.set_mode((400, 400))
        self.__screen.fill(WHITE)
        self.__service = service

    def getMapSurface(self):
        return self.__service.getMapSurface()

    def __initPygame(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("ACO")

    def __getMapImage(self, colour=BLUE, background=WHITE):
        image = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        sensor = pygame.Surface((20, 20))
        brick.fill(colour)
        image.fill(background)
        sensor.fill(GREEN)

        mapSurface = self.__service.getMapSurface()
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if mapSurface[i][j] == 1:
                    image.blit(brick, (j * 20, i * 20))
                elif mapSurface[i][j] == SENSOR_POSITION:
                    image.blit(sensor, (j * 20, i * 20))


        return image

    def __displayMap(self):
        droneImage = pygame.image.load("drona.png")
        pathImage = self.__getMapImage()
        pathImage.blit(droneImage, (self.__service.getDroneYCoord() * 20, self.__service.getDroneXCoord() * 20))
        self.__screen.blit(pathImage, (0, 0))
        pygame.display.update()

        return droneImage, pathImage

    def __waitForKeyboardInput(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return
            pygame.time.wait(1)

    def start(self):
        self.__displayMap()
        # self.__waitForKeyboardInput()
        self.__service.run()
        pygame.time.delay(50000)

