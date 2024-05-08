import random 

lista_pudelek = [
    (3, 3),
    (6, 5),
    (5, 8),
    (7, 2),
    (9, 7),
    (2, 4),
    (3, 1),
    (6, 6),
    (7, 4),
    (1, 2)
]

#kontener
wysokosc_kontenera = 14
szerokosc_kontenera = 10


def policz_pudelka_i_pole(pudelka):
    #liczba pudelek
    liczba_pudelek = len(pudelka)
    
    #laczne pole pudelek
    pola_pudelek = 0
    for pudelko in pudelka:
        wysokosc_pudelka, szerokosc_pudelka = pudelko
        pole = pudelko[0] * pudelko[1]
        pola_pudelek += pole
    
    return liczba_pudelek, pola_pudelek


#wymiana losowego pudelka z kontenera na pudelko poza kontenerem
def mutacja(pudelka_zawarte, pudelka_niezawarte, wysokosc_kontenera, szerokosc_kontenera):
    #losowanie pudelka z kontenera i dodanie go do listy pudelek poza kontenerem
    if pudelka_zawarte:
        pudelko_przeniesione = random.choice(pudelka_zawarte)
        pudelka_zawarte.remove(pudelko_przeniesione)
        pudelka_niezawarte.append(pudelko_przeniesione)
    
    #losowanie pudelka, które nie jest w kontenerze i umieszczenie go w kontenerze
    if pudelka_niezawarte:
        pudelko_do_umieszczenia = random.choice(pudelka_niezawarte)
        wysokosc_pudelka, szerokosc_pudelka = pudelko_do_umieszczenia
        #x = random.randint(0, szerokosc_kontenera - szerokosc_pudelka)
        #y = random.randint(0, wysokosc_kontenera - wysokosc_pudelka)
        #pozycja = (x, y)
        
        #sprawdzenie czy pudelko zmiesci sie do kontenera i czy nie wchodzi na inne pudelka
        #TODO: sprawdzic czy ten warunek dziala
        while not (
            x + szerokosc_pudelka <= szerokosc_kontenera and
            y + wysokosc_pudelka <= wysokosc_kontenera and
            all(not (
                p[0][0] < x + szerokosc_pudelka and
                p[1][0] > x and
                p[0][1] < y + wysokosc_pudelka and
                p[1][1] > y
            ) for p in pudelka_zawarte)
        ):
            x = random.randint(0, szerokosc_kontenera - szerokosc_pudelka)
            y = random.randint(0, wysokosc_kontenera - wysokosc_pudelka)
            pozycja = (x, y)
        
        #dodanie pudelka jesli warunek jest spelniony
        pudelka_zawarte.append((pozycja, (x + szerokosc_pudelka, y + wysokosc_pudelka)))
        
        # usuniecie pudelka
        pudelka_niezawarte.remove(pudelko_do_umieszczenia)

    return pudelka_zawarte, pudelka_niezawarte


# zamiana miejscami dwoch sasiadujacych pudelek w kontenerze
def crossover(pudelka_zawarte):
    #kopia pilsty zeby nie modyfikowac narazie oryginalu
    nowe_pudelka_zawarte = pudelka_zawarte[:]
    
    #czy conajmniej 2 pudelka w kontenerze
    if len(nowe_pudelka_zawarte) < 2:
        return nowe_pudelka_zawarte
    
    #losujemy indeks pudelka
    indeks_1 = random.randint(0, len(nowe_pudelka_zawarte) - 2)
    
    #indeks nastepnego pudelka
    indeks_2 = indeks_1 + 1
    
    # TODO: sprawdzenie czy zamiana miejscami wylosowanych pudelek jest mozliwa, czy nie beda na siebie nachodzic

    #zamiana miejscami
    nowe_pudelka_zawarte[indeks_1], nowe_pudelka_zawarte[indeks_2] = nowe_pudelka_zawarte[indeks_2], nowe_pudelka_zawarte[indeks_1]
    
    return nowe_pudelka_zawarte

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

