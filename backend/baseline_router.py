import heapq


def valid_neighbors(G, node):
    return [nbr for nbr in G.neighbors(node) if not G[node][nbr].get("blocked", False)]


def shortest_path_route(G, source, shelters):
    pq = [(0, source, [source])]
    visited = {}

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost

        if node in shelters:
            return path

        for nbr in valid_neighbors(G, node):
            edge = G[node][nbr]
            new_cost = cost + edge.get("travel_time", 1)
            heapq.heappush(pq, (new_cost, nbr, path + [nbr]))

    return None


def greedy_route(G, source, shelters):
    path = [source]
    visited = {source}
    current = source

    while current not in shelters:
        candidates = []

        for nbr in valid_neighbors(G, current):
            if nbr in visited:
                continue

            edge = G[current][nbr]
            travel_time = edge.get("travel_time", 1)
            risk = edge.get("risk", 0)
            capacity = edge.get("capacity", 1)
            current_load = edge.get("current_load", 0)
            congestion = current_load / max(capacity, 1)

            immediate_cost = travel_time + risk + congestion
            candidates.append((immediate_cost, nbr))

        if not candidates:
            return None

        candidates.sort(key=lambda x: x[0])
        nxt = candidates[0][1]

        path.append(nxt)
        visited.add(nxt)
        current = nxt

    return path