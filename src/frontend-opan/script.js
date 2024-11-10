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

// Initialize each canvas for the algorithms
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

// Function to save cube state to localStorage
function saveCubeState(data) {
    localStorage.setItem('cubeData', JSON.stringify(data));
}

// Function to load cube state from localStorage
function loadCubeState() {
    const cubeData = localStorage.getItem('cubeData');
    return cubeData ? JSON.parse(cubeData) : null;
}

// Display cube data on a specific canvas
function displayCube(data, canvasId) {
    if (!data) return;

    const scene = scenes[canvasId];
    const renderer = renderers[canvasId];
    const camera = cameras[canvasId];

    // Clear previous cube
    while (scene.children.length > 0) {
        scene.remove(scene.children[0]);
    }

    const N = data.length;
    const cubeSize = 1.5;
    const offset = (N - 1) / 2;
    const color = '#800080';

    // Create the cube visualization
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

// Function to initialize a random cube
async function initializeCube() {
    console.log("Initializing cube...");  // Debugging log
    try {
        const response = await fetch('http://127.0.0.1:8000/initialize_cube');
        if (!response.ok) throw new Error(`Failed to initialize cube: ${response.status}`);

        const data = await response.json();
        saveCubeState(data.cube);
        displayCube(data.cube, 'init-cube-canvas');
    } catch (error) {
        console.error("Error in initializeCube:", error);
    }
}

// Event listener for initialize cube button
document.getElementById('initialize-cube').addEventListener('click', (event) => {
    event.preventDefault();  // Prevent any default refresh behavior
    initializeCube();
});

// Function to run a specific algorithm and display its plot
async function runAlgorithm(algorithm, canvasId, plotContainerId) {
    console.log(`Running algorithm: ${algorithm}`);  // Debugging log
    try {
        const savedCube = loadCubeState();
        if (!savedCube) {
            console.error("Cube data not found. Please initialize the cube first.");
            return;
        }

        const response = await fetch(`http://127.0.0.1:8000/run_algorithm_with_plot`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                algorithm: algorithm,
                cube: savedCube
            })
        });

        if (!response.ok) throw new Error(`Failed to run ${algorithm}`);

        const blob = await response.blob();
        const img = document.createElement('img');
        img.src = URL.createObjectURL(blob);
        img.alt = `${algorithm} Objective Function Plot`;
        img.style.width = '100%';

        const plotContainer = document.getElementById(plotContainerId);
        plotContainer.innerHTML = '';
        plotContainer.appendChild(img);
    } catch (error) {
        console.error(`Error running ${algorithm}:`, error);
    }
}