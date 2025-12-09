# Przygotowania
Aby uruchomić program wpierw trzeba pobrać wszystkie potrzebne biblioteki

*Opcjonalnie* można stworzyć to w środowisku wirtualnym
```sh
python3 -m venv env
source env/bin/activate
```

Obowiązkowym jest pobranie wszystkich potrzebnych bibliotek:

```sh
python3 -m pip install -r requirements.txt
```

## Uruchamianie programu:

```sh
python3 main.py
```

## Informacje o naszym środowisku

Sprawdziliśmy program w pythonie w wersji `3.13.5`, oraz w paczkach w następujących wersjach:

```
geopandas          1.1.1
matplotlib         3.10.7
networkx           3.6.1
numpy              2.3.5
osmnx              2.0.7
```

# Informacje o kodzie - jak uruchomić daną trasę

Aby zasymulować dokładną podróz możemy wpierw znaleźć ID nodów w openstreetmaps korzystając z funkcji "zoom in to query features", znaleziony node'y wstawiamy do funkcji main np. `main(G, lights, plotting=True, start = 3284135585, end = 151334702)`; najlepiej to zrobić w sekcji 'if __name__==\'__main__\'', tak aby nie uruchamiać tego przy imporcie kodu

uwaga: czasem jako output jest przypadek w którym podróż z miejsca a do B to nieskończoność, to znaczy że nie ma drogi między początkiem a końcem. Przy analizie danych trzeba przefiltrować tego typu przypadki -- one nie są dla nas przydatne.

### co jest jeszcze w `main.py`
na samym końcu jest kilka przykładowych wywołań programu:
- 100 losowych symulacji, wyniki są w pliku .csv
- predefiniowana ścieżka

## Zmiana parametrów symulacji
Zmiana jest możliwa w pliku `config.py`, więcej nie trzeba nic pisać, nazwy zmiennych są jasne i czytelne.

## `simulation.py`

To własnie w tym pliku symulujemy czas podróży, korzystamy w znaczym stopniu tam funkcji wbudowanych w numpy; korzystamy tam z parametrów `config.py`

## `shortest_path.py`

Dijkstra

## `count_lights_on_route` w `main.py`

Liczymy światła 2.5m od każdej krawędzi

czemu 2.5? wydaje się bardzo dobrym przybliżeniem, prawie że nie widziałem false positive'ów podczas analizy tras

# Przydatne informacje
- w przypadku remisu wygrywa rower
- proszę uważać na to że przejazdy [mogą mieć nieskończoną długość](#informacje-o-kodzie---jak-uruchomić-specjalnie-trasę-modyfikować)
