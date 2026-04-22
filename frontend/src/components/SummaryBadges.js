import React from "react";

function Badge({ label, value }) {
  return (
    <div className="badge-card">
      <div className="label">{label}</div>
      <div className="value">{value}</div>
    </div>
  );
}

function SummaryBadges({ scenario, strategy, frame, frameIndex, totalFrames, numEvacuees }) {
  return (
    <div className="badge-row">
      <Badge label="Scenario" value={scenario} />
      <Badge label="Strategy" value={strategy} />
      <Badge label="Evacuees" value={numEvacuees} />
      <Badge label="Current Step" value={frame ? frame.step : "-"} />
      <Badge label="Frame" value={`${frameIndex}/${Math.max(totalFrames - 1, 0)}`} />
    </div>
  );
}

export default SummaryBadges;