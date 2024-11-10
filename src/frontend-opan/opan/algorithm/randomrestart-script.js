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
        ctx.strokeStyle = '#2d364d';
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

        // Draw fitness curve
        ctx.strokeStyle = '#4f46e5';
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

        // Draw average fitness curve
        ctx.strokeStyle = '#22c55e';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, height * 0.8);
        
        for (let x = 0; x < width; x++) {
            const progress = x / width;
            const y = height * (0.3 + Math.exp(-progress * 2.5) * 0.4);
            ctx.lineTo(x, y);
        }
        ctx.stroke();
    }

    // Initialize restart step values with animation
    function initializeRestartSteps() {
        const steps = document.querySelectorAll('.restart-step');
        
        steps.forEach((step, index) => {
            // Add hover effect
            step.addEventListener('mouseenter', () => {
                step.style.transform = 'translateY(-5px)';
            });
            
            step.addEventListener('mouseleave', () => {
                step.style.transform = 'translateY(0)';
            });

            // Animate value counting
            const valueElement = step.querySelector('.step-value');
            if (valueElement) {
                const finalValue = 150 - (index * 7);
                let currentValue = 0;
                const duration = 1000; // 1 second
                const increment = finalValue / (duration / 16); // 60 FPS

                const updateValue = () => {
                    currentValue = Math.min(currentValue + increment, finalValue);
                    valueElement.textContent = Math.round(currentValue);

                    if (currentValue < finalValue) {
                        requestAnimationFrame(updateValue);
                    }
                };

                // Start animation after a delay based on index
                setTimeout(() => {
                    requestAnimationFrame(updateValue);
                }, index * 100);
            }
        });
    }

    // Initial setup
    resizeCanvas();
    initializeRestartSteps();
    
    // Handle window resize
    window.addEventListener('resize', resizeCanvas);
});