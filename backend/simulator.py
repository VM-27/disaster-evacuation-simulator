import random
import networkx as nx


def get_edge_cost(edge, strategy="dp"):
    if edge.get("blocked", False):
        return float("inf")

    travel_time = edge.get("travel_time", 1)
    capacity = max(edge.get("capacity", 1), 1)
    current_load = edge.get("current_load", 0)
    risk = edge.get("risk", 0.1)

    congestion_factor = 1 + (current_load / capacity)

    if strategy == "shortest":
        return travel_time
    elif strategy == "greedy":
        return travel_time * congestion_factor
    else:
        return travel_time * congestion_factor * (1 + risk)


def get_path_by_strategy(G, source, target, strategy="dp"):
    if source == target:
        return [source]

    dist = {node: float("inf") for node in G.nodes()}
    prev = {node: None for node in G.nodes()}
    dist[source] = 0
    visited = set()

    while len(visited) < len(G.nodes()):
        current = None
        current_dist = float("inf")

        for node in G.nodes():
            if node not in visited and dist[node] < current_dist:
                current = node
                current_dist = dist[node]

        if current is None:
            break

        if current == target:
            break

        visited.add(current)

        for nbr in G.neighbors(current):
            edge = G[current][nbr]
            cost = get_edge_cost(edge, strategy)

            if cost == float("inf"):
                continue

            new_dist = dist[current] + cost
            if new_dist < dist[nbr]:
                dist[nbr] = new_dist
                prev[nbr] = current

    if dist[target] == float("inf"):
        return []

    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def choose_best_shelter(G, current_node, shelters, strategy="dp"):
    best_shelter = None
    best_cost = float("inf")
    best_path = []

    for shelter in shelters:
        path = get_path_by_strategy(G, current_node, shelter, strategy)
        if not path:
            continue

        total_cost = 0
        for i in range(len(path) - 1):
            edge = G[path[i]][path[i + 1]]
            total_cost += get_edge_cost(edge, strategy)

        if total_cost < best_cost:
            best_cost = total_cost
            best_shelter = shelter
            best_path = path

    return best_shelter, best_path


def apply_scenario(G, scenario):
    if scenario == "fire_academic":
        if G.has_edge("Library", "Academic_Area"):
            G["Library"]["Academic_Area"]["blocked"] = True

    elif scenario == "hospital_block":
        if G.has_edge("Hospital", "Library"):
            G["Hospital"]["Library"]["blocked"] = True
        if G.has_edge("Hospital", "Main_Building"):
            G["Hospital"]["Main_Building"]["blocked"] = True

    elif scenario == "main_gate_congestion":
        if G.has_edge("IITD_Market", "Main_Gate"):
            G["IITD_Market"]["Main_Gate"]["current_load"] = 3
        if G.has_edge("Main_Building", "Main_Gate"):
            G["Main_Building"]["Main_Gate"]["current_load"] = 2

    elif scenario == "hostel_fire":
        if G.has_edge("Karakoram", "Hostels_Junction"):
            G["Karakoram"]["Hostels_Junction"]["risk"] = 0.9
        if G.has_edge("Hostels_Junction", "Hospital"):
            G["Hostels_Junction"]["Hospital"]["risk"] = 0.8
        if G.has_edge("Hostels_Junction", "SAC"):
            G["Hostels_Junction"]["SAC"]["risk"] = 0.7
        if G.has_edge("Hostels_Junction", "Open_Ground"):
            G["Hostels_Junction"]["Open_Ground"]["risk"] = 0.6

    elif scenario == "multi_zone_disaster":
        if G.has_edge("Hospital", "Library"):
            G["Hospital"]["Library"]["blocked"] = True
        if G.has_edge("Library", "Academic_Area"):
            G["Library"]["Academic_Area"]["risk"] = 0.9
        if G.has_edge("Main_Building", "Academic_Area"):
            G["Main_Building"]["Academic_Area"]["risk"] = 0.8

    elif scenario == "shelter_failure":
        pass

    elif scenario == "night_evacuation":
        for u, v in G.edges():
            G[u][v]["travel_time"] = G[u][v].get("travel_time", 1) + 1
            G[u][v]["risk"] = min(1.0, G[u][v].get("risk", 0.1) + 0.2)

    return G


def build_edge_load_map(G):
    edge_loads = {}
    for u, v, data in G.edges(data=True):
        key = "__".join(sorted([u, v]))
        edge_loads[key] = data.get("current_load", 0)
    return edge_loads


def build_category_counts(evacuees):
    counts = {
        "student": 0,
        "injured": 0,
        "staff": 0
    }
    for evac in evacuees:
        category = evac.get("category", "student")
        if category in counts:
            counts[category] += 1
    return counts


def run_simulation(G, source, shelters, num_evacuees, max_steps, strategy="dp", scenario="normal"):
    G = G.copy()

    for u, v in G.edges():
        if "current_load" not in G[u][v]:
            G[u][v]["current_load"] = 0
        if "blocked" not in G[u][v]:
            G[u][v]["blocked"] = False
        if "risk" not in G[u][v]:
            G[u][v]["risk"] = 0.1
        if "travel_time" not in G[u][v]:
            G[u][v]["travel_time"] = 1
        if "capacity" not in G[u][v]:
            G[u][v]["capacity"] = 2

    G = apply_scenario(G, scenario)

    active_shelters = list(shelters)
    if scenario == "shelter_failure":
        active_shelters = ["Main_Gate"]

    evacuees = []

    for i in range(num_evacuees):
        category = random.choices(
            ["student", "injured", "staff"],
            weights=[0.7, 0.2, 0.1]
        )[0]

        if category == "student":
            speed_factor = 1.0
        elif category == "injured":
            speed_factor = 1.6
        else:
            speed_factor = 0.8

        evacuees.append({
            "id": i,
            "current_node": source,
            "status": "waiting",
            "time_taken": 0.0,
            "path": [],
            "category": category,
            "speed_factor": speed_factor
        })

    frames = []
    history = []

    for step in range(max_steps + 1):
        frames.append({
            "step": step,
            "evacuees": [
                {
                    "id": e["id"],
                    "current_node": e["current_node"],
                    "status": e["status"],
                    "category": e["category"]
                }
                for e in evacuees
            ],
            "edge_loads": build_edge_load_map(G)
        })

        evacuated_count = sum(1 for e in evacuees if e["status"] == "evacuated")
        waiting_count = sum(1 for e in evacuees if e["status"] == "waiting")
        moving_count = sum(1 for e in evacuees if e["status"] == "moving")
        stuck_count = sum(1 for e in evacuees if e["status"] == "stuck")

        history.append({
            "time": step,
            "evacuated": evacuated_count,
            "waiting": waiting_count,
            "moving": moving_count,
            "stuck": stuck_count
        })

        if evacuated_count + stuck_count == num_evacuees:
            break

        for u, v in G.edges():
            G[u][v]["current_load"] = 0

        for evac in evacuees:
            if evac["status"] in ["evacuated", "stuck"]:
                continue

            if evac["current_node"] in active_shelters:
                evac["status"] = "evacuated"
                continue

            target_shelter, path = choose_best_shelter(
                G,
                evac["current_node"],
                active_shelters,
                strategy
            )

            if not path or len(path) < 2:
                evac["status"] = "stuck"
                continue

            next_node = path[1]

            if not G.has_edge(evac["current_node"], next_node):
                evac["status"] = "stuck"
                continue

            edge = G[evac["current_node"]][next_node]

            if edge.get("blocked", False):
                evac["status"] = "stuck"
                continue

            base_time = edge.get("travel_time", 1)
            evac["time_taken"] += base_time * evac["speed_factor"]
            evac["current_node"] = next_node
            evac["path"] = path
            evac["status"] = "moving"
            edge["current_load"] += 1

            if evac["current_node"] in active_shelters:
                evac["status"] = "evacuated"

        for evac in evacuees:
            if evac["status"] == "moving" and evac["current_node"] not in active_shelters:
                evac["status"] = "waiting"

    evacuated = sum(1 for e in evacuees if e["status"] == "evacuated")
    stuck = sum(1 for e in evacuees if e["status"] == "stuck")
    evacuated_times = [e["time_taken"] for e in evacuees if e["status"] == "evacuated"]
    average_time = round(sum(evacuated_times) / len(evacuated_times), 2) if evacuated_times else 0

    metrics = {
        "total_evacuees": num_evacuees,
        "evacuated": evacuated,
        "stuck": stuck,
        "average_evacuation_time": average_time,
        "completion_step": len(history) - 1,
        "active_shelters": active_shelters,
        "category_counts": build_category_counts(evacuees)
    }

    return {
        "frames": frames,
        "metrics": metrics,
        "history": history
    }