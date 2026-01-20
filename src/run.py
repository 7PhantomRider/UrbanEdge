import pandas as pd
import random
import osmnx as ox
import config #nadpis zmiennych z configu
from shortest_path import shortest_path
from main import count_lights_on_route, estimate_time
from shapely.geometry import Point
import logging

#logi off dla osmnx
logging.getLogger().setLevel(logging.ERROR)

#Simulation
MIASTO = "Poland, Wrocław"
N_ITERATIONS = 50  # i to bedzie razy 6 

#Plan
SCENARIUSZE = {
    "OFF_PEAK": { #poza szczytem
        "traffic_min": 0, "traffic_max": 0.5,
        "parking_car": 0.02, "parking_bike": 0.2 #duza lambda = szybko
    },
    "PEAK": { #szczyt
        "traffic_min": 2, "traffic_max": 4,
        "parking_car": 0.0015, "parking_bike": 0.1 #mała lambda = wolno
    }
}

DYSTANSE = {
    "SHORT": (200, 2000),    # < 2km
    "MEDIUM": (2000, 5000),  # 2-5km
    "LONG": (5000, 12000)    # > 5km
}

def get_random_nodes_dist(G, min_d, max_d):
    nodes = list(G.nodes(data=True))
    while True:
        u = random.choice(nodes)
        v = random.choice(nodes)
        p1 = Point(u[1]['x'], u[1]['y'])
        p2 = Point(v[1]['x'], v[1]['y'])
        #1 stopień to ok. 111km. Przybliżenie przelicznika bo obliczanie odległości geodezyjnej jest czasochłonne
        dist = p1.distance(p2) * 111000 
        if min_d <= dist <= max_d:
            return u[0], v[0]

def run():
    print(f"1. Pobieranie mapy miasta: {MIASTO}...")
    ox.settings.use_cache = True
    G = ox.graph_from_place(MIASTO, network_type="drive", simplify=True)
    lights = ox.features_from_place(MIASTO, tags={"highway": "traffic_signals"})
    lights = lights.to_crs(G.graph["crs"])
    print("   Mapa pobrana.")

    results = []
    total_steps = len(DYSTANSE) * len(SCENARIUSZE) * N_ITERATIONS
    current_step = 0

    print("2. Symulacja...")
    
    for dist_name, (d_min, d_max) in DYSTANSE.items():
        for scen_name, params in SCENARIUSZE.items():
            
            #NADPIS
            config.TRAFFIC_DELAY_MIN = params["traffic_min"]
            config.TRAFFIC_DELAY_MAX = params["traffic_max"]
            config.PARKING_LAMBDA_CAR = params["parking_car"]
            config.PARKING_LAMBDA_BIKE = params["parking_bike"]
            #tu jeszcze -> auto w szczycie jedzie wolniej
            if scen_name == "PEAK":
                config.CAR_BASE_SPEED = 25
            else:
                config.CAR_BASE_SPEED = 50

            for i in range(N_ITERATIONS):
                current_step += 1
                if current_step % 10 == 0:
                    print(f" postęp: {current_step}/{total_steps} (cat: {dist_name}, scenario: {scen_name})")

                try:
                    start, end = get_random_nodes_dist(G, d_min, d_max)
                    route, length = shortest_path(G, start, end)
                    
                    if length == float('inf'): continue

                    n_lights = count_lights_on_route(G, route, lights)
                    
                    car_time = estimate_time(G, route, config.CAR_BASE_SPEED, "car", n_lights)
                    bike_time = estimate_time(G, route, config.BIKE_BASE_SPEED, "bike", n_lights)
                    
                    results.append({
                        "distance_cat": dist_name,
                        "scenario": scen_name,
                        "distance_m": length,
                        "n_lights": n_lights,
                        "car_time_s": car_time,
                        "bike_time_s": bike_time,
                        "diff_time": car_time - bike_time,
                        "winner": "Bike" if bike_time < car_time else "Car"
                    })
                except Exception as e:
                    print(f"błąd w iteracji: {e}")
                    continue

    #csv
    df = pd.DataFrame(results)
    filename = "wyniki_symulacji.csv"
    df.to_csv(filename, index=False)
    print(f"\n3. Ready, dane zapisane w pliku: {filename}")

if __name__ == "__main__":
    run()