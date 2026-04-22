import React from "react";

function MetricsPanel({ metrics }) {
  if (!metrics) {
    return (
      <div className="metrics-panel">
        <h2>Metrics</h2>
        <p>No simulation data yet.</p>
      </div>
    );
  }

  return (
    <div className="metrics-panel">
      <h2>Metrics</h2>

      <div className="metric-card">
        <strong>Total Evacuees:</strong> {metrics.total_evacuees}
      </div>

      <div className="metric-card">
        <strong>Evacuated:</strong> {metrics.evacuated}
      </div>

      <div className="metric-card">
        <strong>Stuck:</strong> {metrics.stuck}
      </div>

      <div className="metric-card">
        <strong>Average Evacuation Time:</strong> {metrics.average_evacuation_time}
      </div>

      <div className="metric-card">
        <strong>Completion Step:</strong> {metrics.completion_step}
      </div>

      {metrics?.scenario_description && (
        <div className="metric-card">
          <strong>Scenario Detail:</strong> {metrics.scenario_description}
        </div>
      )}

      {metrics?.active_shelters && (
        <div className="metric-card">
          <strong>Active Shelters:</strong> {metrics.active_shelters.join(", ")}
        </div>
      )}

      {metrics?.disabled_shelters?.length > 0 && (
        <div className="metric-card">
          <strong>Disabled Shelters:</strong> {metrics.disabled_shelters.join(", ")}
        </div>
      )}
      {metrics?.category_counts && (
  <>
    <div className="metric-card">
      <strong>Students:</strong> {metrics.category_counts.student}
    </div>
    <div className="metric-card">
      <strong>Injured:</strong> {metrics.category_counts.injured}
    </div>
    <div className="metric-card">
      <strong>Staff:</strong> {metrics.category_counts.staff}
    </div>
  </>
)}
    </div>
  );
}

export default MetricsPanel;