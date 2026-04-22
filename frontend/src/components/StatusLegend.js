import React from "react";

function LegendItem({ color, text }) {
  return (
    <div className="legend-item">
      <span className="legend-color" style={{ background: color }}></span>
      <span>{text}</span>
    </div>
  );
}

function StatusLegend() {
  return (
    <div className="legend-box">
      <div className="legend-group">
        <h4>Node / Evacuee Legend</h4>
        <LegendItem color="#2563eb" text="Source Node" />
        <LegendItem color="#16a34a" text="Shelter Node / Evacuated" />
        <LegendItem color="#06b6d4" text="Moving Evacuee" />
        <LegendItem color="#eab308" text="Waiting Evacuee" />
        <LegendItem color="#dc2626" text="Stuck Evacuee" />
      </div>

      <div className="legend-group">
        <h4>Road Legend</h4>
        <LegendItem color="#111827" text="Normal Road" />
        <LegendItem color="#f59e0b" text="Partially Loaded Road" />
        <LegendItem color="#7c3aed" text="Highly Loaded Road" />
        <LegendItem color="#dc2626" text="Blocked Road" />
      </div>
    </div>
  );
}

export default StatusLegend;