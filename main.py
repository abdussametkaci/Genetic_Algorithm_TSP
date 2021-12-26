import random
import Utils
from Individual import Individual
from Population import Population
import matplotlib.pyplot as plt


def main():
    analysis_enabled = True    # if variable set as True, a graph is shown
    results = []    # analysis results
    cities = Utils.get_cities('data/Cities_Coordinates.tsp')    # get all cities
    population_size = 150
    generation_size = 5000
    start_city = 28
    parent_count = 16
    population = Population(population_size, cities, start_city)
    population.initialize()
    population.evaluate()
    print("current population")
    population.print_population()

    termination = 0     # termination condition
    while termination < generation_size:
        parents = population.select_parents(parent_count)   # select n parent, n must be even
        children = []   # new solutions
        for (p1, p2) in parents:
            child1, child2 = cross_over(p1, p2)     # product children with cross over
            # mutation
            swap_mutation(child1)
            swap_mutation(child2)
            # evaluate children
            child1.evaluate()
            child2.evaluate()
            # add children to list
            children.append(child1)
            children.append(child2)

        # remove n worst solution from population and add new solutions (children)
        population.survivor_children(children)

        # if enabled analysis, the best result is added to results list
        if analysis_enabled:
            results.append(min(population.get_individuals(), key=lambda i: i.get_fitness()).get_fitness())

        termination += 1

    print("last population")
    population.print_population()

    print("best solution: ")
    min(population.get_individuals(), key=lambda i: i.get_fitness()).print_chromosome()

    # if enabled analysis, draw graph
    if analysis_enabled:
        plt.plot(results)
        plt.xlabel("Generation")
        plt.ylabel("Distance")
        plt.show()


def cross_over(parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
    # get chromosome of parents
    chromosome1: list = parent1.get_chromosome()[:]
    chromosome2: list = parent2.get_chromosome()[:]
    # define children chromosome
    child_chromosome1 = []
    child_chromosome2 = []
    # define invalid cities
    invalid_values1 = []
    invalid_values2 = []
    for i in range(len(chromosome1)):
        if random.random() >= 0.5:
            value1, value2 = chromosome1[i], chromosome2[i]     # get gene
            # cities are unique, so if gene is in child chromosome, it is invalid
            if value1 in child_chromosome1:
                invalid_values1.append(value1)
            if value2 in child_chromosome2:
                invalid_values2.append(value2)
            child_chromosome1.append(value1)
            child_chromosome2.append(value2)
        else:
            value1, value2 = chromosome2[i], chromosome1[i]     # get gene crossly
            if value1 in child_chromosome1:
                invalid_values1.append(value1)
            if value2 in child_chromosome2:
                invalid_values2.append(value2)
            child_chromosome1.append(value1)
            child_chromosome2.append(value2)

    # find unused valid cities
    valid_cities1 = list(set(chromosome1) - set(child_chromosome1))
    valid_cities2 = list(set(chromosome2) - set(child_chromosome2))
    # then, put these cities into child chromosome
    for i in invalid_values1:
        child_chromosome1[child_chromosome1.index(i)] = valid_cities1.pop()
    for i in invalid_values2:
        child_chromosome2[child_chromosome2.index(i)] = valid_cities2.pop()
    return (Individual(child_chromosome1, parent1.get_start_point(), False),
            Individual(child_chromosome2, parent2.get_start_point(), False))


def swap_mutation(child: Individual):
    chromosome = child.get_chromosome()[:]
    start = random.randint(1, len(chromosome) // 2)
    end = random.randint(len(chromosome) // 2, len(chromosome) - 1)
    chromosome[start], chromosome[end] = chromosome[end], chromosome[start]
    child.set_chromosome(chromosome)


def scramble_mutation(child: Individual):
    chromosome = child.get_chromosome()[:]
    start = random.randint(1, len(chromosome) // 2)
    end = random.randint(len(chromosome) // 2, len(chromosome) - 1)
    selected_gene = chromosome[start: end]

    random.shuffle(selected_gene)

    chromosome = chromosome[:start] + selected_gene + chromosome[end:]
    child.set_chromosome(chromosome)


def insert_mutation(child: Individual):
    chromosome = child.get_chromosome()[:]
    start = random.randint(1, len(chromosome) // 2)
    end = random.randint(len(chromosome) // 2, len(chromosome) - 1)
    selected_gene = chromosome[start: end]

    for i in range(len(selected_gene) - 1, 1, -1):
        selected_gene[i], selected_gene[i - 1] = selected_gene[i - 1], selected_gene[i]

    chromosome = chromosome[:start] + selected_gene + chromosome[end:]
    child.set_chromosome(chromosome)


def inversion_mutation(child: Individual):
    chromosome = child.get_chromosome()[:]
    start = random.randint(1, len(chromosome) // 2)
    end = random.randint(len(chromosome) // 2, len(chromosome) - 1)
    selected_gene = chromosome[start: end]

    reversed_gene = list(reversed(selected_gene))

    chromosome = chromosome[:start] + reversed_gene + chromosome[end:]
    child.set_chromosome(chromosome)


if __name__ == '__main__':
    main()
