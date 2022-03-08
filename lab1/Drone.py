import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT


class Drone:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lastVisited = [(x, y)]
        self.visited = {}
        for i in range(0, 20):
            for j in range(0, 20):
                self.visited[(i, j)] = 0

    def canMove(self):
        return not (self.x is None or self.y is None)

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

    def moveDSF(self, detectedMap):
        # TO DO!
        # rewrite this function in such a way that you perform an automatic
        # mapping with DFS
        neighbours = []
        if self.x > 0:
            if detectedMap.surface[self.x - 1][self.y] == 0:
                neighbours.append((self.x - 1, self.y))
        if self.x < 19:
            if detectedMap.surface[self.x + 1][self.y] == 0:
                neighbours.append((self.x + 1, self.y))
        if self.y > 0:
            if detectedMap.surface[self.x][self.y - 1] == 0:
                neighbours.append((self.x, self.y - 1))
        if self.y < 19:
            if detectedMap.surface[self.x][self.y + 1] == 0:
                neighbours.append((self.x, self.y + 1))

        unvisited = [n for n in neighbours if self.visited[n] == 0]
        if not unvisited:
            if not self.lastVisited:
                self.x, self.y = None, None
                return False
            self.x, self.y = self.lastVisited.pop()

        #else:
        for n in neighbours:
            if self.visited[n] == 0:
                self.lastVisited.append((self.x, self.y))
                self.x, self.y = unvisited.pop()
                self.visited[(self.x, self.y)] += 1
        return True

