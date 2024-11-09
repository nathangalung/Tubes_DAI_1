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
  onBack,
}) {
  if (!initialCube || !finalCube) return null;
  return (
    <div className="bg-[#0a0a0a] text-white font-['Space_Grotesk',system-ui,sans-serif] min-h-screen p-8">
      <div className="max-w-[1400px] mx-auto">
        <button
          onClick={onBack}  // Changed from anchor tag to button with onClick
          className="inline-flex items-center gap-2 px-4 py-2 bg-[#111318] rounded-lg text-[#94a3b8] hover:text-white transition-colors mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-[#111318] rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-[#4f46e5]" />
              <h2 className="text-lg font-semibold">Initial State</h2>
            </div>
            <Cube magic_cube={initialCube} />  {/* Changed from initialState */}
            <div className="text-sm text-[#94a3b8]">
              Initial State Cost: {initialCost}  {/* Use prop instead of hardcoded value */}
            </div>
          </div>
          <div className="bg-[#111318] rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-[#22c55e]" />
              <h2 className="text-lg font-semibold">Final State</h2>
            </div>
            <Cube magic_cube={finalCube} />  {/* Changed from result.final_state */}
            <div className="text-sm text-[#94a3b8]">
              Final State Cost: {finalCost}  {/* Use prop instead of hardcoded value */}
            </div>
          </div>
        </div>

        {/* Rest of the component remains the same */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
          {[
            { title: "Solution Cost", value: finalCost },
            { title: "Time Elapsed", value: `${duration}s` },
            { title: "Number of Iterations", value: iterations },
          ].map((metric, index) => (
            <div key={index} className="bg-[#111318] rounded-2xl p-6">
              <h3 className="text-sm text-[#94a3b8] mb-2">{metric.title}</h3>
              <div className="text-2xl font-bold text-[#4f46e5]">
                {metric.value}
              </div>
            </div>
          ))}
        </div>

        <div className="bg-[#111318] rounded-2xl p-6">
          <Chart 
            costs={costs} 
            title="Steepest Ascent Objective Function Plot" 
          />
        </div>
      </div>
    </div>
  );
}
