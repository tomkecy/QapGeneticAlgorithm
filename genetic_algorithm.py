import numpy as np


class GeneticAlgorithm:
    def __init__(self, num_of_locations, pop_size, flow_matrix, distance_matrix, mutation_probability,
                 crossover_probability, tour, data_logger):
        self.__num_of_locations = num_of_locations
        self.__flow_matrix = flow_matrix
        self.__distance_matrix = distance_matrix
        self.__pop_size = pop_size
        self.__data_logger = data_logger
        self.__mutation_probability = mutation_probability
        self.__tour = tour
        self.__crossover_probability = crossover_probability

    def __generate_specimen(self):
        specimen = [i for i in range(1, self.__num_of_locations + 1)]
        np.random.shuffle(specimen)
        return specimen

    def initialise_population(self):
        population = np.array([self.__generate_specimen() for _ in range(0, self.__pop_size)])
        return population

    def evaluate(self, population):
        return np.array(
            [self.evaluate_specimen_fitness(specimen) for specimen in population]
        )

    def run(self, generations):
        current_generation = 1
        population = self.initialise_population()
        population_fitness = self.evaluate(population)
        current_best_index = np.argmin(population_fitness)
        current_best_specimen = population[current_best_index]
        current_best_fitness = population_fitness[current_best_index]
        global_best_specimen = current_best_specimen
        global_best_fitness = current_best_fitness

        self.__data_logger.write_log(current_generation, current_best_fitness, np.average(population_fitness), np.amax(population_fitness))

        while current_generation < generations:
            population = self.selection(population, population_fitness)
            population = self.crossover(population)
            self.mutation(population)

            population_fitness = self.evaluate(population)
            current_best_index = np.argmin(population_fitness)
            current_best_specimen = population[current_best_index]
            current_best_fitness = population_fitness[current_best_index]
            current_generation += 1
            self.__data_logger.write_log(current_generation, current_best_fitness, np.average(population_fitness),
                                         np.amax(population_fitness))

            if current_best_fitness < global_best_fitness:
                global_best_fitness = current_best_fitness
                global_best_specimen = current_best_specimen

        return global_best_specimen, global_best_fitness

    def evaluate_specimen_fitness(self, specimen):
        fitness_acc = 0
        for facility in range(0, len(specimen)):
            for other_facility in range(0, len(specimen)):
                if facility == other_facility:
                    continue
                fitness_acc += self.__flow(facility, other_facility) * self.__distance(specimen[facility],
                                                                                       specimen[other_facility])
        return fitness_acc

    def selection(self, population, population_fitness):
        selected_population = []
        for i in range(0, self.__pop_size):
            competitors_indices = [np.random.randint(0, len(population)) for _ in range(0, self.__tour)]
            best_competitor_index = np.argmin(population_fitness[competitors_indices])
            selected_population.append(population[best_competitor_index])

        return np.array(selected_population)

    def crossover(self, population):
        children = []

        for i in range(0, self.__pop_size):
            first_parent_index = np.random.randint(0, len(population))
            second_parent_index = np.random.randint(0, len(population))
            first_child, second_child = self.__specimens_crossover(population[first_parent_index],
                                                                   population[second_parent_index])
            children.extend([first_child, second_child])
        return np.array(children)

    def __distance(self, location, other_location):
        return self.__distance_matrix[location - 1, other_location - 1]

    def __flow(self, facility, other_facility):
        return self.__flow_matrix[facility, other_facility]

    def __specimens_crossover(self, first_parent, second_parent):
        if np.random.randint(0, 1) >= self.__crossover_probability:
            return first_parent, second_parent

        cross_point = np.random.randint(0, len(first_parent))

        first_child = np.append(first_parent[:cross_point], second_parent[cross_point:])
        self.__validate_and_fix_specimen(first_child)

        second_child = np.append(second_parent[:cross_point], first_parent[cross_point:])
        self.__validate_and_fix_specimen(second_child)

        return first_child, second_child

    def __validate_and_fix_specimen(self, specimen):
        if len(specimen) == len(set(specimen)):
            return
        not_found = list(range(1, len(specimen) + 1))
        duplicates_indices = []
        for facility in range(0, len(specimen)):
            if specimen[facility] not in not_found:
                duplicates_indices.append(facility)
                continue
            not_found.remove(specimen[facility])
        for i in duplicates_indices:
            specimen[i] = not_found[0]
            del not_found[0]

    def mutation(self, population):
        for specimen in population:
            if np.random.random() < self.__mutation_probability:
                first_index = np.random.randint(0, len(specimen))
                second_index = (first_index + np.random.randint(1, len(specimen))) % len(specimen)
                temp = specimen[first_index]
                specimen[first_index] = specimen[second_index]
                specimen[second_index] = temp


