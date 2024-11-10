import { ArrowLeft } from "lucide-react";
import Cube from "./Cube";
import Chart from './Chart';

export default function SimulatedAnnealingVisualization({
  initialCube,
  finalCube,
  initialCost,
  finalCost,
  duration,
  iterations,
  costs,
  onBack
}) {
  return (
    <div className="bg-[#0a0a0a] text-white font-['Space_Grotesk',system-ui,sans-serif] min-h-screen p-8">
      <div className="max-w-[1400px] mx-auto">
        <a
          href="/"
          className="inline-flex items-center gap-2 px-3 py-2 bg-[#16181d] rounded-xl text-[#94a3b8] hover:text-white transition-colors mb-8 border border-[#1e1e1e] text-sm"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </a>

        <div className="max-w-[1200px] mx-auto">
          <h1 className="text-4xl font-bold mb-2">Simulated Annealing</h1>
          <p className="text-[#94a3b8] mb-8">Experience the temperature-based probabilistic approach to finding a Magic Cube solution.</p>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <div className="bg-[#16181d] rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-4">Initial State</h2>
              <div className="w-full aspect-video bg-[#1a1d24] rounded-lg mb-2 overflow-hidden">
                <Cube magic_cube={initialCube} />
              </div>
              <div className="text-sm text-[#94a3b8]">
                Initial State Value: 6505
              </div>
            </div>
            <div className="bg-[#16181d] rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-4">Current State</h2>
              <div className="w-full aspect-video bg-[#1a1d24] rounded-lg mb-2 overflow-hidden">
                <Cube magic_cube={finalCube} />
              </div>
              <div className="text-sm text-[#94a3b8]">
                Current State Value: 104
              </div>
            </div>
            <div className="flex flex-col gap-4">
              {[
                { label: "Solution Cost", value: "104" },
                { label: "Time Elapsed", value: "18.76s" },
                { label: "Number of Iterations", value: "1500" },
                { label: "Number of Stuck in Local Optima", value: "15" },
              ].map((metric, index) => (
                <div key={index} className="bg-[#16181d] rounded-xl p-4">
                  <div className="text-sm text-[#94a3b8] mb-1">{metric.label}</div>
                  <div className="text-2xl font-semibold text-[#8b5cf6]">{metric.value}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#16181d] rounded-xl p-6 mb-6">
            <Chart 
              costs={costs} 
              title="Stochastic Objective Function Plot" 
            />
          </div>

          <div className="bg-[#16181d] rounded-xl p-6">
            <Chart 
                costs={costs} 
                title="Stochastic Objective Function Plot" 
              />
          </div>
        </div>
      </div>
    </div>
  );
};