import React, { useEffect, useMemo, useState } from "react";
import ControlPanel from "./components/ControlPanel";
import MetricsPanel from "./components/MetricsPanel";
import CampusGraph from "./components/CampusGraph";
import ProgressChart from "./components/ProgressChart";
import StatusLegend from "./components/StatusLegend";
import SummaryBadges from "./components/SummaryBadges";
import "./App.css";

function App() {
  const [options, setOptions] = useState({ scenarios: [], strategies: [] });
  const [scenario, setScenario] = useState("normal");
  const [strategy, setStrategy] = useState("dp");
  const [numEvacuees, setNumEvacuees] = useState(10);
  const [maxSteps, setMaxSteps] = useState(12);
  const [loading, setLoading] = useState(false);
  const [simData, setSimData] = useState(null);
  const [frameIndex, setFrameIndex] = useState(0);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/options")
      .then((res) => res.json())
      .then((data) => setOptions(data))
      .catch((err) => console.error(err));
  }, []);

  useEffect(() => {
    if (!playing || !simData || !simData.frames?.length) return;

    const timer = setInterval(() => {
      setFrameIndex((prev) => {
        if (prev >= simData.frames.length - 1) {
          clearInterval(timer);
          return prev;
        }
        return prev + 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [playing, simData]);

  const runSimulation = async () => {
    setLoading(true);
    setPlaying(false);
    setFrameIndex(0);

    try {
      const response = await fetch("http://127.0.0.1:8000/simulate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          scenario,
          strategy,
          num_evacuees: Number(numEvacuees),
          max_steps: Number(maxSteps)
        })
      });

      const data = await response.json();
      setSimData(data);
    } catch (error) {
      console.error("Simulation error:", error);
      alert("Failed to run simulation.");
    } finally {
      setLoading(false);
    }
  };

  const resetPlayback = () => {
    setPlaying(false);
    setFrameIndex(0);
  };

  const currentFrame = useMemo(() => {
    if (!simData || !simData.frames || simData.frames.length === 0) return null;
    return simData.frames[frameIndex];
  }, [simData, frameIndex]);

  const maxFrame = simData?.frames?.length ? simData.frames.length - 1 : 0;

  return (
    <div className="app-shell">
      <header className="hero-header">
        <div>
          <h1>IIT Delhi Disaster Evacuation Simulator</h1>
          <p>Dynamic Programming Based Evacuation from Karakoram Hostel</p>
        </div>
        <div className="hero-tags">
          <span className="hero-tag">IIT Delhi</span>
          <span className="hero-tag">Karakoram Source</span>
          <span className="hero-tag">DP + Baselines</span>
        </div>
      </header>

      <ControlPanel
        options={options}
        scenario={scenario}
        setScenario={setScenario}
        strategy={strategy}
        setStrategy={setStrategy}
        numEvacuees={numEvacuees}
        setNumEvacuees={setNumEvacuees}
        maxSteps={maxSteps}
        setMaxSteps={setMaxSteps}
        runSimulation={runSimulation}
        loading={loading}
        playing={playing}
        setPlaying={setPlaying}
        hasData={!!simData}
        frameIndex={frameIndex}
        setFrameIndex={setFrameIndex}
        maxFrame={maxFrame}
        resetPlayback={resetPlayback}
      />

      <SummaryBadges
        scenario={scenario}
        strategy={strategy}
        frame={currentFrame}
        frameIndex={frameIndex}
        totalFrames={maxFrame + 1}
        numEvacuees={numEvacuees}
      />

      <div className="dashboard-grid">
        <div className="panel panel-large">
          <div className="panel-header">
            <h2>Campus Evacuation Graph</h2>
            <span className="panel-subtitle">
              Live frame-based evacuation view
            </span>
          </div>

          {simData ? (
            <>
              <CampusGraph
                graph={simData.graph}
                source={simData.source}
                shelters={simData.shelters}
                frame={currentFrame}
              />
              <StatusLegend />
            </>
          ) : (
            <div className="empty-state">
              Run a simulation to display the IIT Delhi campus graph.
            </div>
          )}
        </div>

        <div className="side-column">
          <div className="panel">
            <div className="panel-header">
              <h2>Metrics</h2>
              <span className="panel-subtitle">Final simulation summary</span>
            </div>
            {simData ? (
              <MetricsPanel metrics={simData.metrics} />
            ) : (
              <div className="empty-state">No metrics available yet.</div>
            )}
          </div>

          <div className="panel">
            <div className="panel-header">
              <h2>Current Frame Status</h2>
              <span className="panel-subtitle">Live playback information</span>
            </div>
            {currentFrame ? (
              <div className="frame-status-box">
                <div className="frame-line">
                  <strong>Step:</strong> <span>{currentFrame.step}</span>
                </div>
                <div className="frame-line">
                  <strong>Frame Index:</strong> <span>{frameIndex}</span>
                </div>
                <div className="frame-line">
                  <strong>Playback:</strong> <span>{playing ? "Playing" : "Paused"}</span>
                </div>
              </div>
            ) : (
              <div className="empty-state">No frame loaded.</div>
            )}
          </div>
        </div>
      </div>

      <div className="panel chart-panel">
        <div className="panel-header">
          <h2>Evacuation Progress</h2>
          <span className="panel-subtitle">Time-wise evacuee counts</span>
        </div>
        {simData && Array.isArray(simData.history) ? (
          <ProgressChart history={simData.history} />
        ) : (
          <div className="empty-state">Run a simulation to see progress curves.</div>
        )}
      </div>
    </div>
  );
}

export default App;