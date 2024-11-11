import React, { useState, useRef, useEffect, memo } from "react";
import Cube from "./Cube";
import { X, Play, Pause } from "lucide-react";

const MemoizedCube = memo(Cube);

export default function Player({
  onClose,
  states,
  playbackSpeeds = [0.5, 1, 2, 4],
  iteration,
  population = null,
  restart = null,
}) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [elapsedTime, setElapsedTime] = useState(0); // Track time in seconds
  const requestRef = useRef(null);
  
  const maxIterations = Math.min(states.length, 10000);
  const totalDuration = (maxIterations / 10000) * 1000; // Adjust total duration based on the number of states
  const stateDuration = 1000 / 10000; // 0.1 seconds per state at 1x speed

  // Calculate the current state index based on elapsedTime and playbackSpeed
  const currentCubeStateIndex = Math.min(
    Math.floor(elapsedTime / (stateDuration / playbackSpeed)),
    maxIterations - 1
  );
  const currentCubeState = states[currentCubeStateIndex];

  const handlePlayPause = () => {
    setIsPlaying((prev) => !prev);
  };

  const handleSpeedChange = (speed) => {
    setPlaybackSpeed(speed);
  };

  // Update elapsedTime and handle playback
  const animateProgress = (timestamp) => {
    requestRef.current = requestAnimationFrame(animateProgress);
    setElapsedTime((prevElapsedTime) => {
      const newElapsedTime = prevElapsedTime + 0.0167 * playbackSpeed; // 0.0167 ~ 1 frame at 60fps
      if (newElapsedTime >= totalDuration) {
        setIsPlaying(false);
        cancelAnimationFrame(requestRef.current);
        return totalDuration;
      }
      return newElapsedTime;
    });
  };

  // Start or stop animation
  useEffect(() => {
    if (isPlaying) {
      requestRef.current = requestAnimationFrame(animateProgress);
    } else {
      cancelAnimationFrame(requestRef.current);
    }
    return () => cancelAnimationFrame(requestRef.current);
  }, [isPlaying, playbackSpeed]);

  // Reset elapsedTime when playback is stopped or speed is changed
  useEffect(() => {
    if (!isPlaying) {
      setElapsedTime(0); // Reset time if playback is paused or stopped
    }
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
          <MemoizedCube magic_cube={currentCubeState} fetchCubeData={false} />
        </div>

        <input
          type="range"
          min="0"
          max={totalDuration}
          value={elapsedTime}
          onChange={(e) => setElapsedTime(Number(e.target.value))}
          className="w-full mb-4"
        />

        <div className="flex items-center justify-center gap-4 mt-2 mb-4">
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

        {/* Display time and iteration with improved spacing and formatting */}
        <div className="flex justify-between w-full px-6 text-white text-sm">
          <div>
            Time: {elapsedTime.toFixed(2)}s / {totalDuration.toFixed(2)}s
          </div>
          <div>
            Iteration: {currentCubeStateIndex}
          </div>
        </div>

        {population !== null && (
          <div className="absolute bottom-4 right-4 text-white text-sm">
            Population: {population}
          </div>
        )}
        {restart !== null && (
          <div className="absolute bottom-4 right-16 text-white text-sm">
            Restart: {restart}
          </div>
        )}
      </div>
    </div>
  );
}
