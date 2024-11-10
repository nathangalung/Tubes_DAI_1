import { ArrowLeft } from "lucide-react";
import Cube from "./Cube";
import Chart from './Chart';

export default function SteepestAscentVisualization({
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
          className="inline-flex items-center gap-2 px-4 py-3 bg-[#16181d] rounded-xl text-[#94a3b8] hover:text-white transition-colors mb-8 border border-[#1e1e1e] text-sm"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </a>

        <div className="max-w-[1200px] mx-auto">
          <h1 className="text-4xl font-bold mb-2">Steepest Ascent Hill-climbing</h1>
          <p className="text-[#94a3b8] mb-8">Visualize the optimal gradient-based solution approach for solving the Magic Cube.</p>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <div className="bg-[#16181d] rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-4">Initial State</h2>
              <div className="w-full aspect-video bg-[#1a1d24] rounded-lg mb-2 overflow-hidden">
                <Cube magic_cube={initialCube} />
              </div>
              <div className="text-sm text-[#94a3b8]">
                Initial State Value: {initialCost}
              </div>
            </div>
            <div className="bg-[#16181d] rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-4">Current State</h2>
              <div className="w-full aspect-video bg-[#1a1d24] rounded-lg mb-2 overflow-hidden">
                <Cube magic_cube={finalCube} />
              </div>
              <div className="text-sm text-[#94a3b8]">
                Current State Value: {finalCost}
              </div>
            </div>
            <div className="flex flex-col gap-4">
              {[
                { label: "Solution Cost", value: finalCost },
                { label: "Time Elapsed", value: `${duration}s` },
                { label: "Number of Iterations", value: iterations },
              ].map((metric, index) => (
                <div key={index} className="bg-[#16181d] rounded-xl p-4">
                  <div className="text-sm text-[#94a3b8] mb-1">{metric.label}</div>
                  <div className="text-2xl font-semibold text-[#8b5cf6]">{metric.value}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#16181d] rounded-xl p-6">
            <Chart 
              costs={costs} 
              title="Steepest Ascent Objective Function vs Iteration Plot" 
            />
          </div>
        </div>
      </div>
    </div>
  );
};
