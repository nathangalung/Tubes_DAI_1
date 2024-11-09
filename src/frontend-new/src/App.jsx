// App.jsx
import React, { useState, useEffect } from "react";
import Main from "./components/Main";
import Steepest from "./components/Steepest";
import Sideways from "./components/Sideways";
import Stochastic from "./components/Stochastic";
import Simulated from "./components/Simulated";
import Random from "./components/Random";
import Genetic from "./components/Genetic";

const API_URL = 'http://localhost:8000';

const App = () => {
  const [selectedAlgorithm, setSelectedAlgorithm] = useState(null);
  const [initialCube, setInitialCube] = useState(null); // Remove localStorage initialization
  const [initialCost, setInitialCost] = useState(null); // Remove localStorage initialization
  const [finalCube, setFinalCube] = useState(null);
  const [finalCost, setFinalCost] = useState(null);
  const [duration, setDuration] = useState(null);
  const [iterations, setIterations] = useState(null);
  const [costs, setCosts] = useState([]);
  const [restart, setRestart] = useState(null);
  const [population, setPopulation] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const clearStorage = () => {
      localStorage.removeItem('initialCube');
      localStorage.removeItem('initialCost');
    };

    window.addEventListener('beforeunload', clearStorage);
    return () => window.removeEventListener('beforeunload', clearStorage);
  }, []);

  const fetchInitialCube = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/initialize_cube`);
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      
      // Update state with response data
      setInitialCube(data.initial_cube);
      setInitialCost(data.initial_cost);
      
      // Store in localStorage
      localStorage.setItem('initialCube', JSON.stringify(data.initial_cube));
      localStorage.setItem('initialCost', JSON.stringify(data.initial_cost));
    } catch (error) {
      console.error("Failed to fetch initial cube:", error);
      setInitialCube(null);
      setInitialCost(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAlgorithm = async (algorithmType) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/run_algorithm`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          algorithm: algorithmType,
          cube: initialCube
        })
      });

      if (!response.ok) throw new Error('Algorithm execution failed');
      const result = await response.json();
      
      setFinalCube(result.final_cube);
      setFinalCost(result.final_cost);
      setDuration(result.duration);
      setIterations(result.iterations);
      setCosts(result.costs); // Set costs array
      setSelectedAlgorithm(algorithmType);
    } catch (error) {
      console.error("Algorithm execution failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    setSelectedAlgorithm(null);
  };

  const renderAlgorithm = () => {
    const commonProps = {
      initialCube,
      finalCube,
      initialCost,
      finalCost,
      duration,
      iterations,
      costs,
      onBack: () => setSelectedAlgorithm(null),
      isLoading
    };

    const specificProps = {
      random: { ...commonProps, restart },
      genetic: { ...commonProps, population }
    };

    switch (selectedAlgorithm) {
      case "steepest": return <Steepest {...commonProps} />;
      case "sideways": return <Sideways {...commonProps} />;
      case "stochastic": return <Stochastic {...commonProps} />;
      case "simulated": return <Simulated {...commonProps} />;
      case "random": return <Random {...specificProps.random} />;
      case "genetic": return <Genetic {...specificProps.genetic} />;
      default: return null;
    }
  };

  return (
    <>
      {!selectedAlgorithm ? (
        <Main 
          onAlgorithmSelect={handleAlgorithm}
          initialCube={initialCube}
          initialCost={initialCost}
          onInitialize={fetchInitialCube}
          isLoading={isLoading}
        />
      ) : (
        renderAlgorithm()
      )}
    </>
  );
};

export default App;