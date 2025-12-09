// Examples Section JavaScript
(function() {
    console.log('🚀 Examples Section Loaded');

    // Initialize when component is loaded
    window.initExamples = function() {
        // Tab switching
        window.switchTab = function(tabId) {
            // Update UI
            document.querySelectorAll('.tab-header').forEach(h => h.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
            document.getElementById(`content-${tabId}`).classList.add('active');
            
            // Notify Streamlit
            if (window.parent && window.parent.sendToStreamlit) {
                window.parent.sendToStreamlit('tab_changed', { tab: tabId });
            }
        };

        // Handle demo clicks
        document.querySelectorAll('.demo-placeholder').forEach(placeholder => {
            placeholder.addEventListener('click', function() {
                const demo = this.dataset.demo;
                alert(`Would load ${demo} demo. Expand the section above to see it!`);
            });
        });
    };

    // Auto-initialize
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', window.initExamples);
    } else {
        window.initExamples();
    }
})();