#!/usr/bin/env python3
import csv
import sys

def calculate_averages(csv_file):
    car_times = []
    bike_times = []
    car_wins = 0
    bike_wins = 0
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            car_time = float(row['car_time_s'])
            bike_time = float(row['bike_time_s'])
            
            car_times.append(car_time)
            bike_times.append(bike_time)
            
            if row['did_car_won'] == 'True':
                car_wins += 1
            else:
                bike_wins += 1
    
    total = len(car_times)
    avg_car = sum(car_times) / total
    avg_bike = sum(bike_times) / total
    
    print(f"Analiza pliku: {csv_file}")
    print(f"Liczba symulacji: {total}")
    print(f"\nŚredni czas samochodu: {avg_car:.2f} s ({avg_car/60:.2f} min)")
    print(f"Średni czas roweru: {avg_bike:.2f} s ({avg_bike/60:.2f} min)")
    print(f"\nSamochód wygrał: {car_wins} razy ({car_wins/total*100:.1f}%)")
    print(f"Rower wygrał: {bike_wins} razy ({bike_wins/total*100:.1f}%)")
    
    var_car = sum((x - avg_car) ** 2 for x in car_times) / total
    var_bike = sum((x - avg_bike) ** 2 for x in bike_times) / total
    
    print(f"\nWariancja czasu samochodu: {var_car:.2f}")
    print(f"Wariancja czasu roweru: {var_bike:.2f}")
    
    if avg_car < avg_bike:
        diff = avg_bike - avg_car
        print(f"\nSamochód jest średnio szybszy o {diff:.2f} s ({diff/60:.2f} min)")
    else:
        diff = avg_car - avg_bike
        print(f"\nRower jest średnio szybszy o {diff:.2f} s ({diff/60:.2f} min)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = "Wrocław.csv"
    
    calculate_averages(csv_file)
