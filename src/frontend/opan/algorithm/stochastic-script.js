document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('progressChart');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        const container = canvas.parentElement;
        canvas.width = container.clientWidth;
        canvas.height = 300;
        drawChart();
    }

    function drawChart() {
        const width = canvas.width;
        const height = canvas.height;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw grid
        ctx.strokeStyle = '#1e1e1e';
        ctx.lineWidth = 1;
        
        // Vertical grid lines
        for (let i = 0; i < width; i += 40) {
            ctx.beginPath();
            ctx.moveTo(i, 0);
            ctx.lineTo(i, height);
            ctx.stroke();
        }
        
        // Horizontal grid lines
        for (let i = 0; i < height; i += 40) {
            ctx.beginPath();
            ctx.moveTo(0, i);
            ctx.lineTo(width, i);
            ctx.stroke();
        }

        // Draw progress line
        ctx.strokeStyle = '#8b5cf6';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, height);
        
        // Create a curve that starts high and decreases
        for (let x = 0; x < width; x++) {
            const progress = x / width;
            const y = height * (0.2 + Math.exp(-progress * 3) * 0.6);
            ctx.lineTo(x, y);
        }
        ctx.stroke();
    }

    // Initial setup
    resizeCanvas();
    
    // Handle window resize
    window.addEventListener('resize', resizeCanvas);
});