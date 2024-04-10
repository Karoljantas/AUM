import random 


def init_population(pop_size, box_width, box_height, num_items):
    population = []
    for _ in range(pop_size):
        individual = [box_width, box_height]  # Rozmiary pudełka na początek
        for _ in range(num_items):
            individual.append(random.randint(0, 1))  # Losowy wybór przedmiotu (1 - wybrany, 0 - niewybrany)
            if individual[-1] == 1:  # Jeśli przedmiot jest wybrany
                item_width, item_height = items[_][0], items[_][1]
                if random.random() < 0.5:  # 50% szans na obrócenie przedmiotu
                    item_width, item_height = item_height, item_width
                individual.append(item_width)  # Szerokość przedmiotu
                individual.append(item_height)  # Wysokość przedmiotu
            else:
                individual.extend([0, 0])  # Szerokość i wysokość nie mają znaczenia, gdy przedmiot nie jest wybrany
        population.append(individual)
    return population

# Funkcja krzyżowania: krzyżuje dwa osobniki w dwóch punktach
def crossover(ind1, ind2):
    crossover_point1 = random.randint(2, len(ind1) - 2)
    crossover_point2 = random.randint(crossover_point1 + 1, len(ind1) - 1)
    child1 = ind1[:crossover_point1] + ind2[crossover_point1:crossover_point2] + ind1[crossover_point2:]
    child2 = ind2[:crossover_point1] + ind1[crossover_point1:crossover_point2] + ind2[crossover_point2:]
    return child1, child2