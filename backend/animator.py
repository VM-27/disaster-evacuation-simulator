import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter


def animate_simulation(G, pos, source, shelters, frames, history, save_path=None):
    fig, (ax_graph, ax_plot) = plt.subplots(1, 2, figsize=(16, 7))

    all_times = history["time"]
    all_evacuated = history["evacuated"]
    all_waiting = history["waiting"]
    all_moving = history["moving"]
    all_stuck = history["stuck"]

    def draw_base_graph(ax, edge_loads):
        ax.clear()

        node_colors = []
        for node in G.nodes():
            if node == source:
                node_colors.append("blue")
            elif node in shelters:
                node_colors.append("green")
            else:
                node_colors.append("lightgray")

        blocked_edges = []
        normal_edges = []
        edge_colors = []
        edge_widths = []

        for u, v, data in G.edges(data=True):
            if data["blocked"]:
                blocked_edges.append((u, v))
            else:
                normal_edges.append((u, v))
                key = tuple(sorted((u, v)))
                load = edge_loads.get(key, 0)
                cap = data["capacity"]

                if load == 0:
                    edge_colors.append("black")
                elif load < cap:
                    edge_colors.append("orange")
                else:
                    edge_colors.append("purple")

                edge_widths.append(2 + load)

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1600, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", ax=ax)

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=normal_edges,
            edge_color=edge_colors,
            width=edge_widths,
            ax=ax
        )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=blocked_edges,
            edge_color="red",
            style="dashed",
            width=3,
            ax=ax
        )

        edge_labels = {}
        for u, v, data in G.edges(data=True):
            key = tuple(sorted((u, v)))
            load = edge_loads.get(key, 0)
            label = f"{load}/{data['capacity']}"
            if data["blocked"]:
                label = "BLOCKED"
            edge_labels[(u, v)] = label

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_size=7,
            ax=ax
        )

        ax.set_axis_off()

    def update(frame_index):
        frame = frames[frame_index]
        step = frame["step"]
        evacuees = frame["evacuees"]
        edge_loads = frame["edge_loads"]

        draw_base_graph(ax_graph, edge_loads)

        evac_x = []
        evac_y = []
        evac_colors = []

        for evac in evacuees:
            node = evac["current_node"]
            x, y = pos[node]

            offset_x = (evac["id"] % 3) * 0.12 - 0.12
            offset_y = (evac["id"] // 3) * 0.12 - 0.12

            evac_x.append(x + offset_x)
            evac_y.append(y + offset_y)

            if evac["status"] == "evacuated":
                evac_colors.append("green")
            elif evac["status"] == "waiting":
                evac_colors.append("gold")
            elif evac["status"] == "stuck":
                evac_colors.append("red")
            else:
                evac_colors.append("cyan")

        ax_graph.scatter(evac_x, evac_y, s=120, c=evac_colors, edgecolors="black")
        ax_graph.set_title(f"IIT Delhi Evacuation | Step {step}")

        ax_plot.clear()
        upto = min(int(step + 1), len(all_times))
        if upto > 0:
            ax_plot.plot(all_times[:upto], all_evacuated[:upto], marker="o", label="Evacuated")
            ax_plot.plot(all_times[:upto], all_waiting[:upto], marker="s", label="Waiting")
            ax_plot.plot(all_times[:upto], all_moving[:upto], marker="^", label="Moving")
            ax_plot.plot(all_times[:upto], all_stuck[:upto], marker="x", label="Stuck")

        ax_plot.set_xlabel("Time Step")
        ax_plot.set_ylabel("Number of Evacuees")
        ax_plot.set_title("Evacuation Progress")
        ax_plot.grid(True)
        ax_plot.legend()

    anim = FuncAnimation(fig, update, frames=len(frames), interval=1000, repeat=False)

    if save_path is not None:
        writer = PillowWriter(fps=1)
        anim.save(save_path, writer=writer)

    plt.tight_layout()
    plt.show()

    return anim