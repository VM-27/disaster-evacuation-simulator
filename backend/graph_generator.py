import networkx as nx


def create_iitd_graph():
    G = nx.Graph()

    nodes = [
        "Karakoram",
        "Hostels_Junction",
        "SAC",
        "Hospital",
        "Main_Building",
        "Library",
        "Academic_Area",
        "LHC",
        "IITD_Market",
        "Main_Gate",
        "Open_Ground",
        "Shelter_2"
    ]

    for node in nodes:
        G.add_node(node)

    pos = {
        "Karakoram": (0, 4),
        "Hostels_Junction": (2, 4),
        "SAC": (3, 5),
        "Hospital": (4, 4),
        "Main_Building": (6, 4),
        "Library": (6, 3),
        "Academic_Area": (8, 4),
        "LHC": (8, 2),
        "IITD_Market": (10, 2),
        "Main_Gate": (12, 3),
        "Open_Ground": (4, 6),
        "Shelter_2": (5, 6)
    }

    edges = [
        ("Karakoram", "Hostels_Junction", 2, 4, 0.1, False),
        ("Hostels_Junction", "SAC", 2, 3, 0.2, False),
        ("Hostels_Junction", "Hospital", 2, 2, 0.1, False),
        ("Hostels_Junction", "Open_Ground", 3, 2, 0.2, False),
        ("SAC", "Hospital", 2, 2, 0.3, False),
        ("SAC", "Shelter_2", 2, 4, 0.1, False),
        ("Hospital", "Main_Building", 3, 2, 0.2, True),
        ("Hospital", "Library", 3, 2, 0.2, False),
        ("Main_Building", "Library", 1, 3, 0.1, False),
        ("Main_Building", "Academic_Area", 2, 2, 0.3, False),
        ("Library", "Academic_Area", 2, 2, 0.2, False),
        ("Library", "LHC", 2, 2, 0.2, False),
        ("Academic_Area", "LHC", 2, 2, 0.4, False),
        ("LHC", "IITD_Market", 2, 2, 0.2, False),
        ("IITD_Market", "Main_Gate", 3, 3, 0.1, False),
        ("Open_Ground", "Main_Gate", 4, 3, 0.2, False),
        ("Open_Ground", "Shelter_2", 1, 4, 0.1, False),
        ("Main_Building", "Main_Gate", 4, 2, 0.2, False),
    ]

    for u, v, travel_time, capacity, risk, blocked in edges:
        G.add_edge(
            u,
            v,
            travel_time=travel_time,
            capacity=capacity,
            risk=risk,
            blocked=blocked,
            current_load=0
        )

    source = "Karakoram"
    shelters = ["Main_Gate", "Shelter_2"]

    return G, pos, source, shelters