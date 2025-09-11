import React, { useState } from 'react';
import SecurityDashboard from './SecurityDashboard';

const SCENARIOS = ['Login', 'Shopping', 'FileUpload'];
const MODELS = ['gpt-4o-mini', 'gpt-4o', 'claude-3-5-sonnet-20241022'];
const MODES = ['generate', 'test', 'evaluate'];

function RunTab() {
  const [config, setConfig] = useState({
    scenarios: ['Login'],
    model: 'gpt-4o-mini',
    nSamples: 3,
    temperature: 0.0,
    mode: 'generate',
    promptType: 'baseline',
    apiKey: ''
  });
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState('');

  const handleScenarioChange = (scenario) => {
    setConfig(prev => ({
      ...prev,
      scenarios: prev.scenarios.includes(scenario)
        ? prev.scenarios.filter(s => s !== scenario)
        : [...prev.scenarios, scenario]
    }));
  };

  const runBenchmark = async () => {
    if (!config.apiKey) {
      alert('Please enter your OpenAI API key');
      return;
    }

    setIsRunning(true);
    setOutput('Starting benchmark...\n');

    try {
      const response = await fetch('http://localhost:8000/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        setOutput(prev => prev + chunk);
      }
    } catch (error) {
      setOutput(prev => prev + `Error: ${error.message}\n`);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="run-tab">
      <div className="controls">
        <div className="control-group">
          <label>Scenarios:</label>
          <div className="checkbox-group">
            {SCENARIOS.map(scenario => (
              <label key={scenario} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={config.scenarios.includes(scenario)}
                  onChange={() => handleScenarioChange(scenario)}
                />
                {scenario}
              </label>
            ))}
          </div>
        </div>

        <div className="control-group">
          <label>Model:</label>
          <select value={config.model} onChange={e => setConfig({...config, model: e.target.value})}>
            {MODELS.map(model => <option key={model} value={model}>{model}</option>)}
          </select>
        </div>

        <div className="control-group">
          <label>Samples:</label>
          <input
            type="number"
            value={config.nSamples}
            onChange={e => setConfig({...config, nSamples: parseInt(e.target.value)})}
            min="1"
            max="10"
          />
        </div>

        <div className="control-group">
          <label>Temperature:</label>
          <input
            type="number"
            value={config.temperature}
            onChange={e => setConfig({...config, temperature: parseFloat(e.target.value)})}
            min="0"
            max="1"
            step="0.1"
          />
        </div>

        <div className="control-group">
          <label>Mode:</label>
          <select value={config.mode} onChange={e => setConfig({...config, mode: e.target.value})}>
            {MODES.map(mode => <option key={mode} value={mode}>{mode}</option>)}
          </select>
        </div>

        <div className="control-group">
          <label>Prompt Type:</label>
          <div className="radio-group">
            {['baseline', 'generic', 'corridor'].map(type => (
              <label key={type} className="radio-label">
                <input
                  type="radio"
                  name="promptType"
                  value={type}
                  checked={config.promptType === type}
                  onChange={e => setConfig({...config, promptType: e.target.value})}
                />
                {type}
              </label>
            ))}
          </div>
        </div>

        <div className="control-group">
          <label>OpenAI API Key:</label>
          <input
            type="password"
            value={config.apiKey}
            onChange={e => setConfig({...config, apiKey: e.target.value})}
            placeholder="sk-..."
          />
        </div>

        <button 
          className="run-button" 
          onClick={runBenchmark} 
          disabled={isRunning}
        >
          {isRunning ? 'Running...' : 'Run Benchmark'}
        </button>
      </div>

      <div className="output">
        <SecurityDashboard isRunning={isRunning} output={output} />
        <div className="output-logs">
          <h3>Output Logs:</h3>
          <pre className="output-text">{output}</pre>
        </div>
      </div>
    </div>
  );
}

export default RunTab;