// Why Section JavaScript
(function() {
    console.log('🚀 Why Section Loaded');

    // Expander toggle functionality
    window.toggleExpander = function(button) {
        const content = button.nextElementSibling;
        const isActive = content.classList.contains('active');
        
        if (isActive) {
            content.classList.remove('active');
        } else {
            // Close other expanders
            document.querySelectorAll('.expander-content.active').forEach(expander => {
                if (expander !== content) {
                    expander.classList.remove('active');
                }
            });
            content.classList.add('active');
        }
    };

    // Intersection Observer for animations
    function initAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });

        document.querySelectorAll('[data-animation]').forEach(element => {
            observer.observe(element);
        });
    }

    // Initialize on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAnimations);
    } else {
        initAnimations();
    }

    console.log('✨ Why section ready');
})();