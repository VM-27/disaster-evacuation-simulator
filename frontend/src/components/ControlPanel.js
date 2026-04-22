import React from "react";

function ControlPanel({
  options,
  scenario,
  setScenario,
  strategy,
  setStrategy,
  numEvacuees,
  setNumEvacuees,
  maxSteps,
  setMaxSteps,
  runSimulation,
  loading,
  playing,
  setPlaying,
  hasData,
  frameIndex,
  setFrameIndex,
  maxFrame,
  resetPlayback,
}) {
  return (
    <div className="panel control-panel">
      <div className="panel-header">
        <h2>Simulation Controls</h2>
      </div>

      <div className="control-grid">
        <div className="control-item">
          <label>Scenario</label>
          <select value={scenario} onChange={(e) => setScenario(e.target.value)}>
            {(options?.scenarios || []).map((item) => (
              <option key={item} value={item}>
                {item.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
              </option>
            ))}
          </select>
        </div>

        <div className="control-item">
          <label>Strategy</label>
          <select value={strategy} onChange={(e) => setStrategy(e.target.value)}>
            {(options?.strategies || []).map((item) => (
              <option key={item} value={item}>
                {item === "dp"
                  ? "Dynamic Programming"
                  : item.charAt(0).toUpperCase() + item.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div className="control-item">
          <label>Number of Evacuees</label>
          <input
            type="number"
            min="1"
            max="500"
            value={numEvacuees}
            onChange={(e) => setNumEvacuees(Number(e.target.value))}
          />
        </div>

        <div className="control-item">
          <label>Maximum Steps</label>
          <input
            type="number"
            min="1"
            max="200"
            value={maxSteps}
            onChange={(e) => setMaxSteps(Number(e.target.value))}
          />
        </div>

        <div className="control-item button-stack">
          <button onClick={runSimulation} disabled={loading}>
            {loading ? "Running..." : "Run"}
          </button>

          <button onClick={() => setPlaying(true)} disabled={!hasData}>
            Play
          </button>

          <button onClick={() => setPlaying(false)} disabled={!hasData}>
            Pause
          </button>

          <button onClick={resetPlayback} disabled={!hasData}>
            Reset
          </button>
        </div>

        <div className="control-item slider-box">
          <label>Frame Slider</label>
          <input
            type="range"
            min="0"
            max={maxFrame || 0}
            value={frameIndex}
            onChange={(e) => setFrameIndex(Number(e.target.value))}
            disabled={!hasData}
          />
          <div>
            Frame: {frameIndex} / {maxFrame}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ControlPanel;