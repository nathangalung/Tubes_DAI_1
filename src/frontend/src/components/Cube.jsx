import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import axios from "axios";

function createNumberTexture(number) {
  const size = 128;
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const context = canvas.getContext("2d");
  if (!context) return null;

  context.fillStyle = "#FFFFFF";
  context.fillRect(0, 0, size, size);
  context.fillStyle = "#000000";
  context.font = "bold 70px Arial";
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillText(number.toString(), size / 2, size / 2);
  return new THREE.CanvasTexture(canvas);
}

const Cube = ({ magic_cube, fetchCubeData }) => {
  const rendererRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const containerRef = useRef(null);
  const controlsRef = useRef(null);
  const texturesRef = useRef([]);
  const parentCubeRef = useRef(null);
  const [cubeData, setCubeData] = useState(magic_cube);
  const [initialized, setInitialized] = useState(false);

  const initialCameraPosition = new THREE.Vector3(0, 0, 10);

  // Fetch initial cube data when component mounts
  useEffect(() => {
    const fetchInitialCube = async () => {
      try {
        const response = await axios.get("http://localhost:8000/initialize_cube");
        setCubeData(response.data.initial_cube); // Set cube data from backend
      } catch (error) {
        console.error("Error fetching initial cube data:", error);
      }
    };

    if (fetchCubeData) {
      fetchInitialCube();
    } else {
      setCubeData(magic_cube);
    }
  }, [fetchCubeData, magic_cube]);

  // Initialize scene and camera only once
  useEffect(() => {
    const scene = new THREE.Scene();
    scene.background = null;
    sceneRef.current = scene;

    const w = window.innerWidth / 2.5;
    const h = window.innerHeight / 2;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(w, h);
    rendererRef.current = renderer;

    const camera = new THREE.PerspectiveCamera(70, w / h, 0.1, 1000);
    camera.position.copy(initialCameraPosition);
    cameraRef.current = camera;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;
    controlsRef.current = controls;

    if (containerRef.current) {
      containerRef.current.appendChild(renderer.domElement);
    }

    parentCubeRef.current = new THREE.Group();
    scene.add(parentCubeRef.current);

    setInitialized(true);

    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      renderer.dispose();
      scene.traverse((object) => {
        if (object instanceof THREE.Mesh) {
          object.geometry.dispose();
          if (Array.isArray(object.material)) {
            object.material.forEach((material) => material.dispose());
          } else {
            object.material.dispose();
          }
        }
      });
      if (containerRef.current && renderer.domElement) {
        containerRef.current.removeChild(renderer.domElement);
      }
    };
  }, []);

  // Update only necessary cubes
  useEffect(() => {
    if (!initialized || !cubeData) return;

    const cubeSize = 0.75;
    const spacing = 1.7;

    cubeData.forEach((plane, x) => {
      plane.forEach((row, y) => {
        row.forEach((number, z) => {
          const texture = createNumberTexture(number);
          const materials = Array(6).fill(
            new THREE.MeshBasicMaterial({ color: 0xffffff, map: texture })
          );

          let cube = parentCubeRef.current.children.find(
            (child) => child.position.x === (x - 2) * spacing &&
                       child.position.y === (y - 2) * spacing &&
                       child.position.z === (z - 2) * spacing
          );

          if (!cube) {
            cube = new THREE.Mesh(new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize), materials);
            cube.position.set((x - 2) * spacing, (y - 2) * spacing, (z - 2) * spacing);
            parentCubeRef.current.add(cube);
          } else {
            cube.material = materials;
          }
        });
      });
    });
  }, [cubeData, initialized]);

  const resetCamera = () => {
    if (cameraRef.current && controlsRef.current) {
      cameraRef.current.position.copy(initialCameraPosition);
      cameraRef.current.lookAt(0, 0, 0);
      controlsRef.current.reset();
    }
  };

  return (
    <div className="relative flex items-center justify-center w-full h-full bg-transparent">
      <button
        onClick={resetCamera}
        className="absolute top-2 right-2 z-10 bg-black text-white px-3 py-1 rounded-lg hover:bg-gray-800 transition-colors text-sm"
      >
        Reset view
      </button>
      <div ref={containerRef} className="w-full h-full flex justify-center items-center bg-transparent overflow-hidden" />
    </div>
  );
};

export default Cube;
