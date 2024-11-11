import React, { useState, useRef, useEffect, memo } from "react";
import Cube from "./Cube";
import { X, Play, Pause } from "lucide-react";

const MemoizedCube = memo(Cube);

export default function Player({
  onClose,
  states,
  playbackSpeeds = [0.5, 1, 2, 4],
  iteration,
  restart = null,
  population = null,
  iterationRestart = [], // Array containing iteration thresholds for each restart
}) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [elapsedTime, setElapsedTime] = useState(0); // Track time in seconds
  const requestRef = useRef(null);
  const [restartCount, setRestartCount] = useState(0); // Initialize restart count

  const maxIterations = Math.min(states.length, 10000);
  const totalDuration = (maxIterations / 10000) * 1000;
  const stateDuration = 1000 / 10000;

  // Calculate the current state index based on elapsedTime and playbackSpeed
  const currentCubeStateIndex = Math.min(
    Math.floor(elapsedTime / (stateDuration / playbackSpeed)),
    maxIterations - 1
  );

  const currentCubeState = states[currentCubeStateIndex];

  useEffect(() => {
    // Check if currentCubeStateIndex has crossed the next threshold in iterationRestart
    if (iterationRestart.length > 0 && currentCubeStateIndex >= iterationRestart[0]) {
      setRestartCount((prev) => prev + 1);
      iterationRestart.shift(); // Remove the first element as it’s reached
    }
  }, [currentCubeStateIndex, iterationRestart]);

  const handlePlayPause = () => {
    setIsPlaying((prev) => !prev);
  };

  const handleProgressChange = (e) => {
    const newElapsedTime = parseFloat(e.target.value) * totalDuration / 100;
    setElapsedTime(newElapsedTime);
  };

  const handleSpeedChange = (speed) => {
    setPlaybackSpeed(speed);
  };

  const animateProgress = () => {
    setElapsedTime((prev) => {
      const newElapsedTime = prev + playbackSpeed * 0.1;
      if (newElapsedTime >= totalDuration) {
        setIsPlaying(false);
        return totalDuration;
      }
      return newElapsedTime;
    });
    requestRef.current = requestAnimationFrame(animateProgress);
  };

  useEffect(() => {
    if (isPlaying) {
      requestRef.current = requestAnimationFrame(animateProgress);
    } else {
      cancelAnimationFrame(requestRef.current);
    }
    return () => cancelAnimationFrame(requestRef.current);
  }, [isPlaying, playbackSpeed]);

  return (
    <div className="fixed inset-0 bg-[rgba(10,10,10,0.8)] flex justify-center items-center z-50">
      <div className="relative bg-[#16181d] p-6 rounded-lg w-[85%] max-w-[1000px] flex flex-col items-center">
        <button
          onClick={onClose}
          className="absolute top-0 right-0 mt-2 mr-2 z-50 text-white hover:text-gray-400 transition"
        >
          <X className="w-6 h-6" />
        </button>

        <div className="relative w-full h-[400px] bg-[#1a1d24] rounded-lg flex justify-center items-center overflow-hidden mb-4">
          <MemoizedCube key={`player-cube-${currentCubeStateIndex}`} magic_cube={currentCubeState} />
        </div>

        <input
          type="range"
          min="0"
          max="100"
          value={(elapsedTime / totalDuration) * 100}
          onChange={handleProgressChange}
          className="w-full mb-2"
        />

        <div className="flex items-center justify-center gap-4 mt-4">
          <button
            onClick={handlePlayPause}
            className="p-3 bg-[#8b5cf6] rounded-full text-white hover:bg-[#7a4bd1] transition"
          >
            {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
          </button>

          {playbackSpeeds.map((speed) => (
            <button
              key={speed}
              onClick={() => handleSpeedChange(speed)}
              className={`px-3 py-1 rounded-full ${
                playbackSpeed === speed ? "bg-[#8b5cf6] text-white" : "bg-[#1a1d24] text-[#94a3b8]"
              } transition`}
            >
              {speed}x
            </button>
          ))}
        </div>

        <div className="absolute bottom-4 left-4 text-white text-sm">
          Iteration: {currentCubeStateIndex}
        </div>
        {population !== null && (
          <div className="absolute bottom-4 right-4 text-white text-sm">
            Population: {population}
          </div>
        )}
        {restart !== null && (
          <div className="absolute bottom-4 right-4 text-white text-sm">
            Restart: {restartCount}
          </div>
        )}
      </div>
    </div>
  );
}
