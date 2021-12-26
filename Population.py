from City import City
from Individual import Individual


class Population:
    def __init__(self, population_size: int, cities: list[City], start_point: int):
        self.__population_size = population_size
        self.__individuals = []   # solutions
        self.__cities = cities
        self.__start_point = start_point - 1  # city index start 1, not 0

    # product solutions
    def initialize(self):
        self.__individuals = [Individual(self.__cities, self.__start_point) for _ in range(self.__population_size)]

    # calculate fitness values of all individuals
    def evaluate(self):
        for i in self.__individuals:
            i.evaluate()

    def print_population(self):
        for i in self.__individuals:
            i.print_chromosome()

    def get_individuals(self):
        return self.__individuals

    # select best n solutions
    def select_parents(self, parent_count=2) -> list[tuple[Individual, Individual]]:
        def pairwise(individuals):
            return [(x, y) for x, y in zip(individuals[::2], individuals[1::2])]
        return pairwise(sorted(self.__individuals, key=lambda i: i.get_fitness())[:parent_count])    # best n individual

    # remove worst n individual and add children
    def survivor_children(self, children):
        worst_individuals = sorted(self.__individuals, key=lambda p: p.get_fitness())[-len(children):]    # worst n individual
        for (i, c) in enumerate(children):
            index = self.__individuals.index(worst_individuals[i])
            self.__individuals[index] = c
