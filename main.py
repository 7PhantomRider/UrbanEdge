import osmnx as ox
import networkx as nx
import random
import matplotlib.pyplot as plt
from shapely.geometry import Point

from shortest_path import shortest_path
from simulation import estimate_time
from config import CAR_BASE_SPEED, BIKE_BASE_SPEED


def count_lights_on_route(G, route, lights_gdf, dist=20):
    """
    sprawdzić, czy zliczamy dobrze światła. nie działa 😭
    """
    count = 0
    for node in route:
        x = G.nodes[node]["x"]
        y = G.nodes[node]["y"]
        p = Point(x, y)

        # odległość w METRACH (bo CRS jest projektowany)
        nearby = lights_gdf.distance(p) < dist
        if nearby.any():
            count += 1
    return int(count/2)



def main(plotting:bool=True) -> tuple[float, float]:
    nodes = list(G.nodes)
    start = random.choice(nodes)
    print(f"start = {start}")
    end = random.choice(nodes)
    print(f"end={end}")
    lights = ox.features_from_place(
        "Wrocław, Poland",
        tags={"highway": "traffic_signals"}
    )
    lights = lights.to_crs(G.graph["crs"])
    print("Start:", start)
    print("Cel:", end)


    try:
        route, route_length = shortest_path(G, start, end)
        #route = nx.shortest_path(G, start, end)
        #route_length = nx.shortest_path_length(G, start, end, weight="length")
    except Exception as e:
        print("nie ma drogi między punktami")
        print(e)
        return (float("inf"), float("inf"))


    print("Odległość [m]:", route_length)

    # liczba świateł na trasie (w promieniu 20 m)
    n_lights = count_lights_on_route(G, route, lights, dist=20)
    print("Liczba świateł na trasie:", n_lights)

    car_time = estimate_time(G, route, CAR_BASE_SPEED, "car", n_lights)
    bike_time = estimate_time(G, route, BIKE_BASE_SPEED, "bike", n_lights)

    if car_time < bike_time:
        print("samochód wygrywa")
    else:
        print("rower wygrywa")

    print("Auto:", round(car_time, 1), "s =", round(car_time / 60, 2), "min")
    print("Rower:", round(bike_time, 1), "s =", round(bike_time / 60, 2), "min")

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
    main()
