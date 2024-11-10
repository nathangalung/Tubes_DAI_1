import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

function createNumberTexture(number) {
  const size = 128;
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const context = canvas.getContext("2d");
  if (!context) return null;

  // Set background to white for the number texture
  context.fillStyle = "#FFFFFF";
  context.fillRect(0, 0, size, size);

  // Set text color to black
  context.fillStyle = "#000000";
  context.font = "bold 70px Arial";
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillText(number.toString(), size / 2, size / 2);
  return new THREE.CanvasTexture(canvas);
}

const Cube = ({ magic_cube }) => {
  const rendererRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const containerRef = useRef(null);
  const controlsRef = useRef(null);
  const texturesRef = useRef([]);

  // Sesuaikan posisi awal kamera agar seluruh kubus terlihat jelas
  const initialCameraPosition = new THREE.Vector3(0, 0, 10);

  useEffect(() => {
    const scene = new THREE.Scene();
    scene.background = null; // Transparent background
    sceneRef.current = scene;

    const w = window.innerWidth / 2.5; // Sesuaikan ukuran frame
    const h = window.innerHeight / 2;
    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true, // Enable transparency
    });
    renderer.setClearColor(0x000000, 0); // Transparent renderer
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

    const cubeSize = 0.75;
    const spacing = 1.7;

    const parentCube = new THREE.Group();

    for (let x = 0; x < 5; x++) {
      for (let y = 0; y < 5; y++) {
        for (let z = 0; z < 5; z++) {
          const number = magic_cube[x][y][z];
          const texture = createNumberTexture(number);
          texturesRef.current.push(texture);

          const materials = Array(6).fill(
            new THREE.MeshBasicMaterial({
              color: 0xffffff, // Set cube face color to white
              map: texture,
            })
          );

          const smallCube = new THREE.Mesh(
            new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize),
            materials
          );

          smallCube.position.set(
            (x - 2) * spacing,
            (y - 2) * spacing,
            (z - 2) * spacing
          );

          parentCube.add(smallCube);
        }
      }
    }

    scene.add(parentCube);

    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      renderer.dispose();
      texturesRef.current.forEach((texture) => texture.dispose());
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
  }, [magic_cube]);

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
