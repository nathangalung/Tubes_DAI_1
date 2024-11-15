import React from "react";
import Cube from "./Cube";
import { saveAs } from "file-saver";

export default function Main({ onAlgorithmSelect, initialCube, initialCost, onInitialize, isLoading, onLoadCube }) {
  const handleLoadCube = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const loadedCube = JSON.parse(e.target.result);
        if (loadedCube.magic_cube) {
          onLoadCube(loadedCube.magic_cube); // Ensure we're passing only the cube data to `onLoadCube`
        } else {
          alert("Invalid file format. Please upload a valid cube JSON file.");
        }
      };
      reader.readAsText(file);
    }
  };

  const handleSaveCube = () => {
    const blob = new Blob([JSON.stringify({ magic_cube: initialCube })], { type: "application/json" });
    saveAs(blob, "magic_cube.json");
  };

  return (
    <div className="bg-[#0a0a0a] text-white font-['Space_Grotesk',system-ui,sans-serif]">
      <nav className="fixed top-0 left-0 right-0 bg-[rgba(10,10,10,0.8)] backdrop-blur-[12px] border-b border-[#2d3748] z-50">
        <div className="max-w-[1200px] mx-auto px-6 flex justify-between items-center h-16">
          <div className="font-bold text-xl">Magic Cube Solver</div>
        </div>
      </nav>

      <main>
        <section className="pt-32 pb-16">
          <div className="max-w-[1200px] mx-auto px-6">
            <div className="max-w-[900px] mx-auto text-center">
              <h1 className="text-6xl font-extrabold leading-tight mb-6 bg-gradient-to-r from-[#4f46e5] via-[#8b5cf6] to-[#d946ef] text-transparent bg-clip-text">
                Solve Magic Cube,<br />Your Way.
              </h1>
              <p className="text-xl text-[#94a3b8] mb-8 max-w-[600px] mx-auto">
                Explore a world of solutions for your Magic Cube with our solver. 
                Visualize, learn, and apply different algorithms tailored to your solving style.
              </p>
              
              <div className="bg-[#111318] rounded-2xl p-6 max-w-[600px] mx-auto">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-2 h-2 rounded-full bg-[#6366f1]" />
                  <h3 className="font-semibold">Initial State Cube</h3>
                </div>

                {!initialCube ? (
                  <div className="h-[357px] flex items-center justify-center text-[#94a3b8]">
                    <button 
                      onClick={onInitialize}
                      disabled={isLoading}
                      className="bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
                    >
                      {isLoading ? 'Loading...' : 'Initialize Random Cube'}
                    </button>
                  </div>
                ) : (
                  <>
                    <Cube magic_cube={initialCube} />
                    <div className="text-sm text-[#94a3b8] mt-4">
                      Initial State Cost: <strong>{initialCost}</strong>
                    </div>
                    <div className="flex gap-2 mt-4 justify-center">
                      <input
                        type="file"
                        accept="application/json"
                        onChange={handleLoadCube}
                        className="hidden"
                        id="loadCubeInput"
                      />
                      <button
                        onClick={() => document.getElementById("loadCubeInput").click()}
                        className="bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
                      >
                        Load Cube
                      </button>
                      <button
                        onClick={handleSaveCube}
                        className="bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
                      >
                        Save Cube
                      </button>
                      <button 
                        onClick={onInitialize}
                        disabled={isLoading}
                        className="bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
                      >
                        {isLoading ? 'Loading...' : 'Initialize Random Cube'}
                      </button>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </section>

        <section className="py-12">
          <div className="max-w-[1200px] mx-auto px-6">
            <h2 className="text-4xl font-bold text-center mb-8">Choose Your Algorithm</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { id: "steepest", name: "Steepest Ascent", icon: "▲", desc: "Optimal path finding algorithm" },
                { id: "sideways", name: "Sideways Move", icon: "↔", desc: "Flexible movement patterns" },
                { id: "stochastic", name: "Stochastic", icon: "⚄", desc: "Randomized solution approach" },
                { id: "random", name: "Random Restart", icon: "↺", desc: "Multiple starting points" },
                { id: "simulated", name: "Simulated Annealing", icon: "🌡", desc: "Temperature-based solving" },
                { id: "genetic", name: "Genetic", icon: "🧬", desc: "Evolution-inspired solution" }
              ].map(algo => (
                <button
                  key={algo.id}
                  onClick={() => onAlgorithmSelect(algo.id)}
                  disabled={!initialCube || isLoading}
                  className="bg-[#111318] border border-[#2d3748] rounded-2xl p-6 text-left w-full hover:border-[#8b5cf6] hover:shadow-lg hover:shadow-[#8b5cf6]/10 transition-all duration-300 transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div className="text-3xl mb-4 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-transparent bg-clip-text">
                    {algo.icon}
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{algo.name}</h3>
                  <p className="text-[#94a3b8] text-sm">{algo.desc}</p>
                </button>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="py-8 bg-[#0a0a0a] border-t border-[#2d3748] text-center text-[#94a3b8]">
        <div className="max-w-[1200px] mx-auto px-6">
          <p>&copy; 2024 Magic Cube Solver. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
