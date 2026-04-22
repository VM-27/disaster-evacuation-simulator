import React from "react";

function CampusGraph({ graph, source, shelters, frame }) {
  const width = 800;
  const height = 420;

  const scaleX = (x) => 60 + x * 50;
  const scaleY = (y) => height - (40 + y * 50);

  const edgeLoadMap = frame?.edge_loads || {};
  const evacuees = frame?.evacuees || [];

  const getEdgeKey = (a, b) => {
    return [a, b].sort().join("__");
  };

  if (!graph || !graph.nodes || !graph.edges) {
    return <div className="empty-state">No graph data available.</div>;
  }

  return (
    <svg viewBox={`0 0 ${width} ${height}`}>
      {graph.edges.map((edge, index) => {
        const sourceNode = graph.nodes.find((n) => n.id === edge.source);
        const targetNode = graph.nodes.find((n) => n.id === edge.target);

        if (!sourceNode || !targetNode) return null;

        const x1 = scaleX(sourceNode.x);
        const y1 = scaleY(sourceNode.y);
        const x2 = scaleX(targetNode.x);
        const y2 = scaleY(targetNode.y);

        const currentLoad = edgeLoadMap[getEdgeKey(edge.source, edge.target)] || 0;

        let stroke = "#111827";
        if (edge.blocked) stroke = "#dc2626";
        else if (currentLoad > 0 && currentLoad < edge.capacity) stroke = "#f59e0b";
        else if (currentLoad >= edge.capacity && currentLoad > 0) stroke = "#7c3aed";

        return (
          <g key={index}>
            <line
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke={stroke}
              strokeWidth={edge.blocked ? 4 : 3}
              strokeDasharray={edge.blocked ? "8 6" : "0"}
            />
            <text
              x={(x1 + x2) / 2}
              y={(y1 + y2) / 2 - 6}
              textAnchor="middle"
              fontSize="10"
              fill="#374151"
            >
              {edge.blocked ? "BLOCKED" : `${currentLoad}/${edge.capacity}`}
            </text>
          </g>
        );
      })}

      {graph.nodes.map((node) => {
        const x = scaleX(node.x);
        const y = scaleY(node.y);

        let fill = "#d1d5db";
        if (node.id === source) fill = "#2563eb";
        if (shelters.includes(node.id)) fill = "#16a34a";

        return (
          <g key={node.id}>
            <circle cx={x} cy={y} r="18" fill={fill} stroke="#111827" strokeWidth="1.5" />
            <text x={x} y={y - 24} textAnchor="middle" fontSize="12" fontWeight="bold">
              {node.id}
            </text>
          </g>
        );
      })}

      {evacuees.map((evac) => {
        const node = graph.nodes.find((n) => n.id === evac.current_node);
        if (!node) return null;

        const baseX = scaleX(node.x);
        const baseY = scaleY(node.y);

        const offsetX = (evac.id % 3) * 8 - 8;
        const offsetY = Math.floor(evac.id / 3) * 8 - 8;

        let fill = "#06b6d4";

        if (evac.category === "injured") fill = "#f97316";
        if (evac.category === "staff") fill = "#6366f1";

        if (evac.status === "evacuated") fill = "#16a34a";
        else if (evac.status === "waiting") fill = "#eab308";
        else if (evac.status === "stuck") fill = "#dc2626";

        return (
          <circle
            key={evac.id}
            cx={baseX + offsetX}
            cy={baseY + offsetY}
            r="5.5"
            fill={fill}
            stroke="#111827"
          />
        );
      })}
    </svg>
  );
}

export default CampusGraph;