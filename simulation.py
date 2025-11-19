import numpy as np
from config import *

def estimate_time(G, route, base_speed_kmh):
    total_time = 0
    for u, v in zip(route[:-1], route[1:]):
        data = G[u][v][0]
        length = data.get("length", 0)
        speed = base_speed_kmh
        speed_m_s = speed * 1000 / 3600
        total_time += length / speed_m_s
    return total_time

car_time = estimate_time(G, route, 50)
bike_time = estimate_time(G, route, 20)
print("Czas auta:", car_time, "s")
print("Czas roweru:", bike_time, "s")