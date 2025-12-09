// Installation Section JavaScript
(function() {
    console.log('🚀 Installation Section Loaded');

    // Animate steps on scroll
    function initStepAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const step = entry.target;
                    const stepNumber = step.dataset.step;
                    
                    // Animate step number
                    const numberElement = step.querySelector('.step-number');
                    numberElement.style.transform = 'scale(0)';
                    numberElement.style.opacity = '0';
                    
                    setTimeout(() => {
                        numberElement.style.transition = 'all 0.5s ease';
                        numberElement.style.transform = 'scale(1)';
                        numberElement.style.opacity = '1';
                    }, 100);
                    
                    // Animate step content
                    step.style.opacity = '0';
                    step.style.transform = 'translateX(-20px)';
                    
                    setTimeout(() => {
                        step.style.transition = 'all 0.6s ease';
                        step.style.opacity = '1';
                        step.style.transform = 'translateX(0)';
                    }, 200 * stepNumber);
                    
                    observer.unobserve(step);
                }
            });
        }, {
            threshold: 0.2,
            rootMargin: '50px'
        });

        document.querySelectorAll('.installation-step').forEach(step => {
            observer.observe(step);
        });
    }

    // Copy code functionality
    function initCodeCopy() {
        document.querySelectorAll('.step-code').forEach(codeBlock => {
            const copyButton = document.createElement('button');
            copyButton.className = 'copy-button';
            copyButton.innerHTML = '📋';
            copyButton.title = 'Copy code';
            
            copyButton.addEventListener('click', function() {
                const code = this.parentElement.querySelector('code').textContent;
                navigator.clipboard.writeText(code).then(() => {
                    this.innerHTML = '✅';
                    this.style.background = '#10b981';
                    
                    setTimeout(() => {
                        this.innerHTML = '📋';
                        this.style.background = '';
                    }, 2000);
                    
                    // Show notification
                    showCopyNotification('Code copied to clipboard!');
                }).catch(err => {
                    console.error('Failed to copy:', err);
                    showCopyNotification('Failed to copy code');
                });
            });
            
            codeBlock.style.position = 'relative';
            copyButton.style.cssText = `
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 5px 10px;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 0.9rem;
            `;
            
            codeBlock.appendChild(copyButton);
        });
    }

    function showCopyNotification(message) {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }

    // Add animations for notification
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        .copy-button:hover {
            background: rgba(255, 255, 255, 0.3) !important;
            transform: scale(1.1);
        }
    `;
    document.head.appendChild(style);

    // Success section animation
    function initSuccessAnimation() {
        const successSection = document.querySelector('.installation-success');
        if (successSection) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '0';
                        entry.target.style.transform = 'scale(0.9)';
                        
                        setTimeout(() => {
                            entry.target.style.transition = 'all 0.8s ease';
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'scale(1)';
                        }, 300);
                        
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.5
            });
            
            observer.observe(successSection);
        }
    }

    // Initialize everything
    function init() {
        initStepAnimations();
        initCodeCopy();
        initSuccessAnimation();
        
        // Add click effects to success section
        const successSection = document.querySelector('.installation-success');
        if (successSection) {
            successSection.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 200);
                
                // Send celebration event
                if (typeof window.sendToStreamlit === 'function') {
                    window.sendToStreamlit('celebration', {
                        type: 'installation_complete',
                        timestamp: new Date().toISOString()
                    });
                }
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    console.log('✨ Installation section ready');
})();