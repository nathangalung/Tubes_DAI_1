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
    const savedCube = localStorage.getItem('initialCube');
    return savedCube ? JSON.parse(savedCube) : null;
  });
  const [initialCost, setInitialCost] = useState(() => {
    const savedCost = localStorage.getItem('initialCost');
    return savedCost ? JSON.parse(savedCost) : null;
  });
  const [finalCube, setFinalCube] = useState(null);
  const [finalCost, setFinalCost] = useState(null);
  const [averageCost, setAverageCost] = useState(null);
  const [duration, setDuration] = useState(null);
  const [iteration, setIteration] = useState(null);
  const [restart, setRestart] = useState(null);
  const [localOptima, setLocalOptima] = useState(null);
  const [iterationRestart, setIterationRestart] = useState([]);
  const [population, setPopulation] = useState(null);
  const [costs, setCosts] = useState([]);
  const [states, setStates] = useState([]);
  const [exps, setExps] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch new initial cube and set state
  const fetchInitialCube = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/initialize_cube`);
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      
      // Save the initial cube to both state and local storage
      setInitialCube(data.initial_cube);
      setInitialCost(data.initial_cost);
      localStorage.setItem('initialCube', JSON.stringify(data.initial_cube));
      localStorage.setItem('initialCost', JSON.stringify(data.initial_cost));
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
      setAverageCost(result.average_cost);
      setDuration(result.duration);
      setIteration(result.iteration);
      setCosts(result.costs);
      setStates(result.states);
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
      averageCost,
      duration,
      iteration,
      costs,
      states,
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
