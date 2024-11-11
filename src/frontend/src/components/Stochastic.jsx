import { useState } from 'react';
import { ArrowLeft } from "lucide-react";
import Cube from "./Cube";
import Chart from './Chart';
import Player from './Player';

export default function StochasticVisualization({
  initialCube,
  finalCube,
  initialCost,
  finalCost,
  averageCost,
  duration,
  iteration,
  costs,
  states
}) {
  const [isPlayerOpen, setIsPlayerOpen] = useState(false);

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
          <h1 className="text-4xl font-bold mb-2">Stochastic Hill-Climbing Algorithm</h1>
          <p className="text-[#94a3b8] mb-8">Visualize the randomized solution approach for solving the Magic Cube.</p>

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
                { label: "Number of Iteration", value: iteration }
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

          <div className="bg-[#16181d] rounded-lg p-6">
            <Chart 
              costs={costs} 
              title="Stochastic Objective Function vs Iteration Plot" 
            />
          </div>
        </div>
      </div>

      {isPlayerOpen && (
        <Player
          onClose={() => setIsPlayerOpen(false)}
          states={states}
          iteration={iteration}
        />
      )}
    </div>
  );
};
