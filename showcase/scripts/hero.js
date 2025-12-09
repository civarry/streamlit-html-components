// Hero Section JavaScript
(function() {
    console.log('🚀 Streamlit HTML Components - Landing Page Loaded!');

    // Smooth scroll to section
    window.scrollToSection = function(sectionId) {
        console.log('Scrolling to:', sectionId);

        // Send event to Streamlit
        if (typeof window.sendToStreamlit === 'function') {
            window.sendToStreamlit('navigate', {
                section: sectionId,
                timestamp: new Date().toISOString()
            });
        }

        // Visual feedback
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                btn.style.transform = '';
            }, 200);
        });
    };

    // Animate elements on load
    function animateOnLoad() {
        const heroContent = document.querySelector('.hero-content');
        if (heroContent) {
            heroContent.style.opacity = '0';
            heroContent.style.transform = 'translateY(30px)';

            setTimeout(() => {
                heroContent.style.transition = 'all 0.8s ease';
                heroContent.style.opacity = '1';
                heroContent.style.transform = 'translateY(0)';
            }, 100);
        }
    }

    // Parallax effect on mouse move
    document.addEventListener('mousemove', function(e) {
        const orbs = document.querySelectorAll('.gradient-orb');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;

        orbs.forEach((orb, index) => {
            const speed = (index + 1) * 20;
            const x = (mouseX - 0.5) * speed;
            const y = (mouseY - 0.5) * speed;

            orb.style.transform = `translate(${x}px, ${y}px)`;
        });
    });

    // Typing effect for title (optional)
    function typeWriter(element, text, speed = 100) {
        let i = 0;
        element.textContent = '';

        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }

        type();
    }

    // Add sparkle effect on hover
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.filter = 'brightness(1.1)';
        });

        btn.addEventListener('mouseleave', function() {
            this.style.filter = '';
        });

        btn.addEventListener('click', function() {
            // Ripple effect
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.animation = 'ripple 0.6s ease-out';

            this.style.position = 'relative';
            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Initialize
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', animateOnLoad);
    } else {
        animateOnLoad();
    }

    console.log('✨ Landing page animations ready!');
})();

// Ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        from {
            transform: scale(0);
            opacity: 1;
        }
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
