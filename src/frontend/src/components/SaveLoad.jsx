import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { saveAs } from 'file-saver';

const API_URL = 'http://localhost:8000';

export default function SaveLoadPanel({ cubeData, onLoadCube }) {
  const [fileName, setFileName] = useState('');
  const [savedFiles, setSavedFiles] = useState([]);
  const [isPanelVisible, setIsPanelVisible] = useState(false);

  // Fetch saved files from backend when component mounts
  useEffect(() => {
    fetchSavedFiles();
  }, []);

  const fetchSavedFiles = async () => {
    try {
      const response = await axios.get(`${API_URL}/saved_cubes`);
      setSavedFiles(response.data);
    } catch (error) {
      console.error("Error fetching saved files:", error);
    }
  };

  const handleSave = async () => {
    if (!fileName) {
      alert("Please enter a file name.");
      return;
    }
    try {
      await axios.post(`${API_URL}/save_cube`, {
        file_name: fileName,
        cube: cubeData
      });
      setFileName('');
      fetchSavedFiles(); // Refresh the saved files list
      alert("Cube saved successfully.");
    } catch (error) {
      console.error("Error saving cube:", error);
    }
  };

  const handleLoad = async (file) => {
    try {
      const response = await axios.get(`${API_URL}/load_cube/${file}`);
      onLoadCube(response.data.cube); // Send loaded data back to parent component
      setIsPanelVisible(false); // Close panel after loading
    } catch (error) {
      console.error("Error loading cube:", error);
    }
  };

  return (
    <div className="bg-[#111318] p-4 rounded-lg">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold mb-2">Save / Load Cube</h3>
        <button
          onClick={() => setIsPanelVisible(!isPanelVisible)}
          className="bg-[#8b5cf6] text-white px-2 py-1 rounded-lg font-medium hover:opacity-90 transition-opacity"
        >
          {isPanelVisible ? 'Close' : 'Open'}
        </button>
      </div>
      {isPanelVisible && (
        <div className="mt-4">
          {/* Save Cube Section */}
          <div className="mb-4">
            <h4 className="font-medium">Save Cube</h4>
            <input
              type="text"
              placeholder="Enter filename"
              value={fileName}
              onChange={(e) => setFileName(e.target.value)}
              className="w-full mt-2 p-2 rounded bg-[#1a1d24] text-white"
            />
            <button
              onClick={handleSave}
              className="mt-2 bg-[#4ade80] text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity"
            >
              Save Cube
            </button>
          </div>

          {/* Load Cube Section */}
          <div>
            <h4 className="font-medium">Load Cube</h4>
            <ul className="text-sm text-[#94a3b8] mt-2">
              {savedFiles.map((file, index) => (
                <li key={index} className="flex justify-between items-center py-2">
                  <span>{file}</span>
                  <button
                    onClick={() => handleLoad(file)}
                    className="bg-[#8b5cf6] text-white px-2 py-1 rounded-lg font-medium hover:opacity-90 transition-opacity"
                  >
                    Load
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
