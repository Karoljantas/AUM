import random  
import numpy as np  

#wymiary kontenera
W, H = 10, 10  
#pole kontenera
container_area = W * H 
#lista pudelek (pusta)
box_dimensions = [] 

#funkcja ktora z pliku wczytuje baze danych (pudelka o okreslonych rozmiarach)
with open('m1a.txt', 'r') as file:
    width = None
    for line in file:
        values = line.strip().split()
        for value in values:
            dimension = int(value)  
            if width is None:
                width = dimension  
            else:
                height = dimension 
                box_dimensions.append((width, height)) 
                width = None 
#wyswietlenie wczytanych pudelek ()
#print(box_dimensions)

#funkcja ktora sprawdza czy dane pudelko mozna umiescic w okreslonym miejscu (x,y) w naszym kontenerze
def can_place_box(box, position, packed_boxes):
    #szerokosc i wysokosc pudelka
    w, h = box 
    #pozycja pudelka w kontenerze (x,y)
    x, y = position
    #sprawdzenie czy pudelko miesci sie w kontenerze
    if x + w > W or y + h > H:
        #jesli warunek jest spelniony to znaczy ze pudelko sie nie miesci w granicach kontenera -- zwracamy False
        return False 
    #sprawdzenie w petli czy nasze pudelko nie zachodzi na inne pudelka, ktore juz sa zapakowane w packed_boxes
    for other_box, other_pos in packed_boxes:
        #przypisanie wymiarow sprawdzanego pudelka (zapakowanego)
        other_w, other_h = other_box
        #przypisanie pozycji sprawdzanego pudelka (zapakowanego)
        other_x, other_y = other_pos
        if not (x + w <= other_x or x >= other_x + other_w or y + h <= other_y or y >= other_y + other_h):
            #jesli warunek nie jest spelniony to nasze pudelko nachodzi na inne pudelka -- zwaracmy False
            return False 
    return True

#funkcja ktora ocena dane rozmieszczenie pudelek pod katem liczby zapakowanych pudelek oraz miejsca ktore zajmuja
def evaluate_solution(solution):
    #inicjalizacja pustych pudelek oraz zajetej przez nich przestrzeni (0)
    packed_boxes = []  
    total_area = 0  
    #petla ktora przechodzi przez wszystkie pudelka i ich rozmieszczenia w zmiennej solution
    for box, position in solution:
        #sprawdzenie czy okreslone pudelko mozna zapakowac w danym miejscu
        if can_place_box(box, position, packed_boxes):
            #jesli tak to dodajemy pudelko do zmiennej packed_boxes
            packed_boxes.append((box, position)) 
            #aktualizujemy calkowite pole zajmowane przez pudelka (obliczamy pole dodanego przed chwila pudelka i dodajemy do zmiennej total_area)
            total_area += box[0] * box[1]
    #zwracamy liczbe umieszczonych pudelek w kontenerze oraz calkowita przestrzen ktora one zajmuja -- sa to dwa parametry ktore algorytm ma za zadanie maksymalizowac
    return len(packed_boxes), total_area

#generowanie poczatkowego, losowego rozwiazania
def generate_random_solution():
    #inicjalizacja pustego rozwiazania ()
    solution = []
    for box in box_dimensions:
        #wybranie losowej pozycji x danego pudelka
        x = random.randint(0, W - box[0])  
        #wybranie losowej pozycji y danego pudelka
        y = random.randint(0, H - box[1])  
        #dodanie pudelka do rozwiazania
        solution.append((box, (x, y)))  
    return solution

#operator genetyczny -- funkcja mutacji, ktora najpierw wybiera losowe pudelko a nastepnie w losowy sposob okresla jego nowa pozycje (koordynaty)
def mutate(solution):
    #okreslenie szansy na mutacje (domyslnie mniej niz 10%)
    if random.random() < 0.1:
        #losowanie indeksu pudelka, ktorego polozenie zostanie zmienione
        index = random.randint(0, len(solution) - 1)  # Losowy indeks pudelka do zmutowania
        #wybranie tego wylosowanego pudelka
        box = solution[index][0]  
        #wybranie nowej losowej pozycji x wylosowanego pudelka
        x = random.randint(0, W - box[0])  
        #wybranie nowej losowej pozycji y wylosowanego pudelka
        y = random.randint(0, H - box[1]) 
        #mutowanie pudelka -- podmienienie jego wspolrzednych w solution
        solution[index] = (box, (x, y))  # Zmutuj pudelko

#algorytm genetyczny -- zlozenie wszystkich funkcji w calosc
def genetic_algorithm(population_size=100, generations=1000):
    #stworzenie poczatkowej populacji losowych rozwiazan
    population = [generate_random_solution() for _ in range(population_size)] 
    #inicjalizacja zmiennej przechowujacej najlepsze rozwiazanie
    best_solution = None  
    #inicjalizacja zmiennej przechowujacej najlepszy wynik dopasowania (liczba pudelek w kontenerze, calkowite pole zajmowane przez pudelka)
    best_fitness = (-1, -1)  
    #petla po kolejnych generacjach (pokoleniach)
    for generation in range(generations):  # Petla iterujaca po kolejnych pokoleniach
        #ocena pod katem liczby pudelek oraz calkowitego pola, kazdego mozliwego rozwiazania w populacji
        #stworzenie tablicy fitnesses przechowujacej informacje o liczbie pudelek oraz calkowitym zajmowanym polu
        fitnesses = [evaluate_solution(ind) for ind in population] 

        #wybranie najlepszego rozwiazania z tablicy fitness
        for ind, fitness in zip(population, fitnesses):  # Iteracja po populacji i odpowiadajacym jej wynikom fitness
            #jesli nowa liczba pudelek jest wieksza lub rowna najlepszemu dotychczasowemu wynikowi
            if fitness[0] >= best_fitness[0]:
                #jesli nowa zajeta powierzchnia jest wieksza lub rowna najlepszemu dotychczasowemu wynikowi
                if fitness[1] >= best_fitness[1]:
                    #to znaczy ze znalezlismy lepsze rozwiazanie wiec je aktualizujemy
                    best_solution = ind 
                    #aktualizacja najlepszego wyniku (liczba pudelek, zajmowany obszar)
                    best_fitness = fitness 

        #operator selekcji -- wybieranie rodzicow, na podstawie ich wynikow fitness (do mutacji)
        selected_parents = random.choices(population, weights=[f[0] + f[1] for f in fitnesses], k=population_size)  
        #budowanie nowej populacji przy wykorzystaniu mutacji, inicjalizacja nowej populacji
        new_population = []
        #petla po wybranych w procesie selekcji rodzicach
        for parent in selected_parents:
            #tworzenie kopii rodzica
            mutated_child = parent[:] 
            #mutowanie dziecka (kopii rodzica)
            mutate(mutated_child)  
            #dodanie zmutowanego dziecka do nowej populacji
            new_population.append(mutated_child) 
        #aktuaclizacja pupulacji
        population = new_population 
        #wyswietlenie informacji o aktualnej generacji i najelpszym uzyskanym dopasowaniu (wyniku)
        print(f'Generation {generation}: Best Fitness {best_fitness}')
    return best_solution, best_fitness

best_solution, best_fitness = genetic_algorithm()
print("Best fitness: ",best_fitness)

def packed_boxes(best_solution):
    packed_boxes = []  
    total_area = 0  
    for box, position in best_solution:
        if can_place_box(box, position, packed_boxes):
            packed_boxes.append((box, position)) 
            total_area += box[0] * box[1]
    return len(packed_boxes), total_area, packed_boxes

num_of_boxes, area, placed_boxes = packed_boxes(best_solution)


print("Packed boxes: ", placed_boxes)
