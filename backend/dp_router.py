def edge_cost(data, alpha=1.0, beta=2.0, gamma=2.0):
    if data.get("blocked", False):
        return float("inf")

    travel_time = data.get("travel_time", 1)
    capacity = data.get("capacity", 1)
    risk = data.get("risk", 0)
    current_load = data.get("current_load", 0)

    congestion = current_load / max(capacity, 1)
    return alpha * travel_time + beta * congestion + gamma * risk


def compute_min_cost_to_shelter(G, shelters, alpha=1.0, beta=2.0, gamma=2.0):
    dp = {node: float("inf") for node in G.nodes()}
    next_hop = {node: None for node in G.nodes()}

    for shelter in shelters:
        dp[shelter] = 0

    changed = True
    max_iterations = len(G.nodes()) * 10
    iteration = 0

    while changed and iteration < max_iterations:
        changed = False
        iteration += 1

        for node in G.nodes():
            if node in shelters:
                continue

            best_cost = dp[node]
            best_neighbor = next_hop[node]

            for neighbor in G.neighbors(node):
                data = G[node][neighbor]
                cost = edge_cost(data, alpha, beta, gamma)
                if cost == float("inf"):
                    continue

                candidate = cost + dp[neighbor]
                if candidate < best_cost:
                    best_cost = candidate
                    best_neighbor = neighbor

            if best_cost < dp[node]:
                dp[node] = best_cost
                next_hop[node] = best_neighbor
                changed = True

    return dp, next_hop


def reconstruct_path(source, shelters, next_hop):
    path = [source]
    visited = {source}
    current = source

    while current not in shelters:
        nxt = next_hop.get(current)
        if nxt is None or nxt in visited:
            return None
        path.append(nxt)
        visited.add(nxt)
        current = nxt

    return path