from copy import deepcopy


def _ensure_edge_fields(edge):
    edge.setdefault("capacity", 10)
    edge.setdefault("congestion", 0)
    edge.setdefault("blocked", False)
    edge.setdefault("risk", 1.0)
    edge.setdefault("time_multiplier", 1.0)
    return edge


def _safe_set_edge(graph, u, v, **updates):
    if u in graph and v in graph[u]:
        _ensure_edge_fields(graph[u][v])
        graph[u][v].update(updates)

    if v in graph and u in graph[v]:
        _ensure_edge_fields(graph[v][u])
        graph[v][u].update(updates)


def _mark_blocked(graph, u, v):
    _safe_set_edge(graph, u, v, blocked=True, capacity=0, risk=9999.0)


def _mark_risky(graph, u, v, risk=3.0, time_multiplier=1.5):
    _safe_set_edge(graph, u, v, risk=risk, time_multiplier=time_multiplier)


def _mark_congested(graph, u, v, capacity=None, congestion=None, risk=None, time_multiplier=None):
    updates = {}
    if capacity is not None:
        updates["capacity"] = capacity
    if congestion is not None:
        updates["congestion"] = congestion
    if risk is not None:
        updates["risk"] = risk
    if time_multiplier is not None:
        updates["time_multiplier"] = time_multiplier
    _safe_set_edge(graph, u, v, **updates)


def get_available_scenarios():
    return [
        "normal",
        "fire_academic",
        "hospital_block",
        "main_gate_congestion",
        "hostel_fire",
        "multi_zone_disaster",
        "shelter_failure",
        "night_evacuation",
    ]


def apply_scenario(graph, scenario_name, shelters=None):
    modified_graph = deepcopy(graph)

    for u in modified_graph:
        for v in modified_graph[u]:
            _ensure_edge_fields(modified_graph[u][v])

    metadata = {
        "name": scenario_name,
        "disabled_shelters": [],
        "global_time_multiplier": 1.0,
        "description": ""
    }

    if scenario_name == "normal":
        metadata["description"] = "Normal evacuation conditions."
        return modified_graph, metadata

    elif scenario_name == "fire_academic":
        metadata["description"] = "Fire risk near Academic Area."
        _mark_blocked(modified_graph, "Academic_Area", "Library")
        _mark_risky(modified_graph, "Academic_Area", "Hostels_Junction", risk=3.5, time_multiplier=1.7)
        _mark_risky(modified_graph, "Academic_Area", "Hospital", risk=3.0, time_multiplier=1.5)
        return modified_graph, metadata

    elif scenario_name == "hospital_block":
        metadata["description"] = "Roads near Hospital are blocked."
        _mark_blocked(modified_graph, "Hospital", "Library")
        _mark_blocked(modified_graph, "Hospital", "Main_Gate")
        return modified_graph, metadata

    elif scenario_name == "main_gate_congestion":
        metadata["description"] = "Heavy congestion near Main Gate."
        _mark_congested(modified_graph, "Library", "Main_Gate", capacity=3, congestion=4, risk=2.5, time_multiplier=1.8)
        _mark_congested(modified_graph, "Hospital", "Main_Gate", capacity=2, congestion=5, risk=3.0, time_multiplier=2.0)
        return modified_graph, metadata

    elif scenario_name == "hostel_fire":
        metadata["description"] = "Fire starts near Karakoram hostel region, making nearby roads risky."
        _mark_risky(modified_graph, "Karakoram", "Hostels_Junction", risk=5.0, time_multiplier=2.2)
        _mark_risky(modified_graph, "Hostels_Junction", "Academic_Area", risk=4.0, time_multiplier=1.8)
        _mark_risky(modified_graph, "Hostels_Junction", "Library", risk=3.5, time_multiplier=1.6)
        _mark_risky(modified_graph, "Karakoram", "Academic_Area", risk=4.5, time_multiplier=2.0)
        metadata["global_time_multiplier"] = 1.05
        return modified_graph, metadata

    elif scenario_name == "multi_zone_disaster":
        metadata["description"] = "Simultaneous disruptions near Hospital and Academic Area."
        _mark_blocked(modified_graph, "Hospital", "Main_Gate")
        _mark_risky(modified_graph, "Hospital", "Library", risk=4.0, time_multiplier=1.9)
        _mark_risky(modified_graph, "Academic_Area", "Library", risk=4.5, time_multiplier=2.0)
        _mark_risky(modified_graph, "Academic_Area", "Hostels_Junction", risk=4.0, time_multiplier=1.8)
        _mark_congested(modified_graph, "Library", "Main_Gate", capacity=4, congestion=3, risk=2.7, time_multiplier=1.6)
        metadata["global_time_multiplier"] = 1.10
        return modified_graph, metadata

    elif scenario_name == "shelter_failure":
        metadata["description"] = "One shelter fails and evacuees must reroute to remaining shelters."
        metadata["disabled_shelters"] = ["Shelter_2"]
        _mark_blocked(modified_graph, "Library", "Shelter_2")
        _mark_blocked(modified_graph, "Hospital", "Shelter_2")
        _mark_congested(modified_graph, "Library", "Shelter_1", capacity=4, congestion=2, risk=2.0, time_multiplier=1.4)
        _mark_congested(modified_graph, "Hospital", "Main_Gate", capacity=3, congestion=2, risk=2.2, time_multiplier=1.5)
        return modified_graph, metadata

    elif scenario_name == "night_evacuation":
        metadata["description"] = "Night evacuation reduces movement efficiency and increases risk."
        metadata["global_time_multiplier"] = 1.35

        for u in modified_graph:
            for v in modified_graph[u]:
                modified_graph[u][v]["risk"] *= 1.25
                modified_graph[u][v]["time_multiplier"] *= 1.30

        _mark_risky(modified_graph, "Academic_Area", "Library", risk=3.8, time_multiplier=1.8)
        _mark_risky(modified_graph, "Hospital", "Main_Gate", risk=3.5, time_multiplier=1.7)
        _mark_risky(modified_graph, "Hostels_Junction", "Academic_Area", risk=3.2, time_multiplier=1.6)
        return modified_graph, metadata

    else:
        metadata["description"] = f"Unknown scenario '{scenario_name}', using normal."
        metadata["name"] = "normal"
        return modified_graph, metadata