import React, { useState, useEffect } from 'react';

function LiveMetrics({ targetValue, label, emoji, isRunning }) {
  const [currentValue, setCurrentValue] = useState(0);

  useEffect(() => {
    if (!isRunning && targetValue > 0) {
      // Animate to target value
      const duration = 2000; // 2 seconds
      const steps = 60;
      const increment = targetValue / steps;
      let step = 0;

      const timer = setInterval(() => {
        step++;
        setCurrentValue(Math.min(targetValue, increment * step));
        
        if (step >= steps) {
          clearInterval(timer);
          setCurrentValue(targetValue);
        }
      }, duration / steps);

      return () => clearInterval(timer);
    } else if (isRunning) {
      setCurrentValue(0);
    }
  }, [targetValue, isRunning]);

  return (
    <div className="live-metric">
      <span className="metric-emoji">{emoji}</span>
      <span className="metric-value">
        {Math.round(currentValue)}{typeof targetValue === 'number' && targetValue <= 100 ? '%' : ''}
      </span>
      <span className="metric-label">{label}</span>
    </div>
  );
}

export default LiveMetrics;