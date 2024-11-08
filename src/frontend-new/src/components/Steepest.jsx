import { ArrowLeft } from "lucide-react";
import Cube from "./Cube";

export default function SteepestAscentVisualization({ initialState, result }) {
  return (
    <div className="bg-[#0a0a0a] text-white font-['Space_Grotesk',system-ui,sans-serif] min-h-screen p-8">
      <div className="max-w-[1400px] mx-auto">
        <a
          href="/"
          className="inline-flex items-center gap-2 px-4 py-2 bg-[#111318] rounded-lg text-[#94a3b8] hover:text-white transition-colors mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </a>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-[#111318] rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-[#4f46e5]" />
              <h2 className="text-lg font-semibold">Initial State</h2>
            </div>
            <Cube magic_cube={initialState} />
            <div className="text-sm text-[#94a3b8]">
              Initial State Objective Function: 6505
            </div>
          </div>
          <div className="bg-[#111318] rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-[#22c55e]" />
              <h2 className="text-lg font-semibold">Final State</h2>
            </div>
            <div className="w-full aspect-video bg-[#1a1d24] rounded-lg mb-4" />
            {/* <Cube magic_cube={result.final_state} /> */}

            <div className="text-sm text-[#94a3b8]">
              Final State Objective Function: 104
            </div>
          </div>
        </div>

        {/* Rest of the component remains the same */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
          {[
            { title: "Solution Cost", value: "104" },
            { title: "Time Elapsed", value: "18.76s" },
            { title: "Number of Iterations", value: "1500" },
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
          <h3 className="mb-4">Plot of Fitness Values vs Iteration</h3>
          {/* Add chart implementation here */}
        </div>
      </div>
    </div>
  );
}
