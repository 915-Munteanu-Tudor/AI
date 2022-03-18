# import the pygame module, so you can use it
import pygame
from random import randint

from pygame.locals import *

# Creating some colors
from domain.Drone import Drone
from domain.Map import Map
from sources.common import *
from service.Service import Service
import time


def dummysearch():
    # example of some path in test1.map from [5,7] to [7,11]
    return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]


def moveInBoth(move, paths):
    return move in paths[0] and move in paths[1]


def displayWithPath(service, paths, end, colour=None):
    if colour is None:
        colour = [GREEN]
    image = service.getMap().image()
    mark = pygame.Surface((20, 20))

    for path in paths:
        for move in path:
            if moveInBoth(move, paths):
                mark.fill(colour[2])
            else:
                mark.fill(colour[paths.index(path)])
            image.blit(mark, (move[1] * 20, move[0] * 20))
    image = service.getDrone().mapWithDroneAndEndPoint(image, end)
    return image


# define a main function
def main():
    # we create the map
    m = Map()
    # m.randomMap()
    # m.saveMap("test2.map")

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("I:\\materiale\\an2\\sem2\\AI\\lab2\\taks1Done\\images\\logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we position the drone somewhere in the area
    x = randint(0, SIZE_LINES - 1)
    y = randint(0, SIZE_COLUMNS - 1)

    # create drona
    d = Drone(x, y)

    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((SIZE_COLUMNS * 20, SIZE_LINES * 20))
    screen.fill(WHITE)

    service = Service(d, m)
    service.randomMap()
    # define a variable to control the main loop
    running = True
    screen.blit(service.getDrone().mapWithDrone(service.getMap().image()), (0, 0))
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == KEYDOWN:
                endX = randint(0, SIZE_LINES - 1)
                endY = randint(0, SIZE_COLUMNS - 1)
                while service.getMap().isBrickOrOut([endX, endY]):
                    endX = randint(0, SIZE_LINES - 1)
                    endY = randint(0, SIZE_COLUMNS - 1)
                startTime = time.time()
                path1 = service.searchAStar(endX, endY)
                endTime = time.time()
                print("A* took", endTime - startTime, "time")
                startTime = time.time()
                path2 = service.searchGreedy(endX, endY)
                endTime = time.time()
                print("Greedy took", endTime - startTime, "time")

                # green is A* , red is greedy and pink is common path
                screen.blit(
                    displayWithPath(
                        service,
                        [path1, path2],
                        (endX, endY),
                        [GREEN, RED, PINK]
                    ),
                    (0, 0)
                )
        pygame.display.flip()

    pygame.display.flip()
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
