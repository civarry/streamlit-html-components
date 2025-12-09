// Demo Button JavaScript
(function() {
    console.log('🚀 Demo Button Loaded');
    
    let clickCount = 0;
    
    // Function receives initial count from onclick attribute
    window.handleDemoClick = function(initialCount = 0) {
        if (clickCount === 0) {
            // First click: initialize from parameter
            clickCount = initialCount;
        }
        
        clickCount++;
        
        // Update UI
        document.getElementById('click-count').textContent = clickCount;
        document.getElementById('demo-status').textContent = `Clicked ${clickCount} time(s)!`;
        document.getElementById('demo-status').style.background = '#dbeafe';
        document.getElementById('demo-status').style.color = '#1e40af';
        
        // Visual feedback
        const button = document.querySelector('.demo-button');
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = '';
        }, 200);
        
        // Send event to Streamlit
        if (typeof window.sendToStreamlit === 'function') {
            window.sendToStreamlit('demo_click', {
                count: clickCount,
                timestamp: new Date().toISOString(),
                button_id: 'demo_button'
            });
        }
        
        // Ripple effect
        createRipple(button);
    };
    
    function createRipple(button) {
        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        `;
        
        const size = Math.max(button.offsetWidth, button.offsetHeight);
        const rect = button.getBoundingClientRect();
        
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${event.clientX - rect.left - size / 2}px`;
        ripple.style.top = `${event.clientY - rect.top - size / 2}px`;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }
    
    // Add ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    console.log('✨ Demo button ready');
})();