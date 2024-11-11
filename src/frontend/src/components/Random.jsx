import { useState } from 'react';
import { ArrowLeft, RotateCcw } from "lucide-react";
import Cube from "./Cube";
import Chart from './Chart';
import Player from './Player';

export default function RandomRestartVisualization({
  initialCube,
  finalCube,
  initialCost,
  finalCost,
  averageCost,
  duration,
  iteration,
  restart,
  iterationRestart,
  costs,
  states
}) {
  const [isPlayerOpen, setIsPlayerOpen] = useState(false);
  const displayIterations = iterationRestart.slice(0, 10);

  return (
    <div className="bg-[#0a0a0a] text-white font-['Space_Grotesk',system-ui,sans-serif] min-h-screen p-8 overflow-hidden">
      <div className="max-w-[1400px] mx-auto">
        <a
          href="/"
          className="inline-flex items-center gap-2 px-4 py-3 bg-[#16181d] rounded-xl text-[#94a3b8] hover:text-white transition-colors mb-8 border border-[#1e1e1e] text-sm"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </a>

        <div className="max-w-[1200px] mx-auto">
          <h1 className="text-4xl font-bold mb-2">Random Restart Hill-Climbing Algorithm</h1>
          <p className="text-[#94a3b8] mb-8">Explore multiple randomized restarts to escape local optima and solve the Magic Cube.</p>

          <div className="grid grid-cols-1 lg:grid-cols-[1fr_1fr_300px] gap-6 mb-8">
            <div className="bg-[#16181d] p-10 rounded-lg flex flex-col items-center text-center">
              <h2 className="text-xl font-semibold mb-2">Initial State Cube</h2>
              <div className="w-full max-w-[400px] h-[400px] bg-[#1a1d24] rounded-lg overflow-hidden flex items-center justify-center">
                <Cube magic_cube={JSON.parse(JSON.stringify(initialCube))} />
              </div>
              <div className="text-sm text-[#94a3b8] mt-2">
                Initial State Cost: {initialCost}
              </div>
            </div>

            <div className="bg-[#16181d] p-10 rounded-lg flex flex-col items-center text-center">
              <h2 className="text-xl font-semibold mb-2">Final State Cube</h2>
              <div className="w-full max-w-[400px] h-[400px] bg-[#1a1d24] rounded-lg overflow-hidden flex items-center justify-center">
                <Cube magic_cube={JSON.parse(JSON.stringify(finalCube))} />
              </div>
              <div className="text-sm text-[#94a3b8] mt-2">
                Final State Cost: {finalCost}
              </div>
            </div>

            <div className="flex flex-col gap-4">
              {[
                { label: "Average Cost", value: `${averageCost}` },
                { label: "Duration", value: `${duration}s` },
                { label: "Number of Iteration", value: iteration },
                { label: 'Number of Restart', value: restart }
              ].map((metric, index) => (
                <div key={index} className="bg-[#16181d] rounded-lg p-2 w-[185px]">
                  <div className="text-sm text-[#94a3b8] mb-1">{metric.label}</div>
                  <div className="text-2xl font-semibold text-[#8b5cf6]">{metric.value}</div>
                </div>
              ))}
              <button
                onClick={() => setIsPlayerOpen(true)}
                className="mt-4 bg-[#8b5cf6] text-white rounded-lg py-2 px-4 hover:bg-[#7a4bd1] transition w-[185px]"
              >
                Replay
              </button>
            </div>
          </div>

          <div className="bg-[#16181d] p-8 rounded-lg mb-6">
            <h2 className="text-xl text-gray-400 font-semibold text-center mb-8">
              Number of Iteration per Restart
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-10 gap-4">
              {displayIterations.map((value, index) => (
                <div
                  key={index}
                  className="flex flex-col items-center p-4 bg-[#1a1d24]/60 rounded-lg backdrop-blur-xl transition-transform hover:-translate-y-1"
                >
                  <div className="w-12 h-12 bg-[#16181d] rounded-xl flex items-center justify-center mb-4">
                    <RotateCcw className="w-6 h-6" />
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-gray-400 mb-1">Restart {index + 1}</div>
                    <div className="text-xl font-bold">{value}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#16181d] p-6 rounded-lg">
            <Chart 
              costs={costs} 
              title="Random Restart Objective Function vs Iteration Plot" 
            />
          </div>
        </div>
      </div>

      {isPlayerOpen && (
        <Player
          onClose={() => setIsPlayerOpen(false)}
          states={states}
          restart={restart}
          restartIndices={iterationRestart}
        />
      )}
    </div>
  );
};
