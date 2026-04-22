import React from "react";

function ProgressChart({ history }) {
  if (!Array.isArray(history) || history.length === 0) {
    return <div className="empty-state">No progress data available yet.</div>;
  }

  const width = 900;
  const height = 280;
  const padding = 40;

  const maxTime = Math.max(...history.map((d) => d.time || 0), 1);
  const maxValue = Math.max(
    ...history.map((d) =>
      Math.max(
        d.evacuated || 0,
        d.waiting || 0,
        d.moving || 0,
        d.stuck || 0
      )
    ),
    1
  );

  const scaleX = (t) =>
    padding + (t / maxTime) * (width - 2 * padding);

  const scaleY = (v) =>
    height - padding - (v / maxValue) * (height - 2 * padding);

  const buildPath = (key) => {
    return history
      .map((point, index) => {
        const x = scaleX(point.time || 0);
        const y = scaleY(point[key] || 0);
        return `${index === 0 ? "M" : "L"} ${x} ${y}`;
      })
      .join(" ");
  };

  const evacuatedPath = buildPath("evacuated");
  const waitingPath = buildPath("waiting");
  const movingPath = buildPath("moving");
  const stuckPath = buildPath("stuck");

  return (
    <div className="progress-chart-wrapper">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        width="100%"
        height="280"
        style={{ background: "#ffffff", borderRadius: "12px" }}
      >
        <line
          x1={padding}
          y1={height - padding}
          x2={width - padding}
          y2={height - padding}
          stroke="#374151"
          strokeWidth="2"
        />
        <line
          x1={padding}
          y1={padding}
          x2={padding}
          y2={height - padding}
          stroke="#374151"
          strokeWidth="2"
        />

        {[0, 0.25, 0.5, 0.75, 1].map((ratio, idx) => {
          const value = Math.round(maxValue * ratio);
          const y = scaleY(value);
          return (
            <g key={`y-${idx}`}>
              <line
                x1={padding}
                y1={y}
                x2={width - padding}
                y2={y}
                stroke="#e5e7eb"
                strokeWidth="1"
              />
              <text
                x={padding - 10}
                y={y + 4}
                textAnchor="end"
                fontSize="11"
                fill="#6b7280"
              >
                {value}
              </text>
            </g>
          );
        })}

        {history.map((point, idx) => {
          const x = scaleX(point.time || 0);
          return (
            <text
              key={`x-${idx}`}
              x={x}
              y={height - padding + 18}
              textAnchor="middle"
              fontSize="11"
              fill="#6b7280"
            >
              {point.time || 0}
            </text>
          );
        })}

        <path d={evacuatedPath} fill="none" stroke="#16a34a" strokeWidth="3" />
        <path d={waitingPath} fill="none" stroke="#eab308" strokeWidth="3" />
        <path d={movingPath} fill="none" stroke="#06b6d4" strokeWidth="3" />
        <path d={stuckPath} fill="none" stroke="#dc2626" strokeWidth="3" />

        {history.map((point, idx) => {
          const x = scaleX(point.time || 0);
          return (
            <g key={`pt-${idx}`}>
              <circle cx={x} cy={scaleY(point.evacuated || 0)} r="3.5" fill="#16a34a" />
              <circle cx={x} cy={scaleY(point.waiting || 0)} r="3.5" fill="#eab308" />
              <circle cx={x} cy={scaleY(point.moving || 0)} r="3.5" fill="#06b6d4" />
              <circle cx={x} cy={scaleY(point.stuck || 0)} r="3.5" fill="#dc2626" />
            </g>
          );
        })}
      </svg>

      <div
        style={{
          display: "flex",
          gap: "18px",
          flexWrap: "wrap",
          marginTop: "12px",
          fontSize: "14px",
          fontWeight: "600",
        }}
      >
        <span style={{ color: "#16a34a" }}>Evacuated</span>
        <span style={{ color: "#eab308" }}>Waiting</span>
        <span style={{ color: "#06b6d4" }}>Moving</span>
        <span style={{ color: "#dc2626" }}>Stuck</span>
      </div>
    </div>
  );
}

export default ProgressChart;