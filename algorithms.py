import math
import heapq

import heapq

def beam_search(env, beta):
    start = env.start
    goal = env.goal

    g = {start: 0}
    parent = {start: None}
    frontier = [start]
    visited = set([start])

    while frontier:
        successors = []
        for node in frontier:
            if node == goal:
                return reconstruct_path(parent, goal)
            for (nb, cost) in env.get_neighbors(node):
                if nb not in visited:
                    visited.add(nb)
                    g_new = g[node] + cost
                    if g_new < g.get(nb, float('inf')):
                        g[nb] = g_new
                        parent[nb] = node
                    successors.append(nb)

        if not successors:  # ✅ evita bucles vacíos
            break

        successors = list(set(successors))
        successors.sort(key=lambda n: g[n] + heuristic(n, goal))
        frontier = successors[:beta]

    return None


def reconstruct_path(parent, node):
    path = []
    while node is not None:
        path.append(node)
        node = parent[node]
    return list(reversed(path))

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def dynamic_weighted_a_star(env, epsilon=1.5):
    start = env.start
    goal  = env.goal
    N = env.size * env.size

    g = {start: 0}
    parent = {start: None}
    # heap entries: (f, counter, node, depth)
    heap = []
    counter = 0
    h0 = heuristic(start, goal)
    weight0 = 1 + epsilon * (1 - (0 / N))
    heapq.heappush(heap, (g[start] + weight0 * h0, counter, start, 0))

    closed = set()

    while heap:
        f, _, node, depth = heapq.heappop(heap)
        if node in closed:
            continue
        if node == goal:
            return reconstruct_path(parent, goal)

        closed.add(node)

        for (nb, cost) in env.get_neighbors(node):
            tentative_g = g[node] + cost
            if tentative_g < g.get(nb, float('inf')):
                g[nb] = tentative_g
                parent[nb] = node
                depth_nb = depth + 1
                h = heuristic(nb, goal)
                weight = 1 + epsilon * (1 - (depth_nb / N))
                f_nb = tentative_g + weight * h
                counter += 1
                heapq.heappush(heap, (f_nb, counter, nb, depth_nb))

    return None

def path_cost(path, env):
    total = 0
    for i in range(len(path)-1):
        curr = path[i]
        nxt = path[i+1]
        # find cost in neighbors
        for (nb, cost) in env.get_neighbors(curr):
            if nb == nxt:
                total += cost
                break
    return total
