import React, { useState, useEffect } from 'react';

const FRAMEWORKS = ['Flask', 'Django', 'FastAPI', 'Express', 'Fastify', 'Koa', 'Nest'];
const SCENARIOS = ['Login', 'Shopping', 'FileUpload'];
const CWES = ['CWE-89', 'CWE-79', 'CWE-22', 'CWE-78', 'CWE-502', 'CWE-400'];

function SecurityDashboard({ isRunning, output }) {
  const [vulnerabilities, setVulnerabilities] = useState({});
  const [securityScore, setSecurityScore] = useState(0);
  const [cweCount, setCweCount] = useState({});
  const [heatmapData, setHeatmapData] = useState({});

  useEffect(() => {
    if (output) {
      parseSecurityEvents(output);
    }
  }, [output]);

  const parseSecurityEvents = (logOutput) => {
    const lines = logOutput.split('\n');
    let newVulns = { ...vulnerabilities };
    let newCwes = { ...cweCount };
    let newHeatmap = { ...heatmapData };
    let score = 0;
    let hasActivity = false;
    let tableData = [];

    // Parse BaxBench table output
    let inTable = false;
    let headers = [];
    
    lines.forEach(line => {
      // Check for any security-related activity
      if (line.includes('security') || line.includes('test') || line.includes('pass') || line.includes('fail')) {
        hasActivity = true;
      }

      // Detect table boundaries
      if (line.includes('┌') || line.includes('├')) {
        inTable = true;
        return;
      }
      if (line.includes('└')) {
        inTable = false;
        return;
      }

      // Parse table headers and data
      if (inTable && line.includes('│')) {
        const cells = line.split('│').map(cell => cell.trim()).filter(cell => cell);
        
        if (cells.length > 1) {
          if (headers.length === 0 && !cells[0].includes('insec') && !cells[0].includes('exceptions')) {
            headers = cells;
          } else if (cells[0] && (cells[0].includes('gpt') || cells[0].includes('Login') || cells[0].includes('Shopping'))) {
            const rowData = { scenario: cells[0] };
            cells.slice(1).forEach((cell, idx) => {
              if (headers[idx + 1]) {
                rowData[headers[idx + 1]] = cell;
              }
            });
            tableData.push(rowData);
          }
        }
      }

      // Parse for security successes (increase score)
      if (line.includes('PASS') || line.includes('secure')) {
        score += 10;
      }

      // Parse for security failures (don't increase score)
      if (line.includes('FAIL') || line.includes('insec')) {
        const framework = FRAMEWORKS.find(f => line.toLowerCase().includes(f.toLowerCase()));
        const scenario = SCENARIOS.find(s => line.toLowerCase().includes(s.toLowerCase()));
        
        if (framework && scenario) {
          const key = `${framework}-${scenario}`;
          newHeatmap[key] = 'danger';
        }
      }

      // Parse for CWE mentions (vulnerabilities found)
      CWES.forEach(cwe => {
        if (line.includes(cwe)) {
          newCwes[cwe] = (newCwes[cwe] || 0) + 1;
        }
      });

      // Parse for specific vulnerabilities
      if (line.toLowerCase().includes('sql injection')) {
        newVulns['SQL Injection'] = (newVulns['SQL Injection'] || 0) + 1;
      }
      if (line.toLowerCase().includes('xss') || line.toLowerCase().includes('cross-site')) {
        newVulns['XSS'] = (newVulns['XSS'] || 0) + 1;
      }
      if (line.toLowerCase().includes('auth')) {
        newVulns['Auth Bypass'] = (newVulns['Auth Bypass'] || 0) + 1;
      }
    });

    // If running but no activity yet, show minimal score
    if (isRunning && !hasActivity) {
      score = 5;
    }

    setVulnerabilities(newVulns);
    setCweCount(newCwes);
    setHeatmapData(newHeatmap);
    setSecurityScore(Math.min(100, score));
    
    // Store parsed table data
    if (tableData.length > 0) {
      setHeatmapData(prev => ({ ...prev, tableData }));
    }
  };

  const getHeatmapColor = (framework, scenario) => {
    const key = `${framework}-${scenario}`;
    const status = heatmapData[key];
    
    if (status === 'danger') return '#dc3545';
    if (status === 'warning') return '#ffc107';
    return '#28a745';
  };

  const getHeatmapText = (framework, scenario) => {
    const key = `${framework}-${scenario}`;
    const status = heatmapData[key];
    
    if (status === 'danger') return 'HIGH';
    if (status === 'warning') return 'MED';
    return 'SAFE';
  };

  const totalVulns = Object.values(vulnerabilities).reduce((sum, count) => sum + count, 0);
  const totalCwes = Object.values(cweCount).reduce((sum, count) => sum + count, 0);

  return (
    <div className="security-dashboard">
      <h3>Live Security Dashboard</h3>
      


      {/* Live Counters */}
      <div className="vulnerability-counters">
        <div className="counter-card">
          <span className="counter-value">{totalVulns}</span>
          <span className="counter-label">Vulnerabilities</span>
        </div>
        
        <div className="counter-card">
          <span className="counter-value">{totalCwes}</span>
          <span className="counter-label">CWEs Detected</span>
        </div>
        
        <div className="counter-card">
          <span className="counter-value">{isRunning ? '...' : 'Done'}</span>
          <span className="counter-label">Status</span>
        </div>
      </div>

      {/* Vulnerability Breakdown */}
      {Object.keys(vulnerabilities).length > 0 && (
        <div className="vulnerability-breakdown">
          <h4>Vulnerability Types</h4>
          <div className="vuln-list">
            {Object.entries(vulnerabilities).map(([type, count]) => (
              <div key={type} className="vuln-item">
                <span className="vuln-type">{type}</span>
                <span className={`vuln-count ${count > 0 ? 'pulse' : ''}`}>{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}



      {/* Results Table */}
      {heatmapData.tableData && heatmapData.tableData.length > 0 && (
        <div className="results-table">
          <h4>Benchmark Results</h4>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Scenario</th>
                  <th>Framework</th>
                  <th>Security Status</th>
                  <th>Exceptions</th>
                </tr>
              </thead>
              <tbody>
                {heatmapData.tableData.map((row, idx) => {
                  const frameworks = Object.keys(row).filter(k => k !== 'scenario');
                  return frameworks.map((framework, fIdx) => (
                    <tr key={`${idx}-${fIdx}`}>
                      {fIdx === 0 && <td rowSpan={frameworks.length}>{row.scenario}</td>}
                      <td>{framework.split(' ')[0]}</td>
                      <td className={row[framework].includes('nan') ? 'no-data' : 'has-data'}>
                        {row[framework].split('\n')[0] || 'No data'}
                      </td>
                      <td>{row[framework].split('\n')[1] || 'N/A'}</td>
                    </tr>
                  ));
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* CWE Badges */}
      {Object.keys(cweCount).length > 0 && (
        <div className="cwe-badges">
          <h4>CWE Detections</h4>
          <div className="badge-container">
            {Object.entries(cweCount).map(([cwe, count]) => (
              <div key={cwe} className={`cwe-badge ${count > 0 ? 'active' : ''}`}>
                <span className="cwe-id">{cwe}</span>
                <span className="cwe-count">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default SecurityDashboard;