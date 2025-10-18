import math
import heapq

def beam_search(env, beta):
    """
    Beam Search: mantiene solo los β nodos más prometedores en cada nivel.
    Expande por niveles (BFS) pero limitando el ancho del beam.
    """
    start = env.start
    goal = env.goal
    frontier = [(heuristic(start, goal), start, [start])]
    visited = set([start])

    while frontier:
        # Mantener solo los β nodos más prometedores (según heurística)
        frontier.sort(key=lambda x: x[0])
        frontier = frontier[:beta]

        new_frontier = []
        for h_val, node, path in frontier:
            if node == goal:
                return path
            
            # Expandir vecinos
            for neighbor in env.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    h_neighbor = heuristic(neighbor, goal)
                    new_frontier.append((h_neighbor, neighbor, path + [neighbor]))
        
        frontier = new_frontier
    return None


def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def dynamic_weighted_a_star(env, epsilon=1.5):
    start = env.start
    goal = env.goal
    # Usar heap para mantener frontera ordenada eficientemente
    # Formato: (f_score, contador, nodo, camino, g_score, profundidad)
    counter = 0  # Para desempatar nodos con mismo f
    frontier = [(0, counter, start, [start], 0, 0)]
    visited = set()
    N = env.size * env.size

    while frontier:
        f, _, node, path, g, d = heapq.heappop(frontier)
        
        # Marcar como visitado al EXTRAER, no al insertar
        if node in visited:
            continue
        visited.add(node)
        
        if node == goal:
            return path

        for neighbor in env.get_neighbors(node):
            if neighbor not in visited:
                # g_new es el número de pasos desde el inicio
                g_new = g + 1
                h = heuristic(neighbor, goal)
                depth_new = d + 1
                
                # Peso dinámico que disminuye con la profundidad
                weight = 1 + epsilon * (1 - (depth_new / N))
                f_new = g_new + weight * h
                
                counter += 1
                heapq.heappush(frontier, 
                              (f_new, counter, neighbor, path + [neighbor], g_new, depth_new))
    return None
