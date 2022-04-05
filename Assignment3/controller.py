from repository import *


class controller():
    def __init__(self):
        self.__currentIteration = 0
        self.__repository = repository()

    def iteration(self):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors
        self.__repository.getPopulation().evaluate()
        self.__repository.getPopulation().selection(int(Util.populationSize / 0.75))
        self.__repository.getPopulation().extendPopulation()

    def getMap(self):
        return self.__repository.cmap

    def run(self):
        # args - list of parameters needed in order to run the algorithm

        # until stop condition
        #    perform an iteration
        #    save the information need it for the statistics

        # return the results and the info for statistics
        fitnesses = []
        while self.__stopCondition():
            self.iteration()
            self.__currentIteration += 1
            fitnesses.append(self.__repository.getPopulation().averageFitness())
        return self.__repository.getPopulation(), fitnesses

    def solver(self):
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics
        self.__repository.createPopulation(
            args=[Util.populationSize,
                  Util.individualSize
                  ]
        )

        return self.run()

    def load(self, val):
        if val == "random":
            self.__repository.initRandomMap()
        else:
            self.__repository.loadFile(fileName=val)

    def __stopCondition(self):
        if self.__currentIteration != Util.maxIterations or \
                self.__repository.getPopulation().getIndividuals()[0].fitness() == self.__repository.cmap.nrZeroes():
            return True
        return False
