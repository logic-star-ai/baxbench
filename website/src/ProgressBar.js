import React, { useState, useEffect } from 'react';

function ProgressBar({ output, isRunning }) {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');
  const [startTime, setStartTime] = useState(null);

  useEffect(() => {
    if (!isRunning) {
      setProgress(0);
      setCurrentStep('');
      setStartTime(null);
      return;
    }

    if (!startTime) {
      setStartTime(Date.now());
    }

    // Time-based progress
    const timer = setInterval(() => {
      if (startTime) {
        const elapsed = Date.now() - startTime;
        const estimatedDuration = 60000; // 60 seconds
        let newProgress = Math.min(90, (elapsed / estimatedDuration) * 100);
        let step = 'Running benchmark...';

        if (elapsed < 10000) step = 'Starting...';
        else if (elapsed < 20000) step = 'Loading scenarios...';
        else if (elapsed < 35000) step = 'Generating code...';
        else if (elapsed < 50000) step = 'Running tests...';
        else step = 'Processing results...';

        // Check for completion
        if (output.includes('pass@1') || output.includes('Complete') || output.includes('Done')) {
          newProgress = 100;
          step = 'Complete!';
        }

        setProgress(newProgress);
        setCurrentStep(step);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [isRunning, startTime, output]);

  return (
    <div className="progress-container">
      <div className="progress-header">
        <span className="progress-step">{currentStep}</span>
        <span className="progress-percent">{Math.round(progress)}%</span>
      </div>
      
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ 
            width: `${progress}%`,
            background: progress === 100 ? '#28a745' : '#007bff'
          }}
        >
          {progress > 0 && (
            <div className="progress-shine"></div>
          )}
        </div>
      </div>
      
      {isRunning && progress < 100 && (
        <div className="progress-dots">
          <span>•</span>
          <span>•</span>
          <span>•</span>
        </div>
      )}
    </div>
  );
}

export default ProgressBar;