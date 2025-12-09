// Footer Section JavaScript
(function() {
    console.log('🚀 Footer Section Loaded');

    // Smooth hover effects for CTA buttons
    function initCTAHoverEffects() {
        const buttons = document.querySelectorAll('.cta-button');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.05)';
                this.style.boxShadow = '0 15px 40px rgba(0, 0, 0, 0.3)';
                
                // Add particle effect for primary button
                if (this.classList.contains('cta-button-primary')) {
                    createParticles(this);
                }
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '';
            });
            
            button.addEventListener('click', function(e) {
                // Ripple effect
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.5);
                    width: ${size}px;
                    height: ${size}px;
                    top: ${y}px;
                    left: ${x}px;
                    transform: scale(0);
                    animation: ripple 0.6s ease-out;
                    pointer-events: none;
                `;
                
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
                
                // Send click event to Streamlit
                if (typeof window.sendToStreamlit === 'function') {
                    const buttonType = this.classList.contains('cta-button-primary') ? 'github' : 'pypi';
                    window.sendToStreamlit('cta_click', {
                        button: buttonType,
                        text: this.textContent.trim(),
                        timestamp: new Date().toISOString()
                    });
                }
            });
        });
    }

    // Create particle effect for button hover
    function createParticles(button) {
        const particleCount = 8;
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('span');
            particle.style.cssText = `
                position: absolute;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 50%;
                width: 4px;
                height: 4px;
                pointer-events: none;
                animation: particle-float 1s ease-out forwards;
            `;
            
            // Random position around button
            const angle = (Math.PI * 2 * i) / particleCount;
            const distance = 40;
            particle.style.left = '50%';
            particle.style.top = '50%';
            particle.style.setProperty('--start-x', Math.cos(angle) * distance + 'px');
            particle.style.setProperty('--start-y', Math.sin(angle) * distance + 'px');
            
            button.appendChild(particle);
            
            setTimeout(() => particle.remove(), 1000);
        }
    }

    // Animate footer links on scroll
    function initFooterAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Animate links with staggered delay
                    document.querySelectorAll('.footer-link').forEach((link, index) => {
                        link.style.animationDelay = `${index * 100}ms`;
                        link.style.animation = 'slideUp 0.5s ease forwards';
                    });
                    
                    // Animate social icons
                    document.querySelectorAll('.social-icon').forEach((icon, index) => {
                        icon.style.opacity = '0';
                        icon.style.transform = 'translateY(20px)';
                        
                        setTimeout(() => {
                            icon.style.transition = `all 0.5s ease ${index * 100 + 300}ms`;
                            icon.style.opacity = '1';
                            icon.style.transform = 'translateY(0)';
                        }, 50);
                    });
                    
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        observer.observe(document.querySelector('.footer-section'));
    }

    // Current year in copyright
    function updateCopyrightYear() {
        const copyrightElement = document.querySelector('.footer-copyright');
        if (copyrightElement) {
            const currentYear = new Date().getFullYear();
            copyrightElement.innerHTML = copyrightElement.innerHTML.replace('2024', currentYear);
        }
    }

    // Social icon hover effects
    function initSocialIcons() {
        document.querySelectorAll('.social-icon').forEach(icon => {
            icon.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) rotate(5deg) scale(1.1)';
                this.style.boxShadow = '0 10px 20px rgba(102, 126, 234, 0.3)';
                
                // Change icon color based on platform
                const href = this.href;
                if (href.includes('github')) {
                    this.style.background = '#333';
                } else if (href.includes('twitter')) {
                    this.style.background = '#1DA1F2';
                } else if (href.includes('discord')) {
                    this.style.background = '#7289DA';
                }
            });
            
            icon.addEventListener('mouseleave', function() {
                this.style.transform = '';
                this.style.boxShadow = '';
                this.style.background = '';
            });
        });
    }

    // Add ripple animation style
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        @keyframes particle-float {
            0% {
                transform: translate(0, 0) scale(1);
                opacity: 1;
            }
            100% {
                transform: translate(var(--start-x), var(--start-y)) scale(0);
                opacity: 0;
            }
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);

    // Initialize everything
    function init() {
        initCTAHoverEffects();
        initFooterAnimations();
        initSocialIcons();
        updateCopyrightYear();
        
        // Add scroll-to-top functionality for footer
        const footer = document.querySelector('.footer-section');
        footer.addEventListener('click', function(e) {
            if (e.target === this || e.target.classList.contains('footer-content')) {
                // Send event to Streamlit
                if (typeof window.sendToStreamlit === 'function') {
                    window.sendToStreamlit('footer_interaction', {
                        type: 'background_click',
                        timestamp: new Date().toISOString()
                    });
                }
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    console.log('✨ Footer section ready');
})();