// App.jsx
import { useState } from "react";
import Main from "./components/Main";
import Steepest from "./components/Steepest";

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
