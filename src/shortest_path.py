import heapq
import networkx

def shortest_path(G: networkx.classes.multidigraph.MultiDiGraph, start:int, end:int):

    distances = {node: float('inf') for node in G.nodes}
    previous = {node: None for node in G.nodes}
    distances[start] = 0

    # Priority queue
    pq = [(0, start)]
    visited = set()

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == end:
            break

        for neighbor in G.neighbors(current_node):
            if neighbor in visited:
                continue

            edge_data = G.get_edge_data(current_node, neighbor)

            if isinstance(edge_data, dict) and 0 in edge_data:
                weight = edge_data[0].get('length', 1)
            else:
                weight = edge_data.get('length', 1)

            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    if distances[end] == float('inf'):
        print("nie ma drogi")
        raise Exception("no path")
        # return None, float('inf')

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    path_length = distances[end]


    return (path, path_length)