import React, { useState } from 'react';
import './App.css';

function App() {
  const [numberId, setNumberId] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleFetchNumbers = async () => {
    setError('');
    setResult(null);
    try {
      const response = await fetch(`http://localhost:9876/numbers/${numberId}`);
      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || 'An error occurred');
      }
    } catch (err) {
      setError('Failed to connect to the microservice.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Average Calculator Microservice Frontend</h1>
        <div className="container">
          <div className="input-section">
            <label htmlFor="numberid">Enter Number ID (p, f, e, r):</label>
            <input
              type="text"
              id="numberid"
              value={numberId}
              onChange={(e) => setNumberId(e.target.value)}
              placeholder="e.g., e"
            />
            <button onClick={handleFetchNumbers}>Fetch Numbers</button>
          </div>

          {error && <p style={{ color: 'red' }}>Error: {error}</p>}

          {result && (
            <div className="results-section">
              <h3>Results:</h3>
              <p><strong>Previous Window State:</strong> {JSON.stringify(result.windowPrevState)}</p>
              <p><strong>Current Window State:</strong> {JSON.stringify(result.windowCurrState)}</p>
              <p><strong>Numbers Fetched:</strong> {JSON.stringify(result.numbers)}</p>
              <p><strong>Average:</strong> {result.avg}</p>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
