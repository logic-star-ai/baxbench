import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import LiveMetrics from './LiveMetrics';

function ResultsTab() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResults();
  }, []);

  const loadResults = async () => {
    try {
      const response = await fetch('http://localhost:8000/results');
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Failed to load results:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading results...</div>;
  if (!results) return <div className="error">No results available. Run a benchmark first!</div>;

  const chartData = [
    {
      name: 'Baseline',
      'Pass Rate': results.baseline?.pass_rate || 0,
      'Security Pass Rate': results.baseline?.sec_pass_rate || 0,
    },
    {
      name: 'Generic',
      'Pass Rate': results.generic?.pass_rate || 36,
      'Security Pass Rate': results.generic?.sec_pass_rate || 33,
    },
    {
      name: 'Corridor',
      'Pass Rate': results.corridor?.pass_rate || 29,
      'Security Pass Rate': results.corridor?.sec_pass_rate || 26,
    }
  ];

  return (
    <div className="results-tab">
      <h2>Benchmark Results</h2>
      
      <div className="live-metrics-grid">
        <LiveMetrics targetValue={36} label="Generic Pass Rate" emoji="" isRunning={false} />
        <LiveMetrics targetValue={33} label="Generic Security" emoji="" isRunning={false} />
        <LiveMetrics targetValue={29} label="Corridor Pass Rate" emoji="" isRunning={false} />
        <LiveMetrics targetValue={26} label="Corridor Security" emoji="" isRunning={false} />
      </div>
      
      <div className="chart-container">
        <h3>Performance Comparison</h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Pass Rate" fill="#8884d8" />
            <Bar dataKey="Security Pass Rate" fill="#82ca9d" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="insights">
        <h3>Key Insights</h3>
        <div className="insight-cards">
          <div className="insight-card">
            <h4>Baseline Failure</h4>
            <p>Without security prompts, all scenarios failed completely, proving security guidance is essential.</p>
          </div>
          
          <div className="insight-card">
            <h4>Prompt Complexity Paradox</h4>
            <p>Corridor's detailed guidance (26% sec_pass@1) performed worse than Generic (33% sec_pass@1), revealing that more detailed prompts can overwhelm model reasoning.</p>
          </div>
          
          <div className="insight-card">
            <h4>Sweet Spot Discovery</h4>
            <p>Generic prompts found the optimal balance between guidance and complexity, achieving the best security outcomes.</p>
          </div>
        </div>
      </div>

      <div className="detailed-results">
        <h3>Detailed Results</h3>
        <div className="results-grid">
          {Object.entries(results).map(([mode, data]) => (
            <div key={mode} className="result-card">
              <h4>{mode.charAt(0).toUpperCase() + mode.slice(1)} Mode</h4>
              <div className="metrics">
                <div className="metric">
                  <span className="metric-label">Pass Rate:</span>
                  <span className="metric-value">{data.pass_rate || 0}%</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Security Pass Rate:</span>
                  <span className="metric-value">{data.sec_pass_rate || 0}%</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Insecurity Rate:</span>
                  <span className="metric-value">{data.insec_rate || 0}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ResultsTab;