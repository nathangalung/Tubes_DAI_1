document.addEventListener('DOMContentLoaded', function() {
    // Initialize UI elements
    const initializeButton = document.getElementById('initializeCube');
    const solveButton = document.getElementById('solveCube');
    const solutionCost = document.getElementById('solutionCost');
    const timeElapsed = document.getElementById('timeElapsed');
    const movesMade = document.getElementById('movesMade');
    
    let solving = false;
    let startTime;

    // Initialize cube visualization canvases
    const initialCanvas = document.getElementById('initialCube');
    const solutionCanvas = document.getElementById('solutionCube');

    // Event listeners
    initializeButton.addEventListener('click', function() {
        initializeCube();
        solveButton.disabled = false;
        resetMetrics();
    });

    solveButton.addEventListener('click', function() {
        if (!solving) {
            startSolving();
        }
    });

    function initializeCube() {
        // Clear previous state
        clearCanvas(initialCanvas);
        clearCanvas(solutionCanvas);
        
        // Draw random initial state
        drawRandomCube(initialCanvas);
        
        // Enable solve button
        solveButton.disabled = false;
    }

    function startSolving() {
        solving = true;
        startTime = Date.now();
        solveButton.disabled = true;
        
        // Simulate solving process with animation
        let progress = 0;
        const interval = setInterval(() => {
            progress += 1;
            updateMetrics(progress);
            
            if (progress >= 100) {
                clearInterval(interval);
                solving = false;
                solveButton.disabled = false;
                drawSolvedCube(solutionCanvas);
            }
        }, 50);
    }

    function updateMetrics(progress) {
        const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
        const moves = Math.floor(progress * 1.2);
        const cost = Math.floor(progress * 2.5);

        timeElapsed.textContent = elapsed + 's';
        movesMade.textContent = moves;
        solutionCost.textContent = cost;
    }

    function resetMetrics() {
        timeElapsed.textContent = '0.00s';
        movesMade.textContent = '0';
        solutionCost.textContent = '0';
    }

    function clearCanvas(canvas) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    function drawRandomCube(canvas) {
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#f0f0f0';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Add placeholder text
        ctx.fillStyle = '#666';
        ctx.font = '14px Inter';
        ctx.textAlign = 'center';
        ctx.fillText('Random Cube State', canvas.width/2, canvas.height/2);
    }

    function drawSolvedCube(canvas) {
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#e0ffe0';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Add placeholder text
        ctx.fillStyle = '#666';
        ctx.font = '14px Inter';
        ctx.textAlign = 'center';
        ctx.fillText('Solved Cube State', canvas.width/2, canvas.height/2);
    }

    // Initialize the page
    resetMetrics();
});