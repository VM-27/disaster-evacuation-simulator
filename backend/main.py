import os
import matplotlib.pyplot as plt

from graph_generator import create_iitd_graph
from scenarios import apply_scenario
from simulator import run_simulation
from metrics import summarize_results, print_summary_table
from animator import animate_simulation


OUTPUT_DIR = "outputs"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_strategy_comparison(results, scenario_name):
    strategies = [r["strategy"] for r in results]
    evacuated = [r["evacuated"] for r in results]
    stuck = [r["stuck"] for r in results]
    avg_steps = [r["avg_steps_taken"] for r in results]

    plt.figure(figsize=(10, 6))
    plt.bar(strategies, evacuated, label="Evacuated")
    plt.bar(strategies, stuck, bottom=evacuated, label="Stuck")
    plt.xlabel("Strategy")
    plt.ylabel("Number of Evacuees")
    plt.title(f"Evacuation Outcome Comparison - {scenario_name}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"{scenario_name}_outcome_comparison.png"))
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(strategies, avg_steps, marker="o")
    plt.xlabel("Strategy")
    plt.ylabel("Average Steps Taken")
    plt.title(f"Average Steps Comparison - {scenario_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"{scenario_name}_avg_steps.png"))
    plt.show()


def run_scenario(scenario_name, num_evacuees=10, max_steps=12):
    scenario_results = []
    dp_frames = None
    dp_history = None
    dp_graph = None

    for strategy in ["dp", "shortest", "greedy"]:
        G, pos, source, shelters = create_iitd_graph()
        G = apply_scenario(G, scenario_name)

        evacuees, history, frames = run_simulation(
            G,
            source,
            shelters,
            strategy=strategy,
            num_evacuees=num_evacuees,
            max_steps=max_steps
        )

        summary = summarize_results(
            evacuees,
            history,
            strategy.upper(),
            scenario_name
        )
        scenario_results.append(summary)

        if strategy == "dp":
            dp_frames = frames
            dp_history = history
            dp_graph = (G, pos, source, shelters)

    plot_strategy_comparison(scenario_results, scenario_name)

    if dp_frames is not None and dp_history is not None and dp_graph is not None:
        G, pos, source, shelters = dp_graph
        gif_path = os.path.join(OUTPUT_DIR, f"{scenario_name}_dp_animation.gif")
        animate_simulation(
            G,
            pos,
            source,
            shelters,
            dp_frames,
            dp_history,
            save_path=gif_path
        )

    return scenario_results


def main():
    ensure_output_dir()

    scenarios = [
        "normal",
        "fire_academic",
        "hospital_block",
        "main_gate_congestion"
    ]

    all_results = []

    for scenario_name in scenarios:
        print(f"\nRunning scenario: {scenario_name}")
        results = run_scenario(scenario_name, num_evacuees=10, max_steps=12)
        all_results.extend(results)

    print_summary_table(all_results)


if __name__ == "__main__":
    main()