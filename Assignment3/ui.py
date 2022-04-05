# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *
import matplotlib.pyplot as plt
from domain import *
from utils import *


def drawPlot(values):
    print(values)
    arr = np.array(values)
    m = np.mean(arr, axis=0)
    std = np.std(arr, axis=0)
    means = []
    stddev = []
    means.append(m)
    stddev.append(std)
    plt.plot(means)
    plt.plot(stddev)
    plt.plot(values)
    plt.show()


class UI:
    def __init__(self):
        self.__service = controller()
        self.path = Population(0, 0)
        self.fitnesses = []

    @staticmethod
    def printMenu():
        print("Map options")
        print("1. Create a random map")
        print("2. Load a map")
        print("3. Save map")
        print("4. Visualise map")
        print("-----------------")
        print("5. Parameters setup")
        print("6. Run solver")
        print("7. Visualise statistics")
        print("8. View the drone moving on a path")
        print("9. Exit")

    def createRandomMap(self):
        self.__service.getMap().randomMap()
        self.__service.getMap().saveMap("talk.map")

    def loadMap(self):
        file = input("file: ")
        self.__service.getMap().loadMap(file)
        self.__service.getMap().saveMap("talk.map")

    def saveMap(self):
        file = input("file: ")
        self.__service.getMap().saveMap(file)

    def viewMap(self):
        screen = initPyGame((self.__service.getMap().n * 20, self.__service.getMap().m * 20))
        for i in range(20):
            screen.blit(image(self.__service.getMap()), (0, 0))
        pygame.display.flip()
        pygame.time.wait(5000)
        closePyGame()

    def parametersSetup(self):
        Util.batteryCapacity = int(input("Battery capacity: "))
        Util.maxIterations = int(input("Max iterations: "))
        Util.populationSize = int(input("Population size: "))
        Util.individualSize = int(input("Individual size: "))

    def runSolver(self):
        start = time.time()
        result = self.__service.solver()
        self.path = result[0]
        self.fitnesses = result[1]
        end = time.time()
        print("Execution time: ", end - start)
        print("Best fitness: ", self.path.bestFitness())

    def viewStats(self):
        lista = []
        for i in range(0, 100):
            seed(i)
            print("Iteration: ", i)
            val = self.__service.solver()
            print(val)
            lista.append(val.bestFitness())
        drawPlot(lista)

    def viewStats1(self):
        lista = self.fitnesses
        drawPlot(lista)

    def viewMovingDrone(self):
        movingDrone(
            currentMap=self.__service.getMap(),
            path=self.path.getIndividuals()[0].getVisited(),
            speed=100
        )

    def start(self):

        while True:
            self.printMenu()
            ch = int(input("Choice: "))
            if ch == 1:
                self.createRandomMap()
            elif ch == 2:
                self.loadMap()
            elif ch == 3:
                self.saveMap()
            elif ch == 4:
                self.viewMap()
            elif ch == 5:
                self.parametersSetup()
            elif ch == 6:
                self.runSolver()
            elif ch == 7:
                self.viewStats1()
            elif ch == 8:
                self.viewMovingDrone()
            elif ch == 9:
                break


if __name__ == "__main__":
    ui = UI()
    ui.start()

# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls
