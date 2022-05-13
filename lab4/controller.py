from sensorList import *
from domain import *


class Controller:
    def __init__(self):
        self.__map = Map()
        self.__drone = Drone(0, 0)

        # place the drone on an empty position
        self.__placeDroneOnEmptyPos()

        # get the sensor list
        self.__sensors = SensorList(self.__map)

        # default pheromone matrix between all the sensors
        self.__pheromones = [[1.0 for _ in range(SENSOR_COUNT)] for _ in range(SENSOR_COUNT)]

        # get the matrix of distances between all the sensors
        self.__distances = self.__sensors.getDistBetweenSensors()

    def __placeDroneOnEmptyPos(self):
        # look for an empty position on the map until finding one, then set its coordinates
        crtX, crtY = random.randint(0, MAP_HEIGHT-1), random.randint(0, MAP_WIDTH-1)
        while self.__map.getSurface()[crtX][crtY] == 1:
            crtX, crtY = random.randint(0, MAP_HEIGHT-1), random.randint(0, MAP_WIDTH-1)
        self.__drone.setCoords(crtX, crtY)

    def __moveAnts(self, ants, alpha, beta, q0):
        # try to perform a move for every ant and select only those which can perform
        # fpr thos alive, compute theit fitness and put them in a list
        antLives = [True for _ in ants]
        for i in range(len(ants)):
            ant = ants[i]
            for step in range(SENSOR_COUNT - 1):
                found = ant.nextMove(self.__distances, self.__pheromones, q0, alpha, beta)
                if not found:
                    antLives[i] = False
                    break

        aliveAnts = []
        for i in range(len(ants)):
            if antLives[i]:
                ants[i].computeFitness(self.__distances)
                aliveAnts.append(ants[i])
        return aliveAnts

    def __selectBestAnt(self, ants):
        # select the ant with the best fitness => the lowest len path
        bestAnt = None
        bestFitness = INFINITY

        for ant in ants:
            if bestFitness > ant.getFitness():
                bestFitness = ant.getFitness()
                bestAnt = ant
        return bestAnt

    def __simulateEpoch(self, nrAnts, alpha, beta, q0, rho):
        ants = [Ant() for _ in range(nrAnts)]

        # perform a move for every ant
        ants = self.__moveAnts(ants, alpha, beta, q0)
        # nr iterations from epoch = len of solution
        for i in range(SENSOR_COUNT):
            for j in range(SENSOR_COUNT):
                # update the pheromones' matrix, for the trace left by all the ants
                self.__pheromones[i][j] = (1 - rho) * self.__pheromones[i][j]

        # check for alive ants after moving
        if not ants:
            return None

        # for every ant update the pheromones for its every two consecutive sensors from its path with 1/ant's fitness
        newPheromones = [1.0 / ant.getFitness() for ant in ants]
        for i in range(len(ants)):
            current = ants[i].getPath()
            for j in range(len(current) - 1):
                currentSensor = current[j]
                nextSensor = current[j + 1]
                self.__pheromones[currentSensor][nextSensor] += newPheromones[i]

        return self.__selectBestAnt(ants)

    def __chargeSensors(self, remainingBattery, accessibleSensors):
        # take all the sensors, set their energy to 0, check if it is still battery in the drone
        # sort the sensors by the report between the coefficient of the sensor for getting energy 5, over max energy
        # begin to assign to the sensors their max energy until there is no more battery => then the rest of the sensors
        # get the energy 0
        sensors = []
        for i in range(len(self.__sensors.getSensorList())):
            if i in accessibleSensors:
                sensors.append(self.__sensors.getSensorList()[i])

        energyLevels = [0 for _ in sensors]
        if remainingBattery <= 0:
            return energyLevels

        sensors.sort(key=lambda s: (s.getAccessiblePositions()[-1] / s.getMaxEnergy()))
        i = 0
        while i < len(sensors) and remainingBattery > 0:
            currentSensorMaxEnergy = sensors[i].getMaxEnergy()
            if remainingBattery > currentSensorMaxEnergy:
                remainingBattery -= currentSensorMaxEnergy
                energyLevels[i] = currentSensorMaxEnergy
            else:
                energyLevels[i] = remainingBattery
                remainingBattery = 0
            i += 1
        return energyLevels

    def __updateBestSolution(self, bestSolution):
        # take the best solution for an epoch
        currentSolution = self.__simulateEpoch(ANT_COUNT, ALPHA, BETA, Q0, RHO)
        if currentSolution is None:
            return bestSolution

        currentSolutionPathLength = len(currentSolution.getPath())
        if bestSolution is None or currentSolutionPathLength > len(bestSolution.getPath()) \
                or (currentSolutionPathLength == len(
            bestSolution.getPath()) and currentSolution.getFitness() < bestSolution.getFitness()):
            return currentSolution  # new best solution
        return bestSolution

    def run(self):
        bestSolution = None  # will be the one with the lowest cost path

        print("Starting")
        # take the best solution from all the epochs
        for epoch in range(EPOCH_COUNT):
            bestSolution = self.__updateBestSolution(bestSolution)

        # get the energy to charge each sensor
        energyLevels = self.__chargeSensors(BATTERY - bestSolution.getFitness(), bestSolution.getPath())
        print("Best path: ")
        for indices in bestSolution.getPath():
            print(self.__sensors.getSensorList()[indices].getCoords(), end=" ")
        print("\nEnergy in each sensor: ", energyLevels)
        # min distance between each pair of sensors in self.__distances => can be displayed
        print("Energy left in there: ", bestSolution.getBattery(), end=" ")

    def getMap(self):
        return self.__map

    def setMap(self, dmap):
        self.__map = dmap

    def getMapSurface(self):
        return self.__map.getSurface()

    def getDroneXCoord(self):
        return self.__drone.getX()

    def getDroneYCoord(self):
        return self.__drone.getY()
