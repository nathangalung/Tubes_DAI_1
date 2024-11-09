document.addEventListener('DOMContentLoaded', function() {
    const initializeButton = document.getElementById('initializeCube');
    const objectiveValue = document.getElementById('objectiveValue');
    const previewCanvas = document.getElementById('previewCube');
    
    function drawCubePreview(canvas) {
        const ctx = canvas.getContext('2d');
        const width = canvas.offsetWidth;
        const height = canvas.offsetHeight;
        
        // Set canvas size with proper scaling
        canvas.width = width * window.devicePixelRatio;
        canvas.height = height * window.devicePixelRatio;
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        
        // Clear canvas
        ctx.fillStyle = '#1a1d24';
        ctx.fillRect(0, 0, width, height);
        
        // Draw cube visualization (placeholder)
        const centerX = width / 2;
        const centerY = height / 2;
        const size = Math.min(width, height) * 0.4;
        
        // Draw cube faces with perspective
        ctx.strokeStyle = '#4f46e5';
        ctx.lineWidth = 2;
        
        // Front face
        ctx.beginPath();
        ctx.moveTo(centerX - size/2, centerY - size/2);
        ctx.lineTo(centerX + size/2, centerY - size/2);
        ctx.lineTo(centerX + size/2, centerY + size/2);
        ctx.lineTo(centerX - size/2, centerY + size/2);
        ctx.closePath();
        ctx.stroke();
        
        // Add some random numbers
        ctx.font = '14px Space Grotesk';
        ctx.fillStyle = '#94a3b8';
        ctx.textAlign = 'center';
        
        for(let i = 0; i < 9; i++) {
            const x = centerX - size/3 + (i % 3) * size/3;
            const y = centerY - size/3 + Math.floor(i/3) * size/3;
            ctx.fillText(Math.floor(Math.random() * 100), x, y);
        }
    }
    
    function updateObjectiveValue() {
        const newValue = Math.floor(Math.random() * 5000 + 5000);
        objectiveValue.textContent = newValue;
        
        // Animate the value change
        objectiveValue.style.color = '#4f46e5';
        setTimeout(() => {
            objectiveValue.style.color = 'inherit';
        }, 300);
    }
    
    if(initializeButton && previewCanvas) {
        // Initial draw
        drawCubePreview(previewCanvas);
        
        // Handle click
        initializeButton.addEventListener('click', () => {
            drawCubePreview(previewCanvas);
            updateObjectiveValue();
        });
    }
    
    document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to algorithm cards
    const algorithmCards = document.querySelectorAll('.algorithm-card');
    algorithmCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'scale(1.02)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'scale(1)';
        });
    });
});
});