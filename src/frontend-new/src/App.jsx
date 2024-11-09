// App.jsx
import { useState } from "react";
import Main from "./components/Main";
import Steepest from "./components/Steepest";
import Sideways from "./components/Sideways"
import Stochastic from "./components/Stochastic"
import Simulated from "./components/Simulated"
import Random from "./components/Random"
import Genetic from "./components/Genetic"
<component />

const App = () => {
  const [selectedAlgorithm, setSelectedAlgorithm] = useState(null);
  const [initialState, setInitialState] = useState(null);

  const handleAlgorithm = (algorithmType, state) => {
    setSelectedAlgorithm(algorithmType);
    setInitialState(state);
    console.log(`Selected algorithm: ${algorithmType}`);
    console.log("Initial state:", state);
    // Ready for backend fetch
  };

  const renderAlgorithm = () => {
    switch (selectedAlgorithm) {
      case "steepest":
        return (
          <Steepest
            initialState={initialState}
            //  result={}
          />
        );
        case "sideways":
          return (
            <Sideways
              initialState={initialState}
              //  result={}
            />
          );
        case "stochastic":
          return (
            <Stochastic
              initialState={initialState}
              //  result={}
            />
          );
          case "simulated":
            return (
              <Simulated
                initialState={initialState}
                //  result={}
              />
            );
          case "random":
            return (
              <Random
                initialState={initialState}
                //  result={}
              />
            );
            case "genetic":
              return (
                <Genetic
                  initialState={initialState}
                  //  result={}
                />
              );
        
      // Add other cases with initialState prop
      default:
        return null;
    }
  };

  return (
    <>
      {!selectedAlgorithm ? (
        <Main onAlgorithmSelect={handleAlgorithm} />
      ) : (
        renderAlgorithm()
      )}
    </>
  );
};

export default App;
