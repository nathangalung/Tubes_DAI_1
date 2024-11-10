import React, { useState, useEffect } from "react";
import Main from "./components/Main";
import Steepest from "./components/Steepest";
import Sideways from "./components/Sideways";
import Stochastic from "./components/Stochastic";
import Random from "./components/Random";
import Simulated from "./components/Simulated";
import Genetic from "./components/Genetic";

const API_URL = 'http://localhost:8000';

const App = () => {
  const [selectedAlgorithm, setSelectedAlgorithm] = useState(null);
  const [initialCube, setInitialCube] = useState(() => {
    const saved = localStorage.getItem('initialCube');
    return saved ? JSON.parse(saved) : null;
  });
  const [initialCost, setInitialCost] = useState(() => {
    const saved = localStorage.getItem('initialCost');
    return saved ? JSON.parse(saved) : null;
  });
  const [finalCube, setFinalCube] = useState(null);
  const [finalCost, setFinalCost] = useState(null);
  const [duration, setDuration] = useState(null);
  const [iterations, setIterations] = useState(null);
  const [restart, setRestart] = useState(null);
  const [localOptima, setLocalOptima] = useState(null);
  const [iterationRestart, setIterationRestart] = useState([]);
  const [population, setPopulation] = useState(null);
  const [costs, setCosts] = useState([]);
  const [exps, setExps] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (initialCube && initialCost) {
      localStorage.setItem('initialCube', JSON.stringify(initialCube));
      localStorage.setItem('initialCost', JSON.stringify(initialCost));
    }
  }, [initialCube, initialCost]);

  useEffect(() => {
    const handleUnload = () => {
      localStorage.clear();
    };

    window.addEventListener('beforeunload', handleUnload);
    return () => {
      window.removeEventListener('beforeunload', handleUnload);
      localStorage.clear();
    };
  }, []);

  const fetchInitialCube = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/initialize_cube`);
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      
      setInitialCube(data.initial_cube);
      setInitialCost(data.initial_cost);
      
    } catch (error) {
      console.error("Failed to fetch initial cube:", error);
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
      setCosts(result.costs);
      if (algorithmType === 'random') {
        setRestart(result.restart);
        setIterationRestart(result.iteration_restart);
      }
      if (algorithmType === 'simulated') {
        setLocalOptima(result.local_optima);
        setExps(result.exps);
      }
      if (algorithmType === 'genetic') {
        setPopulation(result.population);
      }
      setCosts(result.costs);
      setSelectedAlgorithm(algorithmType);
    } catch (error) {
      console.error("Algorithm execution failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    setSelectedAlgorithm(null);
    setFinalCube(null);
    setFinalCost(null);
    setDuration(null);
    setIterations(null);
    setRestart(null);
    setIterationRestart([]);
    setLocalOptima(null);
    setPopulation(null);
    setCosts([]);
    setExps([]);
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
      onBack: handleBack,
      isLoading
    };

    const specificProps = {
      random: { ...commonProps, restart, iterationRestart },
      simulated: {...commonProps, localOptima, exps },
      genetic: { ...commonProps, population }
    };

    switch (selectedAlgorithm) {
      case "steepest": return <Steepest {...commonProps} />;
      case "sideways": return <Sideways {...commonProps} />;
      case "stochastic": return <Stochastic {...commonProps} />;
      case "random": return <Random {...specificProps.random} />;
      case "simulated": return <Simulated {...specificProps.simulated} />;
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