import osmnx as ox
import random
import matplotlib.pyplot as plt
import time
from shortest_path import shortest_path
from simulation import estimate_time
from config import CAR_BASE_SPEED, BIKE_BASE_SPEED
from shapely.geometry import LineString
import geopandas as gpd
import logging
logger = logging.getLogger(__name__)
_reverse_cache: dict[tuple[float, float], str] = {}


def node_to_address(G, node: int, pause_s: float = 1.0) -> str:
    lon = float(G.nodes[node]["x"])
    lat = float(G.nodes[node]["y"])

    key = (round(lat, 6), round(lon, 6))
    if key in _reverse_cache:
        return _reverse_cache[key]

    try:
        info = ox.geocoder.geocode_to_gdf((lat, lon), reverse=True)
        addr = str(info["display_name"].iloc[0])
    except Exception:
        addr = f"{lat:.6f}, {lon:.6f}"

    _reverse_cache[key] = addr
    time.sleep(pause_s)
    return addr


def main(G, lights, plotting: bool = False, start: int | None = None, end: int | None = None) -> tuple[float, float]:
    nodes_list = list(G.nodes)
    start = random.choice(nodes_list) if start is None else start
    end = random.choice(nodes_list) if end is None else end

    print(f"WYLOSOWANY START: {start}")
    print(f"WYLOSOWANY KONIEC: {end}")

    # --- POWRÓT ADRESÓW ---
    print("START (adres):", node_to_address(G, start))
    print("KONIEC (adres):", node_to_address(G, end))
    logging.info(f"start = {start}\nend = {end}")

    try:
        route, route_length = shortest_path(G, start, end)
    except Exception as e:
        logging.warning(f"nie ma drogi między punktami: {e}")
        return (float("inf"), float("inf"))

    print(f"DŁUGOŚĆ TRASY: {route_length:.1f} m ({route_length / 1000:.2f} km)")
    logging.info(f"Odległość [m]: {route_length}")

    # --- LOGIKA OPÓŹNIEŃ NA WĘZŁACH ---
    num_intersections = len(route) - 2 if len(route) > 2 else 0
    car_node_delay = 0.0
    bike_node_delay = 0.0

    if num_intersections > 0:
        for _ in range(num_intersections):
            car_node_delay += random.uniform(3, 5)
            bike_node_delay += random.uniform(2, 4)


    # --- SYMULACJA CZASU (Z ROZBICIEM NA SKŁADOWE) ---
    car_stats = estimate_time(G, route, CAR_BASE_SPEED, "car", 0)
    bike_stats = estimate_time(G, route, BIKE_BASE_SPEED, "bike", 0)

    # Wyświetlanie dodatkowych informacji o korkach i parkowaniu
    print(f"\nSZCZEGÓŁY SAMOCHÓD:")
    print(f" - Czas w korkach: {car_stats['congestion']:.2f} s")
    print(f" - Czas parkowania: {car_stats['parking']:.2f} s")
    print(f" - Czas na skrzyżowaniach: {car_node_delay:.2f} s")
    print(f" - Czysty czas przejazdu: {car_stats['travel']:.2f} s")

    print(f"\nSZCZEGÓŁY ROWER:")
    print(f" - Czas spowolnień (korki): {bike_stats['congestion']:.2f} s")
    print(f" - Czas parkowania: {bike_stats['parking']:.2f} s")
    print(f" - Czas na skrzyżowaniach: {bike_node_delay:.2f} s")
    print(f" - Czysty czas przejazdu: {bike_stats['travel']:.2f} s\n")

    # CAŁKOWITY CZAS
    car_total_time = car_stats['total'] + car_node_delay
    bike_total_time = bike_stats['total'] + bike_node_delay

    print(f"ŁĄCZNY CZAS AUTA: {car_total_time:.2f} s")
    print(f"ŁĄCZNY CZAS ROWERU: {bike_total_time:.2f} s")

    if car_total_time < bike_total_time:
        logging.info("Samochód wygrywa")
        print("SAMOCHÓD WYGRYWA!")
    else:
        logging.info("Rower wygrywa")
        print("ROWER WYGRYWA!")

    logging.info(f"Auto: {round(car_total_time, 1)} s = {round(car_total_time / 60, 2)} min")
    logging.info(f"Rower: {round(bike_total_time, 1)} s = {round(bike_total_time / 60, 2)} min")

    if plotting:
        fig, ax = ox.plot_graph(G, show=False, close=False)
        ox.plot_graph_route(G, route, ax=ax, route_color="red", route_linewidth=3, show=False, close=False)
        ax.scatter(G.nodes[start]["x"], G.nodes[start]["y"], c="green", s=80)
        ax.scatter(G.nodes[end]["x"], G.nodes[end]["y"], c="blue", s=80)
        plt.show()

    return (car_total_time, bike_total_time)


if __name__ == "__main__":
    miasto = "Poland, Gorzów Wielkopolski"
    logging.info(f"Pobieranie mapy miasta {miasto.split(',')[1].strip()}")
    ox.settings.use_cache = True # przyśpiesza to działanie kodu

    ## nie usuwać ↓
    G = ox.graph_from_place(miasto, network_type="drive", simplify=True)
    lights = ox.features_from_place(
        miasto,
        tags={"highway": "traffic_signals"}
    )
    lights = lights.to_crs(G.graph["crs"])
    ## nie usuwać ↑


    # import csv
    # simulation_times = []
    # for x in range(100):
    #     simulation_times.append(main(G, lights, plotting=False))
    # with open(f"{miasto.split(',')[1].strip()}.csv", "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["car_time_s", "bike_time_s", "did_car_won"])
    #     for car_time, bike_time in simulation_times:
    #         writer.writerow([car_time, bike_time, car_time>bike_time])
    # exit()

    # dla wrocławia
    main(G, lights, plotting=True)

    # losowy jeden przypadek:
    # main(G, lights, plotting=True)