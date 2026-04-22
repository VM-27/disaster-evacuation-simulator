def summarize_results(evacuees, history, strategy_name, scenario_name):
    total = len(evacuees)
    evacuated = sum(1 for e in evacuees if e["status"] == "evacuated")
    stuck = sum(1 for e in evacuees if e["status"] == "stuck")

    avg_steps = 0.0
    if total > 0:
        avg_steps = sum(e["steps_taken"] for e in evacuees) / total

    completion_step = history["time"][-1] if history["time"] else 0

    return {
        "scenario": scenario_name,
        "strategy": strategy_name,
        "total_evacuees": total,
        "evacuated": evacuated,
        "stuck": stuck,
        "evacuation_rate": evacuated / total if total else 0.0,
        "avg_steps_taken": avg_steps,
        "completion_step": completion_step
    }


def print_summary_table(results):
    print("\n===== MILESTONE 5: SCENARIO-BASED EVACUATION =====\n")
    print(
        f"{'Scenario':<20} {'Strategy':<12} {'Total':<8} {'Evacuated':<10} "
        f"{'Stuck':<8} {'Rate':<10} {'AvgSteps':<10} {'FinishStep':<12}"
    )
    print("-" * 110)

    for r in results:
        print(
            f"{r['scenario']:<20} "
            f"{r['strategy']:<12} "
            f"{r['total_evacuees']:<8} "
            f"{r['evacuated']:<10} "
            f"{r['stuck']:<8} "
            f"{r['evacuation_rate']:<10.2f} "
            f"{r['avg_steps_taken']:<10.2f} "
            f"{r['completion_step']:<12}"
        )