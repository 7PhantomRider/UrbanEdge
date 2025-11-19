import osmnx as ox

ox.settings.use_cache =True

G = ox.graph_from_place('Poland, Wrocław', network_type="drive", simplify=True)
fig, ax = ox.plot_graph(G)


# Example: list first 5 edges with length & speed
for u, v, key, data in list(G.edges(keys=True, data=True))[:5]:
    length = data.get("length")          # meters
    speed  = data.get("maxspeed")        # e.g. "50" or "50;60"
    print(u, v, length, speed)
