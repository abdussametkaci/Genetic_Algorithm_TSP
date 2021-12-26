import random

from City import City
from Utils import distance


class Individual:
    def __init__(self, chromosome: list[City], start_point: int, init=True):
        self.__fitness = 0  # total distance of travel represented by the order of cities
        self.__chromosome = chromosome  # list of city
        self.__start_point = start_point    # start city
        if init:
            self.__initialize_chromosome()

    # calculate fitness value
    def evaluate(self):
        self.__fitness = 0
        length = len(self.__chromosome)
        for i in range(length):
            self.__fitness += distance(self.__chromosome[i % length], self.__chromosome[(i + 1) % length])
        return self.__fitness

    # generate random solution
    def __initialize_chromosome(self):
        random_cities = self.__chromosome[:self.__start_point] + self.__chromosome[self.__start_point + 1:]
        random.shuffle(random_cities)
        random_cities.insert(0, self.__chromosome[self.__start_point])
        self.__chromosome = random_cities

    def get_fitness(self):
        return self.__fitness

    def get_start_point(self):
        return self.__start_point

    def print_chromosome(self):
        for i in self.__chromosome:
            print(i, end=" ")
        print(f"[fitness: {self.evaluate()}]", end=" ")
        print()

    def get_chromosome(self):
        return self.__chromosome

    def set_chromosome(self, chromosome):
        self.__chromosome = chromosome
