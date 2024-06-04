import random  
import numpy as np  

#Wymiary kontenera
W, H = 50, 50  # Okreslenie wymiarow kontenera
container_area = W * H  # Obliczenie calkowitej powierzchni kontenera

box_dimensions = []  # Inicjalizacja pustej listy na wymiary pudelek

# Otwarcie pliku 'm3e.txt' do odczytu
with open('m3e.txt', 'r') as file:
    width = None
    # Iteracja przez kazda linie w pliku
    for line in file:
        # Podzielenie linii na poszczegolne wartosci i usuniecie bialych znakow
        values = line.strip().split()
        for value in values:
            dimension = int(value)  # Konwersja wartosci na liczbe calkowita
            if width is None:
                width = dimension  # Jesli szerokosc jeszcze nie zostala ustawiona, ustaw ja
            else:
                height = dimension  # W przeciwnym razie ustaw wysokosc
                box_dimensions.append((width, height))  # Dodaj pudelko do listy wymiarow pudelek
                width = None  # Zresetuj szerokosc na kolejna iteracje

print(box_dimensions)  # Wydrukuj wymiary pudelek

# Funkcja pomocnicza do sprawdzania, czy pudelko moze byc umieszczone na danej pozycji
def can_place_box(box, position, packed_boxes):
    w, h = box  # Szerokosc i wysokosc pudelka
    x, y = position  # Pozycja pudelka
    if x + w > W or y + h > H:
        return False  # Pudelko wychodzi poza granice kontenera
    for other_box, other_pos in packed_boxes:
        other_w, other_h = other_box
        other_x, other_y = other_pos
        if not (x + w <= other_x or x >= other_x + other_w or y + h <= other_y or y >= other_y + other_h):
            return False  # Pudelka zachodza na siebie
    return True

# Funkcja do oceny rozwiazania
def evaluate_solution(solution):
    packed_boxes = []  # Lista umieszczonych pudelek
    total_area = 0  # Calkowita powierzchnia zajeta przez pudelka
    for box, position in solution:
        if can_place_box(box, position, packed_boxes):
            packed_boxes.append((box, position))  # Dodaj pudelko do listy umieszczonych pudelek
            total_area += box[0] * box[1]  # Dodaj powierzchnie pudelka do calkowitej powierzchni
    return len(packed_boxes), total_area  # Zwroc liczbe umieszczonych pudelek i calkowita zajeta powierzchnie

# Generowanie poczatkowego losowego rozwiazania
def generate_random_solution():
    solution = []  # Inicjalizacja pustego rozwiazania
    for box in box_dimensions:
        x = random.randint(0, W - box[0])  # Losowy x
        y = random.randint(0, H - box[1])  # Losowy y
        solution.append((box, (x, y)))  # Dodaj pudelko z losowa pozycja do rozwiazania
    return solution

# Operator mutacji
def mutate(solution):
    if random.random() < 0.1:  # Szansa mutacji
        index = random.randint(0, len(solution) - 1)  # Losowy indeks pudelka do zmutowania
        box = solution[index][0]  # Wybierz pudelko
        x = random.randint(0, W - box[0])  # Nowe losowe x
        y = random.randint(0, H - box[1])  # Nowe losowe y
        solution[index] = (box, (x, y))  # Zmutuj pudelko

# Algorytm genetyczny
def genetic_algorithm(population_size=100, generations=1000):
    # Inicjalizacja populacji
    population = [generate_random_solution() for _ in range(population_size)]  # Generowanie poczatkowej populacji losowych rozwiazań
    best_solution = None  # Inicjalizacja zmiennej przechowujacej najlepsze rozwiazanie
    best_fitness = (-1, -1)  # Inicjalizacja zmiennej przechowujacej najlepszy wynik fitness

    for generation in range(generations):  # Petla iterujaca po kolejnych pokoleniach
        # Ocena fitnessu
        fitnesses = [evaluate_solution(ind) for ind in population]  # Ocena fitnessu dla kazdego rozwiazania w populacji

        # Wybierz najlepsze rozwiazanie
        for ind, fitness in zip(population, fitnesses):  # Iteracja po populacji i odpowiadajacym jej wynikom fitness
            if fitness[0] >= best_fitness[0]:  # Jesli liczba pudelek jest wieksza lub rowna najlepszemu dotychczasowemu wynikowi
                if fitness[1] >= best_fitness[1]:  # Jesli zajeta powierzchnia jest wieksza lub rowna najlepszemu dotychczasowemu wynikowi
                    best_solution = ind  # Aktualizacja najlepszego rozwiazania
                    best_fitness = fitness  # Aktualizacja najlepszego wyniku fitness

        # Selekcja
        selected_parents = random.choices(population, weights=[f[0] + f[1] for f in fitnesses], k=population_size)  # Wybor rodzicow na podstawie ich wynikow fitness

        # Mutacja i budowanie nowej populacji
        new_population = []  # Inicjalizacja nowej populacji
        for parent in selected_parents:  # Iteracja po wybranych rodzicach
            mutated_child = parent[:]  # Kopia rodzica
            mutate(mutated_child)  # Mutacja dziecka
            new_population.append(mutated_child)  # Dodanie zmutowanego dziecka do nowej populacji

        population = new_population  # Aktualizacja populacji na nowa populacje

        print(f'Generation {generation}: Best Fitness {best_fitness}')  # Wydruk informacji o aktualnym pokoleniu i najlepszym wyniku fitness

    return best_solution, best_fitness  # Zwrocenie najlepszego rozwiazania i jego wyniku fitness


