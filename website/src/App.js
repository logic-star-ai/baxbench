import React, { useState } from 'react';
import RunTab from './RunTab';
import ResultsTab from './ResultsTab';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('run');

  return (
    <div className="app">
      <header className="header">
        <h1>BaxBench Security Benchmark</h1>
        <nav className="tabs">
          <button 
            className={activeTab === 'run' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('run')}
          >
            Run Benchmark
          </button>
          <button 
            className={activeTab === 'results' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('results')}
          >
            Results
          </button>
        </nav>
      </header>
      
      <main className="main">
        {activeTab === 'run' && <RunTab />}
        {activeTab === 'results' && <ResultsTab />}
      </main>
    </div>
  );
}

export default App;