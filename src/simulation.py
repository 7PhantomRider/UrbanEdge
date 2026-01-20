import random
import numpy as np

from config import (
    TRAFFIC_LIGHT_LAMBDA,
    TRAFFIC_DELAY_MIN,
    TRAFFIC_DELAY_MAX,
    PARKING_LAMBDA_CAR,
    PARKING_LAMBDA_BIKE,
)


def draw_traffic_light_delay():
    return np.random.exponential(1 / TRAFFIC_LIGHT_LAMBDA)


def draw_traffic_congestion_delay():
    x = random.uniform(TRAFFIC_DELAY_MIN, TRAFFIC_DELAY_MAX)
    return x


def draw_parking_time(vehicle_type):
    if vehicle_type == "car":
        x = np.random.exponential(1 / PARKING_LAMBDA_CAR)
        return x
    x = np.random.exponential(1 / PARKING_LAMBDA_CAR)
    return x


def estimate_time(G, route, base_speed_kmh, vehicle_type, n_lights):
    total = 0

    #tu zmiana bo rower ma inne potrącenie za światła
    light_penalty_factor = 1.0
    if vehicle_type == "bike":
        light_penalty_factor = 0.3  #ile czasu auta będzie czekać bike

    for _ in range(n_lights):
        total += draw_traffic_light_delay() * light_penalty_factor 

    for u, v in zip(route[:-1], route[1:]):
        data = G[u][v][0]
        length = data.get("length", 0)
        
        #speed
        maxspeed = data.get("maxspeed")
        try:
            if isinstance(maxspeed, list):
                speed_limit = float(maxspeed[0])
            else:
                speed_limit = float(maxspeed)
        except:
            speed_limit = base_speed_kmh
        
        #samochód ma speed limit a rower full base speed
        if vehicle_type == "car":
            real_speed = min(speed_limit, base_speed_kmh)
        else:
            real_speed = base_speed_kmh

        speed_m_s = real_speed * 1000 / 3600
        if speed_m_s > 0:
            total += length / speed_m_s
        
        #korki
        if vehicle_type == "car":
            #auto ma full korki
            total += draw_traffic_congestion_delay()
        else:
            #rower ma procent opóźnienia auta
            total += draw_traffic_congestion_delay() * 0.1

    #parking
    total += draw_parking_time(vehicle_type)

    return total