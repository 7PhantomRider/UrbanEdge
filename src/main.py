import osmnx as ox
import random
import matplotlib.pyplot as plt

from shortest_path import shortest_path
from simulation import estimate_time
from config import CAR_BASE_SPEED, BIKE_BASE_SPEED
from shapely.geometry import LineString
import geopandas as gpd
import logging
logger = logging.getLogger(__name__)

def count_lights_on_route(G, route, lights_gdf, dist=2.5):
    # GDF to CRS
    coords = [(G.nodes[n]["x"], G.nodes[n]["y"]) for n in route]
    edges = [LineString((coords[i], coords[i + 1])) for i in range(len(coords) - 1)]
    edges_gs = gpd.GeoSeries(edges, crs=G.graph["crs"])

    utm_crs = edges_gs.estimate_utm_crs()
    edges_utm = edges_gs.to_crs(utm_crs)
    lights_utm = lights_gdf.to_crs(utm_crs)
    
    # Liczymy światła
    counted_lights = set()
    for edge_utm in edges_utm:
        for idx, light in lights_utm.iterrows():
            if idx not in counted_lights:
                if edge_utm.distance(light.geometry) < dist:
                    counted_lights.add(idx)
    
    return len(counted_lights)



def main(G, lights, plotting:bool=False, start:int|None=None, end:int|None=None) -> tuple[float, float]:
    nodes = list(G.nodes)
    start = random.choice(nodes) if start==None else start
    end = random.choice(nodes) if end==None else end
    logging.info(f"start = {start}\nend = {end}")


    try:
        route, route_length = shortest_path(G, start, end)
    except Exception as e:
        logging.warning("nie ma drogi między punktami", e)
        return (float("inf"), float("inf"))


    logging.info("Odległość [m]:", route_length)

    # liczba świateł na trasie (w promieniu <dist> m)
    n_lights = count_lights_on_route(G, route, lights, dist=2.5)
    logging.info("Liczba świateł na trasie:", n_lights)

    car_time = estimate_time(G, route, CAR_BASE_SPEED, "car", n_lights)
    bike_time = estimate_time(G, route, BIKE_BASE_SPEED, "bike", n_lights)

    if car_time < bike_time:
        logging.info("Samochód wygrywa")
    else:
        logging.info("Rower wygrywa")


    logging.info("Auto:", round(car_time, 1), "s =", round(car_time / 60, 2), "min")
    logging.info("Rower:", round(bike_time, 1), "s =", round(bike_time / 60, 2), "min")

    # rysowanie
    if plotting:
        fig, ax = ox.plot_graph(G, show=False, close=False)
        ox.plot_graph_route(G, route, ax=ax, route_color="red", route_linewidth=3, show=False, close=False)

        # start i end point są kolorowane
        ax.scatter(G.nodes[start]["x"], G.nodes[start]["y"], c="green", s=80)
        ax.scatter(G.nodes[end]["x"], G.nodes[end]["y"], c="blue", s=80)
        
        # światła
        ax.scatter(lights.geometry.x, lights.geometry.y, c="yellow", s=20)

        plt.show()

    return (car_time, bike_time)


if __name__ == "__main__":
    miasto = "Poland, Wrocław"
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
    main(G, lights, plotting=True, start = 3284135585, end = 151334702)

    # losowy jeden przypadek:
    # main(G, lights, plotting=True)