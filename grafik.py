'''
Plik dane.csv zawiera dane zbierane na węźle ciepłowniczym przez
przedsiębiorstwo dostarczające ciepło do budynku (patrz opisy kolumn w pliku).
Napisać skrypt w języku Python, dokonujący podstawowej analizy tych danych.
'''

# A. Wczytanie obserwacji dla wybranych zmiennych.
# B. Sprawdzenie podstawowych statystyk dla poszczególnych zmiennych. Wykreślenie histogramów.
# C. Identyfikacja zmiennych, w których występują potencjalnie błędne dane (obserwacje) lub braki danych. Naprawa danych.
# D. Obliczenie unormowanych korelacji pomiędzy poszczególnymi zmiennymi.
# E. Przeprowadzenie regresji liniowej dla wybranych zmiennych, wraz z wykresami.
# F. Wykorzystanie wyników regresji dla podstawowej predykcji wyników.

import csv, numpy as np, matplotlib.pyplot as plt

przeplyw = []
temp_zasilania = []
temp_powrotu = []
roznica_temp = []
moc = []

plik = open("dane.csv", "rt")
dane = csv.reader(plik)

next(dane)

for obserwacja in dane:
    przeplyw.append(float(obserwacja[6]))
    temp_zasilania.append(float(obserwacja[7]))
    temp_powrotu.append(float(obserwacja[8]))
    roznica_temp.append(float(obserwacja[9]))
    moc.append(float(obserwacja[12]))
    
print(przeplyw)

plik.close()

zmienne = {"Przeplyw":przeplyw,
           "Temperatura zasilania":temp_zasilania,
           "Temperatura powrotu":temp_powrotu,
           "Roznica temperatur":roznica_temp,
           "Moc":moc
           }

for nazwa, zmienna in zmienne.items():
    print("Zmienna:", nazwa)
    print("min = ", min(zmienna))
    print("max = ", max(zmienna))
    print("srednia = ", np.mean(zmienna))
    print("mediana = ", np.median(zmienna))
    print("zakres = ", np.ptp(zmienna))
    print("odch. std = ", np.std(zmienna))
    print("wariancja = ", np.var(zmienna))
    print("histogram = ", np.histogram(zmienna))
    plt.hist(zmienna,10)
    plt.show()
    print()

zmienna_naprawa = {"Przeplyw":przeplyw,
                   "Roznica temperatur":roznica_temp,
                   "Moc":moc}

for nazwa, zmienna in zmienna_naprawa.items():
    for i, wartosc in enumerate(zmienna):
        if wartosc > 10000:
            print("Anomalia", nazwa, "pod indeksem", i)
            zmienna[i] = np.median(zmienna)
            
print("Statystyki po naprawie")
for nazwa, zmienna in zmienna_naprawa.items():
    print("Zmienna:", nazwa)
    print("min = ", min(zmienna))
    print("max = ", max(zmienna))
    print("srednia = ", np.mean(zmienna))
    print("mediana = ", np.median(zmienna))
    print("zakres = ", np.ptp(zmienna))
    print("odch. std = ", np.std(zmienna))
    print("wariancja = ", np.var(zmienna))
    print("histogram = ", np.histogram(zmienna))
    plt.hist(zmienna,10)
    plt.show()
    print()
            
def korelacja_unormowana(a,b):
    a = (a - np.mean(a))/(np.std(a)*len(a))
    b = (b - np.mean(b))/(np.std(b))
    return np.correlate(a, b)

for nazwa1, zmienna1 in zmienne.items():
    for nazwa2, zmienna2 in zmienne.items():
        print("Korelacja miedzy {} a {} wynosi {}".format(nazwa1, nazwa2, korelacja_unormowana(zmienna1, zmienna2)))
        
plt.plot(moc, przeplyw,".")
a,b = np.polyfit(moc,przeplyw,1)
print("Wzor prostej: y = {}*x + {}".format(a, b))

yregrecja = [a*i + b for i in moc]
plt.plot(moc,yregrecja)
plt.show()

moc1 = input("Podaj moc = ")
przeplyw1 = a*float(moc1) + b
print("Przepływ = ", round(przeplyw1, 2), "l/min")
