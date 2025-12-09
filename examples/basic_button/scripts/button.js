// Button click counter and event handling
(function() {
    let clickCount = 0;

    function handleButtonClick() {
        clickCount++;

        // Update counter if it exists
        const counter = document.getElementById('counter');
        if (counter) {
            counter.textContent = `Clicks: ${clickCount}`;
        }

        // Send event to Python (if bridge is available)
        if (typeof window.sendToStreamlit === 'function') {
            window.sendToStreamlit('click', {
                clicks: clickCount,
                timestamp: new Date().toISOString()
            });
        }

        // Visual feedback
        const button = document.getElementById('myBtn');
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = '';
        }, 100);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            const button = document.getElementById('myBtn');
            if (button) {
                button.addEventListener('click', handleButtonClick);
            }
        });
    } else {
        const button = document.getElementById('myBtn');
        if (button) {
            button.addEventListener('click', handleButtonClick);
        }
    }
})();
