import osmnx as ox
import networkx as nx
import random


def main():
    ox.settings.use_cache = True
    G = ox.graph_from_place("Poland, Wrocław", network_type="drive", simplify=True)
    
    #wizualizacjonowanie
    ox.plot_graph(G)

    nodes = list(G.nodes)
    start = random.choice(nodes)
    end = random.choice(nodes)
    print("Start:", start, "Koniec:", end)

    #route = nx.shortest_path(G, start, end, weight="length")
    route_length = nx.shortest_path_length(G, start, end, weight="length")
    print("Odległość:", route_length)

if __name__ == "__main__":
    main()


    