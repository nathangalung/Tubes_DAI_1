const canvasIds = [
    'init-cube-canvas',
    'steepest-cube-canvas',
    'sideway-cube-canvas',
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
    renderer.setSize(400, 400); // Increased canvas size for better visibility
    renderer.setClearColor(0x000000); // Set canvas background to black

    camera.position.set(7, 7, 10); // Adjusted for a better view of the cube
    camera.lookAt(0, 0, 0);

    scenes[id] = scene;
    cameras[id] = camera;
    renderers[id] = renderer;
});

let cubeData = null;

async function initializeCube() {
    try {
        const response = await fetch('http://127.0.0.1:8000/initialize_cube');
        if (!response.ok) throw new Error("Failed to fetch cube data");

        const data = await response.json();
        cubeData = data.cube;

        console.log("Initialized Cube Data:", cubeData);
        displayCube(cubeData, 'init-cube-canvas'); // Display initialized cube

        // Automatically run all algorithms after initializing the cube
        await runAllAlgorithms();
    } catch (error) {
        console.error("Error initializing cube:", error);
    }
}

async function runAllAlgorithms() {
    const algorithmEndpoints = [
        // { id: 'steepest-cube-canvas', endpoint: '/steepest_ascent' },
        // { id: 'sideway-cube-canvas', endpoint: '/sideways_move' },
        // { id: 'random-cube-canvas', endpoint: '/random_restart' },
        { id: 'stochastic-cube-canvas', endpoint: '/stochastic' },
        { id: 'annealing-cube-canvas', endpoint: '/simulated_annealing' },
        // { id: 'genetic-cube-canvas', endpoint: '/genetic' }
    ];

    for (const { id, endpoint } of algorithmEndpoints) {
        displayLoading(id); // Show loading indicator

        try {
            const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cube: cubeData })
            });

            if (!response.ok) throw new Error("Failed to run algorithm");

            const result = await response.json();
            console.log(`Algorithm Result for ${id}:`, result);

            displayCube(result.cube, id); // Display cube result after algorithm completes
        } catch (error) {
            console.error(`Error running ${endpoint} algorithm:`, error);
        }
    }
}

function displayCube(data, canvasId) {
    const scene = scenes[canvasId];
    const renderer = renderers[canvasId];
    const camera = cameras[canvasId];

    // Clear previous objects
    while (scene.children.length > 0) {
        scene.remove(scene.children[0]);
    }

    const N = data.length;
    const cubeSize = 1.5; // Increased cube size for better visibility
    const offset = (N - 1) / 2;
    const color = '#800080'; // Purple color for all cubes

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

function displayLoading(canvasId) {
    const scene = scenes[canvasId];
    const renderer = renderers[canvasId];
    const camera = cameras[canvasId];

    // Clear previous objects
    while (scene.children.length > 0) {
        scene.remove(scene.children[0]);
    }

    // Create a static "Loading..." texture for the loading indicator
    const loaderText = document.createElement('canvas');
    loaderText.width = 256;
    loaderText.height = 256;
    const context = loaderText.getContext('2d');
    context.fillStyle = '#800080';
    context.fillRect(0, 0, loaderText.width, loaderText.height);
    context.fillStyle = '#FFFFFF';
    context.font = '24px Arial';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText("Loading...", loaderText.width / 2, loaderText.height / 2);

    const texture = new THREE.CanvasTexture(loaderText);
    const material = new THREE.MeshBasicMaterial({ map: texture });
    const plane = new THREE.PlaneGeometry(4, 4); // Increased size for visibility
    const mesh = new THREE.Mesh(plane, material);

    scene.add(mesh);
    renderer.render(scene, camera);
}

// Add event listener to initialize cube on button click
document.getElementById('initialize-cube').addEventListener('click', initializeCube);
