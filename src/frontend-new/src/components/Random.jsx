import { ArrowLeft } from "lucide-react";
import Cube from "./Cube";
import Chart from './Chart';

export default function RandomRestartVisualization({
  initialCube,
  finalCube,
  initialCost,
  finalCost,
  duration,
  restart,
  iterations,
  costs,
  onBack
}) {
  return (
    <div className="min-h-screen bg-black text-white font-sans">
      <div className="max-w-7xl mx-auto p-8">
        <a
          href="/"
          className="inline-flex items-center gap-2 text-gray-400 text-sm bg-[#16181d] px-4 py-3 rounded-xl border border-[#1e1e1e] mb-8 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </a>

        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold mb-2">Random Restart Hill-Climbing</h1>
          <p className="text-gray-400 mb-8">
            Explore multiple randomized restarts to escape local optima and solve the Magic Cube.
          </p>

          <div className="grid grid-cols-1 lg:grid-cols-[1fr_1fr_300px] gap-6 mb-8">
            <div className="bg-[#16181d] p-6 rounded-lg">
              <h2 className="text-xl font-semibold mb-4">Initial State</h2>
              <div className="w-full aspect-video bg-[#1a1d24] rounded-lg mb-2 overflow-hidden">
                <Cube magic_cube={initialCube} />
              </div>
              <div className="text-sm text-gray-400">Initial State Value: {initialCost} </div>
            </div>

            <div className="bg-[#16181d] p-6 rounded-lg">
              <h2 className="text-xl font-semibold mb-4">Current State</h2>
              <div className="w-full aspect-video bg-[#1a1d24] rounded-lg mb-2 overflow-hidden">
                <Cube magic_cube={finalCube} />
              </div>
              <div className="text-sm text-gray-400">Current State Value: {finalCost}</div>
            </div>

            <div className="flex flex-col gap-4">
              {[
                { label: 'Solution Cost', value: finalCost },
                { label: 'Time Elapsed', value: `${duration}s`},
                { label: 'Number of Iterations', value: iterations },
                { label: 'Number of Restart', value: restart }
              ].map((metric) => (
                <div key={index} className="bg-[#16181d] p-4 rounded-lg">
                  <div className="text-sm text-gray-400 mb-1">{metric.label}</div>
                  <div className="text-2xl font-semibold text-purple-500">{metric.value}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#16181d] p-8 rounded-lg mb-6">
            <h2 className="text-xl text-gray-400 font-semibold text-center mb-8">
              Number of Restart per Iteration
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-10 gap-4">
              {restartSteps.map((step) => (
                <div
                  key={step.step}
                  className="flex flex-col items-center p-4 bg-[#1a1d24]/60 rounded-lg backdrop-blur-xl transition-transform hover:-translate-y-1"
                >
                  <div className="w-12 h-12 bg-[#16181d] rounded-xl flex items-center justify-center mb-4">
                    <RotateCcw className="w-6 h-6" />
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-gray-400 mb-1">Step {step.step}</div>
                    <div className="text-xl font-bold">{step.value}</div>
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
    </div>
  )
}
