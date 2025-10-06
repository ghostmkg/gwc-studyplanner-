//this is the main js file controlling the behaviour of the pages now and might also later

document.addEventListener('DOMContentLoaded', function() {
    initStudySync();        //initializing all functionality
});

function initStudySync() {
    initAnimations(); //init-ing animations
    
    initEventListeners(); //initing eventlisteners
    
    initNavigation(); //init-ing navigations
    
    initSessionManagement(); //initning session management 
    
    initAuthFunctionality(); //init-ing auth functionality
    
    console.log('StudySync initialized successfully!');
}

//animation functions here
function initAnimations() {
    //feature cards on scroll animation
    const featureCards = document.querySelectorAll('.feature-card');
    const steps = document.querySelectorAll('.step');
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            }
        });
    }, observerOptions);
    
    //when observing feature card ani...
    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        observer.observe(card);
    });
    
    //when observing steps ani...
    steps.forEach(step => {
        step.style.opacity = '0';
        step.style.transform = 'translateY(30px)';
        observer.observe(step);
    });
    
    //when observing testimonial cards
    testimonialCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        observer.observe(card);
    });
    
    //hovering effects to cards
    const allCards = document.querySelectorAll('.card');
    allCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

//event listeners
function initEventListeners() {
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                updateActiveNavLink(this);
            }
        });
    });
    
    //call to action(CTA) button event listeners
    const getStartedBtn = document.getElementById('getStartedBtn');
    const demoBtn = document.getElementById('demoBtn');
    const createAccountBtn = document.getElementById('createAccountBtn');
    const learnMoreBtn = document.getElementById('learnMoreBtn');
    const newSessionBtn = document.getElementById('newSessionBtn');
    
    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showNotification('Redirecting to sign up page...', 'success');
            //when signup page and backend will be ready this will redirect to the same
            setTimeout(() => {
                window.location.href = '/signup';
            }, 1000);
        });
    }
    
    if (demoBtn) {
        demoBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showNotification('Opening demo video...', 'info');
            //when developed this will open a modal with demo video for tutorials and promo instructions
        });
    }
    
    if (createAccountBtn) {
        createAccountBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showNotification('Creating your account...', 'success');
            //to redirect on signup page when backend developed
        });
    }
    
    if (learnMoreBtn) {
        learnMoreBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const featuresSection = document.getElementById('features');
            if (featuresSection) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = featuresSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    }
    
    if (newSessionBtn) {
        newSessionBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showSessionModal();
        });
    }
}

//navigation functions
function initNavigation() {
    window.addEventListener('scroll', updateNavOnScroll);
    
    //mobile menu functionality(if needed in future)
    initMobileMenu();
}

function updateNavOnScroll() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    let currentSection = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        const headerHeight = document.querySelector('header').offsetHeight;
        
        if (scrollY >= (sectionTop - headerHeight - 50)) {
            currentSection = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

function updateActiveNavLink(clickedLink) {
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => link.classList.remove('active'));
    clickedLink.classList.add('active');
}

function initMobileMenu() {
    //this would be expanded for mobile menu functionality
}

//session Management
function initSessionManagement() {
    const joinButtons = document.querySelectorAll('.join-session');
    
    joinButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const sessionItem = this.closest('.session-item');
            const sessionTitle = sessionItem.querySelector('h4').textContent;
            
            showNotification(`Joining session: ${sessionTitle}`, 'success');
            
            this.textContent = 'Joining...';
            this.disabled = true;
            
            setTimeout(() => {
                this.textContent = 'Joined!';
                sessionItem.style.backgroundColor = '#f0f8ff';
                sessionItem.style.borderColor = '#4361ee';
                
                // In fully developed app, this would redirect to the session
                setTimeout(() => {
                    showNotification(`Successfully joined ${sessionTitle}`, 'success');
                }, 500);
            }, 1500);
        });
    });
}

function showSessionModal() {
    //creating modal HTML
    const modalHTML = `
        <div class="modal-overlay" id="sessionModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Create New Study Session</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <form id="sessionForm">
                        <div class="form-group">
                            <label for="sessionTitle">Session Title</label>
                            <input type="text" id="sessionTitle" placeholder="e.g., Calculus Review" required>
                        </div>
                        <div class="form-group">
                            <label for="sessionDate">Date & Time</label>
                            <input type="datetime-local" id="sessionDate" required>
                        </div>
                        <div class="form-group">
                            <label for="sessionDuration">Duration (hours)</label>
                            <input type="number" id="sessionDuration" min="0.5" max="8" step="0.5" value="1" required>
                        </div>
                        <div class="form-group">
                            <label for="sessionDescription">Description</label>
                            <textarea id="sessionDescription" placeholder="What will you be studying?" rows="3"></textarea>
                        </div>
                        <div class="form-actions">
                            <button type="button" class="btn btn-outline" id="cancelSession">Cancel</button>
                            <button type="submit" class="btn">Create Session</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    addModalStyles();
    
    //event listeners for modal
    const modal = document.getElementById('sessionModal');
    const closeBtn = modal.querySelector('.close-modal');
    const cancelBtn = modal.querySelector('#cancelSession');
    const sessionForm = modal.querySelector('#sessionForm');
    
    //animation - modal
    setTimeout(() => {
        modal.classList.add('active');
    }, 10);
    
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    sessionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        createNewSession(this);
    });
    
    function closeModal() {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

function addModalStyles() {
    const modalStyles = `
        <style>
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 2000;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .modal-overlay.active {
                opacity: 1;
            }
            
            .modal-content {
                background-color: white;
                border-radius: var(--border-radius);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                width: 90%;
                max-width: 500px;
                transform: translateY(-50px);
                transition: transform 0.3s ease;
            }
            
            .modal-overlay.active .modal-content {
                transform: translateY(0);
            }
            
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px;
                border-bottom: 1px solid var(--light-gray);
            }
            
            .modal-header h3 {
                margin: 0;
                color: var(--primary);
            }
            
            .close-modal {
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                color: var(--gray);
            }
            
            .modal-body {
                padding: 20px;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 600;
                color: var(--dark);
            }
            
            .form-group input,
            .form-group textarea,
            .form-group select {
                width: 100%;
                padding: 10px;
                border: 1px solid var(--light-gray);
                border-radius: var(--border-radius);
                font-family: inherit;
                transition: var(--transition);
            }
            
            .form-group input:focus,
            .form-group textarea:focus,
            .form-group select:focus {
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
            }
            
            .form-actions {
                display: flex;
                justify-content: flex-end;
                gap: 10px;
                margin-top: 30px;
            }
        </style>
    `;
    
    document.head.insertAdjacentHTML('beforeend', modalStyles);
}

function createNewSession(form) {
    const formData = new FormData(form);
    const sessionData = {
        title: document.getElementById('sessionTitle').value,
        date: document.getElementById('sessionDate').value,
        duration: document.getElementById('sessionDuration').value,
        description: document.getElementById('sessionDescription').value
    };
    
    //simulating API call
    showNotification('Creating your session...', 'info');
    
    setTimeout(() => {
        showNotification('Session created successfully!', 'success');
        closeModal();
        
        // In our developed app, this would update the session list
        console.log('New session created:', sessionData);
    }, 1500);
}

//auth functionality
function initAuthFunctionality() {
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showNotification('Redirecting to login...', 'info');
            //this would redirect to login page when developed
        });
    }
    
    if (signupBtn) {
        signupBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showNotification('Redirecting to sign up...', 'info');
            //this would redirect to signup page when developed
        });
    }
}

//notification system
function showNotification(message, type = 'info') {
    //first removing existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => {
        notification.remove();
    });
    
    //then creating notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    //a bit styling here separately
    if (!document.querySelector('#notification-styles')) {
        const notificationStyles = `
            <style>
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background-color: white;
                    border-radius: var(--border-radius);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                    z-index: 3000;
                    transform: translateX(400px);
                    transition: transform 0.3s ease;
                    max-width: 350px;
                }
                
                .notification.active {
                    transform: translateX(0);
                }
                
                .notification-content {
                    padding: 15px 20px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    border-left: 4px solid;
                }
                
                .notification-info .notification-content {
                    border-left-color: var(--primary);
                }
                
                .notification-success .notification-content {
                    border-left-color: var(--success);
                }
                
                .notification-warning .notification-content {
                    border-left-color: var(--warning);
                }
                
                .notification-error .notification-content {
                    border-left-color: var(--danger);
                }
                
                .notification-close {
                    background: none;
                    border: none;
                    font-size: 1.2rem;
                    cursor: pointer;
                    color: var(--gray);
                    margin-left: 10px;
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', notificationStyles);
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('active');
    }, 10);
    
    const autoRemove = setTimeout(() => {
        closeNotification(notification);
    }, 5000);
    
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        clearTimeout(autoRemove);
        closeNotification(notification);
    });
    
    function closeNotification(notificationElement) {
        notificationElement.classList.remove('active');
        setTimeout(() => {
            if (notificationElement.parentNode) {
                notificationElement.remove();
            }
        }, 300);
    }
}

//utility functions
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

//exporting functions for later needs
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initStudySync,
        showNotification,
        formatDate
    };
}
