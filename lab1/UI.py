# import the pygame module, so you can use it
import time

import pygame

from Service import Service
from Variables import *


def display_text(msg, screen):
    font = pygame.font.SysFont('corbel', 35, True)
    text = font.render(msg, True, LIGHTBLUE)
    text_rect = text.get_rect()
    text_rect.center = (400, 200)
    screen.fill(LIGHTPURPLE)
    screen.blit(text, text_rect)
    pygame.display.update()


def main():
    # initialize the pygame module
    pygame.init()

    # load and set the logo
    logo = pygame.image.load("explore.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("New world exploration")

    service = Service()

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800, 400))
    screen.fill(WHITE)
    screen.blit(service.getEnvironmentImage(), (0, 0))

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            # if event.type == KEYDOWN:
            # use this function instead of move
        if service.droneCanStillMove():
            service.markDetectedWalls()
            screen.blit(service.getDroneMapImage(), (400, 0))

        running = service.moveDFS()
        time.sleep(0.6)
        pygame.display.flip()

    display_text("Exploration done!", screen)
    pygame.time.delay(3500)
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
