import osmnx as ox
import networkx as nx
import random
import matplotlib.pyplot as plt

from simulation import estimate_time
from config import CAR_BASE_SPEED, BIKE_BASE_SPEED


def main():
    print("Pobieranie mapy Wrocławia...")
    ox.settings.use_cache = True

    G = ox.graph_from_place("Poland, Wrocław", network_type="drive", simplify=True)

    nodes = list(G.nodes)
    start = random.choice(nodes)
    end = random.choice(nodes)

    print("Start:", start)
    print("Cel:", end)

    route = nx.shortest_path(G, start, end, weight="length")
    route_length = nx.shortest_path_length(G, start, end, weight="length")

    print("Odległość:", route_length)

    car_time = estimate_time(G, route, CAR_BASE_SPEED, "car")
    bike_time = estimate_time(G, route, BIKE_BASE_SPEED, "bike")

    print("Auto:", round(car_time, 1), "s =", round(car_time/60, 2), "min")
    print("Rower:", round(bike_time, 1), "s =", round(bike_time/60, 2), "min")

    # rysowanie
    fig, ax = ox.plot_graph(G, show=False, close=False)
    ox.plot_graph_route(G, route, ax=ax, route_color="red",
                        route_linewidth=3, show=False, close=False)

    # start / end
    ax.scatter(G.nodes[start]["x"], G.nodes[start]["y"], c="green", s=80)
    ax.scatter(G.nodes[end]["x"], G.nodes[end]["y"], c="blue", s=80)

    plt.show()


if __name__ == "__main__":
    main()