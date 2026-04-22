from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import csv
import json
from datetime import datetime
from graph_generator import create_iitd_graph
from simulator import run_simulation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    scenario: str = "normal"
    strategy: str = "dp"
    num_evacuees: int = 10
    max_steps: int = 12


@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.get("/options")
def get_options():
    return {
        "scenarios": [
            "normal",
            "fire_academic",
            "hospital_block",
            "main_gate_congestion",
            "hostel_fire",
            "multi_zone_disaster",
            "shelter_failure",
            "night_evacuation"
        ],
        "strategies": ["dp", "shortest", "greedy"]
    }


def save_results(metrics, scenario, strategy, evacuees):

    os.makedirs("results", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_file = f"results/run_{timestamp}.csv"
    json_file = f"results/run_{timestamp}.json"
    combined_file = "results/all_runs.csv"

    row = [
        scenario,
        strategy,
        evacuees,
        metrics.get("evacuated", 0),
        metrics.get("stuck", 0),
        metrics.get("average_evacuation_time", 0),
        metrics.get("completion_step", 0)
    ]

    headers = [
        "scenario",
        "strategy",
        "total_evacuees",
        "evacuated",
        "stuck",
        "average_time",
        "completion_step"
    ]

    # Individual run CSV
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(row)

    # Combined CSV (append)
    file_exists = os.path.exists(combined_file)

    with open(combined_file, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(headers)

        writer.writerow(row)

    # JSON summary
    with open(json_file, "w") as f:
        json.dump({
            "scenario": scenario,
            "strategy": strategy,
            "metrics": metrics
        }, f, indent=4)


def convert_graph_for_frontend(G, pos):
    nodes = []
    edges = []

    for node in G.nodes():
        x, y = pos[node]
        nodes.append({
            "id": node,
            "x": x,
            "y": y
        })

    for u, v, data in G.edges(data=True):
        edges.append({
            "source": u,
            "target": v,
            "capacity": data.get("capacity", 1),
            "blocked": data.get("blocked", False)
        })

    return {
        "nodes": nodes,
        "edges": edges
    }


@app.post("/simulate")
def simulate(req: SimulationRequest):
    G, pos, source, shelters = create_iitd_graph()

    result = run_simulation(
        G=G,
        source=source,
        shelters=shelters,
        num_evacuees=req.num_evacuees,
        max_steps=req.max_steps,
        strategy=req.strategy,
        scenario=req.scenario
    )

    save_results(
        result["metrics"],
        req.scenario,
        req.strategy,
        req.num_evacuees
    )

    graph = convert_graph_for_frontend(G, pos)

    return {
        "graph": graph,
        "frames": result["frames"],
        "metrics": result["metrics"],
        "history": result["history"],
        "source": source,
        "shelters": shelters
    }