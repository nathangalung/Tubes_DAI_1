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

// Fungsi untuk menyimpan data cube di local storage
function saveCubeState(data) {
    localStorage.setItem('cubeData', JSON.stringify(data));
}

// Fungsi untuk memuat data cube dari local storage
function loadCubeState() {
    const cubeData = localStorage.getItem('cubeData');
    return cubeData ? JSON.parse(cubeData) : null;
}

async function initializeCube() {
    console.log("Initializing cube...");
    try {
        const response = await fetch('http://127.0.0.1:8000/initialize_cube');
        
        if (!response.ok) throw new Error(`Failed to initialize cube: ${response.status}`);

        const data = await response.json();
        console.log("Cube initialized:", data);
        
        saveCubeState(data.cube); // Simpan data cube setelah inisialisasi
        displayCube(data.cube, 'init-cube-canvas');
    } catch (error) {
        console.error("Error in initializeCube:", error);
    }
}

document.getElementById('initialize-cube').addEventListener('click', initializeCube);

async function runAlgorithm(algorithm, canvasId) {
    try {
        const savedCube = loadCubeState();
        if (!savedCube) {
            console.error("Cube data not found. Please initialize the cube first.");
            return;
        }

        // Kirim permintaan untuk menjalankan algoritma dengan plot
        const response = await fetch(`http://127.0.0.1:8000/run_algorithm_with_plot`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                algorithm: algorithm,
                cube: savedCube
            })
        });

        if (!response.ok) throw new Error(`Failed to run ${algorithm}`);

        // Ambil hasil plot sebagai gambar dan tampilkan
        const blob = await response.blob();
        const img = document.createElement('img');
        img.src = URL.createObjectURL(blob);
        img.alt = "Plot Nilai Objective Function per Iterasi";
        img.style.width = '100%';

        const plotContainer = document.getElementById('steepest-plot-container');
        plotContainer.innerHTML = ''; // Bersihkan konten sebelumnya
        plotContainer.appendChild(img);
    } catch (error) {
        console.error(`Error running ${algorithm}:`, error);
    }
}

function displayCube(data, canvasId) {
    if (!data) {
        console.error(`No cube data to display for ${canvasId}`);
        return;
    }

    const scene = scenes[canvasId];
    const renderer = renderers[canvasId];
    const camera = cameras[canvasId];

    while (scene.children.length > 0) {
        scene.remove(scene.children[0]);
    }

    const N = data.length;
    const cubeSize = 1.5;
    const offset = (N - 1) / 2;
    const color = '#800080';

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
