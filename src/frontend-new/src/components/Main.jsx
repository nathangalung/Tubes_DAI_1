import { useEffect, useRef, useState } from "react";
import {
  ChevronRight,
  Zap,
  RotateCcw,
  Thermometer,
  Dna,
  Box,
} from "lucide-react";
import Cube from "./Cube";

export default function Main({ onAlgorithmSelect }) {
  const [objectiveValue, setObjectiveValue] = useState(6505);
  const [cubeState, setCubeState] = useState(
    Array(5)
      .fill()
      .map(() =>
        Array(5)
          .fill()
          .map(() =>
            Array(5)
              .fill()
              .map(() => Math.floor(Math.random() * 125) + 1)
          )
      )
  );

  const generateNewCubeState = () => {
    const newState = Array(5)
      .fill()
      .map(() =>
        Array(5)
          .fill()
          .map(() =>
            Array(5)
              .fill()
              .map(() => Math.floor(Math.random() * 125) + 1)
          )
      );
    setCubeState(newState);
    return newState;
  };

  const updateObjectiveValue = () => {
    const newValue = Math.floor(Math.random() * 5000 + 5000);
    setObjectiveValue(newValue);
  };

  const handleInitialize = () => {
    const newState = generateNewCubeState();
    updateObjectiveValue();
  };

  return (
    <div className="bg-[#0a0a0a] text-white font-['Space_Grotesk',system-ui,sans-serif]">
      <nav className="fixed top-0 left-0 right-0 bg-[rgba(10,10,10,0.8)] backdrop-blur-[12px] border-b border-[#2d3748] z-50">
        <div className="max-w-[1200px] mx-auto px-6 flex justify-between items-center h-16">
          <div className="font-bold text-xl">Magic Cube Solver</div>
          <div className="flex gap-8 items-center">
            <a
              href="#"
              className="text-[#94a3b8] font-medium hover:text-white transition-colors"
            >
              Home
            </a>
            <a
              href="#"
              className="text-[#94a3b8] font-medium hover:text-white transition-colors"
            >
              About
            </a>
            <a
              href="#"
              className="text-[#94a3b8] font-medium hover:text-white transition-colors"
            >
              Help
            </a>
            <a
              href="#"
              className="bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] px-4 py-2 rounded-lg text-white font-medium"
            >
              Try Demo
            </a>
          </div>
        </div>
      </nav>
      <main>
        <section className="pt-32 pb-16">
          <div className="max-w-[1200px] mx-auto px-6">
            <div className="max-w-[900px] mx-auto text-center">
              <h1 className="text-6xl font-extrabold leading-tight mb-6 bg-gradient-to-r from-[#4f46e5] via-[#8b5cf6] to-[#d946ef] text-transparent bg-clip-text">
                Solve Magic Cube,
                <br />
                Your Way.
              </h1>
              <p className="text-xl text-[#94a3b8] mb-8 max-w-[600px] mx-auto">
                Explore a world of solutions for your Magic Cube with our
                solver. Visualize, learn, and apply different algorithms
                tailored to your solving style.
              </p>
              <div className="flex gap-4 justify-center flex-wrap mb-12">
                <span className="flex items-center gap-2 px-4 py-2 bg-[#111318] border border-[#2d3748] rounded-full text-[#94a3b8] text-sm">
                  <Box className="w-5 h-5 text-[#8b5cf6]" />
                  3D Visualization
                </span>
                <span className="flex items-center gap-2 px-4 py-2 bg-[#111318] border border-[#2d3748] rounded-full text-[#94a3b8] text-sm">
                  <ChevronRight className="w-5 h-5 text-[#8b5cf6]" />
                  Multiple Algorithms
                </span>
                <span className="flex items-center gap-2 px-4 py-2 bg-[#111318] border border-[#2d3748] rounded-full text-[#94a3b8] text-sm">
                  <Zap className="w-5 h-5 text-[#8b5cf6]" />
                  Real-time Solving
                </span>
              </div>
              <div className="bg-[#111318] rounded-2xl p-6 max-w-[600px] mx-auto">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-2 h-2 rounded-full bg-[#6366f1]" />
                  <h3 className="font-semibold">Initial Cube State</h3>
                </div>
                <Cube magic_cube={cubeState} />
                <div className="flex justify-between items-center text-sm text-[#94a3b8]">
                  <span>
                    Initial State Objective Function:{" "}
                    <strong>{objectiveValue}</strong>
                  </span>
                  <button className="bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity">
                    Initialize New State
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section className="py-12">
          <div className="max-w-[1200px] mx-auto px-6">
            <h2 className="text-4xl font-bold text-center mb-8">
              Choose Your Algorithm
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <a
                onClick={(e) => {
                  e.preventDefault();
                  onAlgorithmSelect("steepest", cubeState);
                }}
                href="#"
                className="bg-[#111318] border border-[#2d3748] rounded-2xl p-6 text-white no-underline hover:border-[#8b5cf6] hover:shadow-lg hover:shadow-[#8b5cf6]/10 transition-all duration-300 transform hover:-translate-y-1"
              >
                <div className="text-3xl mb-4 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-transparent bg-clip-text">
                  ▲
                </div>
                <h3 className="text-xl font-semibold mb-2">Steepest Ascent</h3>
                <p className="text-[#94a3b8] text-sm">
                  Optimal path finding algorithm
                </p>
              </a>
              <a
                onClick={(e) => {
                  e.preventDefault();
                  onAlgorithmSelect("sideways", cubeState);
                }}
                href="#"
                className="bg-[#111318] border border-[#2d3748] rounded-2xl p-6 text-white no-underline hover:border-[#8b5cf6] hover:shadow-lg hover:shadow-[#8b5cf6]/10 transition-all duration-300 transform hover:-translate-y-1"
              >
                <div className="text-3xl mb-4 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-transparent bg-clip-text">
                  ↔
                </div>
                <h3 className="text-xl font-semibold mb-2">Sideways Move</h3>
                <p className="text-[#94a3b8] text-sm">
                  Flexible movement patterns
                </p>
              </a>
              <a
                onClick={(e) => {
                  e.preventDefault();
                  onAlgorithmSelect("stochastic", cubeState);
                }}
                href="#"
                className="bg-[#111318] border border-[#2d3748] rounded-2xl p-6 text-white no-underline hover:border-[#8b5cf6] hover:shadow-lg hover:shadow-[#8b5cf6]/10 transition-all duration-300 transform hover:-translate-y-1"
              >
                <div className="text-3xl mb-4 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-transparent bg-clip-text">
                  ⚄
                </div>
                <h3 className="text-xl font-semibold mb-2">Stochastic</h3>
                <p className="text-[#94a3b8] text-sm">
                  Randomized solution approach
                </p>
              </a>
              <a
                onClick={(e) => {
                  e.preventDefault();
                  onAlgorithmSelect("random", cubeState);
                }}
                href="#"
                className="bg-[#111318] border border-[#2d3748] rounded-2xl p-6 text-white no-underline hover:border-[#8b5cf6] hover:shadow-lg hover:shadow-[#8b5cf6]/10 transition-all duration-300 transform hover:-translate-y-1"
              >
                <RotateCcw className="w-8 h-8 mb-4 text-[#6366f1]" />
                <h3 className="text-xl font-semibold mb-2">Random Restart</h3>
                <p className="text-[#94a3b8] text-sm">
                  Multiple starting points
                </p>
              </a>
              <a
                onClick={(e) => {
                  e.preventDefault();
                  onAlgorithmSelect("simulated", cubeState);
                }}
                href="#"
                className="bg-[#111318] border border-[#2d3748] rounded-2xl p-6 text-white no-underline hover:border-[#8b5cf6] hover:shadow-lg hover:shadow-[#8b5cf6]/10 transition-all duration-300 transform hover:-translate-y-1"
              >
                <Thermometer className="w-8 h-8 mb-4 text-[#6366f1]" />
                <h3 className="text-xl font-semibold mb-2">
                  Simulated Annealing
                </h3>
                <p className="text-[#94a3b8] text-sm">
                  Temperature-based solving
                </p>
              </a>
              <a
                onClick={(e) => {
                  e.preventDefault();
                  onAlgorithmSelect("genetic", cubeState);
                }}
                href="#"
                className="bg-[#111318] border border-[#2d3748] rounded-2xl p-6 text-white no-underline hover:border-[#8b5cf6] hover:shadow-lg hover:shadow-[#8b5cf6]/10 transition-all duration-300 transform hover:-translate-y-1"
              >
                <Dna className="w-8 h-8 mb-4 text-[#6366f1]" />
                <h3 className="text-xl font-semibold mb-2">
                  Genetic Algorithm
                </h3>
                <p className="text-[#94a3b8] text-sm">
                  Evolution-inspired solution
                </p>
              </a>
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
