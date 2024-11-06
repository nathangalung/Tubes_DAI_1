const canvasIds = [
    'init-cube-canvas',
    'steepest-cube-canvas',
    'sideways-cube-canvas',
    'random-cube-canvas',
    'stochastic-cube-canvas',
    'annealing-cube-canvas',
    'genetic-cube-canvas'
];

const scenes = {};
const cameras = {};
const renderers = {};

// Initialize Three.js for each canvas
canvasIds.forEach((id) => {
    const canvas = document.getElementById(id);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas });
    renderer.setSize(400, 400);
    renderer.setClearColor(0x000000);

    camera.position.set(7, 7, 10);
    camera.lookAt(0, 0, 0);

    scenes[id] = scene;
    cameras[id] = camera;
    renderers[id] = renderer;
});

// Store cube state in localStorage to maintain across page reloads
function saveCubeState(data) {
    localStorage.setItem('cubeData', JSON.stringify(data));
}

function loadCubeState() {
    const cubeData = localStorage.getItem('cubeData');
    return cubeData ? JSON.parse(cubeData) : null;
}

// Remove cube state from localStorage on page load or backend restart
function clearCubeState() {
    localStorage.removeItem('cubeData');
}

// Show loading spinner for specific canvas
function showSpinner(canvasId) {
    document.getElementById(`${canvasId}-spinner`).style.display = 'flex';
}

// Hide loading spinner for specific canvas
function hideSpinner(canvasId) {
    document.getElementById(`${canvasId}-spinner`).style.display = 'none';
}

// Display cube function for rendering
function displayCube(data, canvasId) {
    if (!data) {
        console.error(`No cube data to display for ${canvasId}`);
        return;
    }

    const scene = scenes[canvasId];
    const renderer = renderers[canvasId];
    const camera = cameras[canvasId];

    // Clear previous cube objects
    while (scene.children.length > 0) {
        scene.remove(scene.children[0]);
    }

    const N = data.length;
    const cubeSize = 1.5;
    const offset = (N - 1) / 2;
    const color = '#800080';

    // Render each layer of the cube as blocks
    for (let x = 0; x < N; x++) {
        for (let y = 0; y < N; y++) {
            for (let z = 0; z < N; z++) {
                const value = data[x][y][z];

                const canvas = document.createElement('canvas');
                canvas.width = 128;
                canvas.height = 128;
                const context = canvas.getContext('2d');
                context.fillStyle = color;
                context.fillRect(0, 0, canvas.width, canvas.height);
                context.fillStyle = '#FFFFFF';
                context.font = '40px Arial';
                context.textAlign = 'center';
                context.textBaseline = 'middle';
                context.fillText(value, canvas.width / 2, canvas.height / 2);

                const texture = new THREE.CanvasTexture(canvas);
                const material = new THREE.MeshBasicMaterial({ map: texture });
                const geometry = new THREE.BoxGeometry(cubeSize * 0.9, cubeSize * 0.9, cubeSize * 0.9);
                const cube = new THREE.Mesh(geometry, material);
                cube.position.set(x - offset, y - offset, z - offset);
                scene.add(cube);
            }
        }
    }
    renderer.render(scene, camera);
}

async function initializeCube() {
    console.log("Initializing cube...");
    try {
        const response = await fetch('http://127.0.0.1:8000/initialize_cube');
        
        if (!response.ok) {
            throw new Error(`Failed to initialize cube: ${response.status}`);
        }

        const data = await response.json();
        console.log("Cube initialized:", data);

        saveCubeState(data.cube);
        displayCube(data.cube, 'init-cube-canvas');

        // Automatically run all algorithms after initializing the cube
        await runAllAlgorithms(data.cube);
    } catch (error) {
        console.error("Error in initializeCube:", error);
    }
}

// Run all algorithms asynchronously after initializing cube
async function runAllAlgorithms(cubeData) {
    try {
        canvasIds.slice(1).forEach(id => showSpinner(id)); // Show spinner for each algorithm canvas

        const response = await fetch('http://127.0.0.1:8000/run_all_algorithms', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cube: cubeData })
        });

        if (!response.ok) throw new Error("Failed to run all algorithms");

        await Promise.all([
            displayAlgorithmResult('steepest_ascent', 'steepest-cube-canvas'),
            displayAlgorithmResult('sideways_move', 'sideways-cube-canvas'),
            displayAlgorithmResult('random_restart', 'random-cube-canvas'),
            displayAlgorithmResult('stochastic', 'stochastic-cube-canvas'),
            displayAlgorithmResult('simulated_annealing', 'annealing-cube-canvas'),
            displayAlgorithmResult('genetic', 'genetic-cube-canvas')
        ]);

    } catch (error) {
        console.error("Error running all algorithms:", error);
    } finally {
        canvasIds.slice(1).forEach(id => hideSpinner(id)); // Hide all spinners after algorithms complete
    }
}

// Fetch and display algorithm results
async function displayAlgorithmResult(algorithm, canvasId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/get_algorithm_result/${algorithm}`);
        
        if (!response.ok) throw new Error(`Failed to fetch result for ${algorithm}`);

        const result = await response.json();
        displayCube(result.cube, canvasId);
    } catch (error) {
        console.error(`Error displaying result for ${algorithm}:`, error);
    } finally {
        hideSpinner(canvasId); // Hide spinner after displaying result
    }
}

// Load state when page loads
window.addEventListener('load', () => {
    clearCubeState(); // Clear saved state on page load
    const savedCube = loadCubeState();
    if (savedCube) displayCube(savedCube, 'init-cube-canvas');
});

document.getElementById('initialize-cube').addEventListener('click', initializeCube);
