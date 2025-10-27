//StudySync Frontend JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initStudySync();        //initializing all functionality
});

//global variables
let currentUser = null;
let authToken = null;

function initStudySync() {
    initAnimations(); //init-ing animations
    initEventListeners(); //initing eventlisteners
    initNavigation(); //init-ing navigations
    initSessionManagement(); //initning session management 
    initAuthFunctionality(); //init-ing auth functionality
    
    //check if user is already logged in
    checkExistingAuth();
    
    console.log('StudySync initialized successfully!');
}

//authentication functions
async function checkExistingAuth() {
    const token = localStorage.getItem('studysync_token');
    if (token) {
        authToken = token;
        try {
            const user = await fetchCurrentUser();
            if (user) {
                currentUser = user;
                updateUIForLoggedInUser();
            }
        } catch (error) {
            console.log('Invalid token, logging out...');
            logout();
        }
    }
}

async function fetchCurrentUser() {
    try {
        const response = await fetch('/api/auth/me', {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Not authenticated');
        }
    } catch (error) {
        console.error('Error fetching user:', error);
        return null;
    }
}

function updateUIForLoggedInUser() {
    const authButtons = document.querySelector('.auth-buttons');
    if (authButtons && currentUser) {
        authButtons.innerHTML = `
            <span style="color: white; margin-right: 15px;">Hello, ${currentUser.full_name}</span>
            <a href="#" class="btn btn-outline" id="dashboardBtn">Dashboard</a>
            <a href="#" class="btn" id="logoutBtn">Log Out</a>
        `;
        
        document.getElementById('logoutBtn').addEventListener('click', logout);
        document.getElementById('dashboardBtn').addEventListener('click', showDashboard);
    }
}

function logout() {
    localStorage.removeItem('studysync_token');
    authToken = null;
    currentUser = null;
    location.reload();
}

function showDashboard() {
    showNotification('Dashboard feature coming soon!', 'info');
}

//API functions
async function apiRequest(endpoint, options = {}) {
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    if (authToken) {
        config.headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    try {
        const response = await fetch(endpoint, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'API request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API request failed:', error);
        showNotification(error.message, 'error');
        throw error;
    }
}

//authentication modals
function showLoginModal() {
    const modalHTML = `
        <div class="modal-overlay" id="loginModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Log In to StudySync</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <form id="loginForm">
                        <div class="form-group">
                            <label for="loginEmail">Email</label>
                            <input type="email" id="loginEmail" placeholder="your@email.com" required>
                        </div>
                        <div class="form-group">
                            <label for="loginPassword">Password</label>
                            <input type="password" id="loginPassword" placeholder="Enter your password" required>
                        </div>
                        <div class="form-actions">
                            <button type="button" class="btn btn-outline" id="cancelLogin">Cancel</button>
                            <button type="submit" class="btn">Log In</button>
                        </div>
                    </form>
                    <p style="text-align: center; margin-top: 15px;">
                        Don't have an account? <a href="#" id="showSignup">Sign up here</a>
                    </p>
                </div>
            </div>
        </div>
    `;
    
    showModal(modalHTML, 'loginModal');
    
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('showSignup').addEventListener('click', function(e) {
        e.preventDefault();
        closeModal();
        showSignupModal();
    });
}

function showSignupModal() {
    const modalHTML = `
        <div class="modal-overlay" id="signupModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Create Your StudySync Account</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <form id="signupForm">
                        <div class="form-group">
                            <label for="signupFullName">Full Name</label>
                            <input type="text" id="signupFullName" placeholder="Enter your full name" required>
                        </div>
                        <div class="form-group">
                            <label for="signupUsername">Username</label>
                            <input type="text" id="signupUsername" placeholder="Choose a username" required>
                        </div>
                        <div class="form-group">
                            <label for="signupEmail">Email</label>
                            <input type="email" id="signupEmail" placeholder="your@email.com" required>
                        </div>
                        <div class="form-group">
                            <label for="signupPassword">Password</label>
                            <input type="password" id="signupPassword" placeholder="Create a password" required>
                        </div>
                        <div class="form-actions">
                            <button type="button" class="btn btn-outline" id="cancelSignup">Cancel</button>
                            <button type="submit" class="btn">Create Account</button>
                        </div>
                    </form>
                    <p style="text-align: center; margin-top: 15px;">
                        Already have an account? <a href="#" id="showLogin">Log in here</a>
                    </p>
                </div>
            </div>
        </div>
    `;
    
    showModal(modalHTML, 'signupModal');
    
    document.getElementById('signupForm').addEventListener('submit', handleSignup);
    document.getElementById('showLogin').addEventListener('click', function(e) {
        e.preventDefault();
        closeModal();
        showLoginModal();
    });
}

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const data = await apiRequest('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        authToken = data.access_token;
        localStorage.setItem('studysync_token', authToken);
        
        currentUser = await fetchCurrentUser();
        showNotification('Login successful!', 'success');
        closeModal();
        updateUIForLoggedInUser();
        
    } catch (error) {
        showNotification('Login failed. Please check your credentials.', 'error');
    }
}

async function handleSignup(e) {
    e.preventDefault();
    
    const formData = {
        full_name: document.getElementById('signupFullName').value,
        username: document.getElementById('signupUsername').value,
        email: document.getElementById('signupEmail').value,
        password: document.getElementById('signupPassword').value
    };
    
    try {
        await apiRequest('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        showNotification('Account created successfully! Please log in.', 'success');
        closeModal();
        showLoginModal();
        
    } catch (error) {
        showNotification('Signup failed. Please try again.', 'error');
    }
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
            showSignupModal(); // Show modal instead of redirect
        });
    }
    
    if (demoBtn) {
        demoBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showNotification('Opening demo video...', 'info');
        });
    }
    
    if (createAccountBtn) {
        createAccountBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showSignupModal(); // Show modal instead of redirect
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
            if (!currentUser) {
                showNotification('Please log in to create sessions', 'warning');
                showLoginModal(); // Show login modal if not authenticated
                return;
            }
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
    //this will be expanded for mobile menu functionality
}

//session Management
async function initSessionManagement() {
    await loadSessionsFromAPI();
    
    const joinButtons = document.querySelectorAll('.join-session');
    
    joinButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            if (!currentUser) {
                showNotification('Please log in to join sessions', 'warning');
                showLoginModal();
                return;
            }
            
            const sessionItem = this.closest('.session-item');
            const sessionTitle = sessionItem.querySelector('h4').textContent;
            
            showNotification(`Joining session: ${sessionTitle}`, 'success');
            
            this.textContent = 'Joining...';
            this.disabled = true;
            
            setTimeout(() => {
                this.textContent = 'Joined!';
                sessionItem.style.backgroundColor = '#f0f8ff';
                sessionItem.style.borderColor = '#4361ee';
                
                //In fully developed app, this will redirect to the session
                setTimeout(() => {
                    showNotification(`Successfully joined ${sessionTitle}`, 'success');
                }, 500);
            }, 1500);
        });
    });
}

async function loadSessionsFromAPI() {
    try {
        const data = await apiRequest('/api/sessions');
        updateSessionList(data.sessions);
    } catch (error) {
        console.log('Could not load sessions from API, using demo data');
    }
}

function updateSessionList(sessions) {
    const sessionList = document.querySelector('.session-list');
    if (!sessionList || !sessions || sessions.length === 0) return;
    
    sessionList.innerHTML = sessions.map(session => `
        <div class="session-item">
            <div class="session-info">
                <h4>${session.title}</h4>
                <div class="session-meta">
                    <span><i class="far fa-calendar"></i> ${formatSessionDate(session.scheduled_time)}</span>
                    <span><i class="far fa-clock"></i> ${session.duration_minutes} minutes</span>
                    <span><i class="fas fa-users"></i> ${session.group_name}</span>
                </div>
                <p>${session.description}</p>
            </div>
            <div class="session-actions">
                <a href="#" class="btn join-session">Join</a>
            </div>
        </div>
    `).join('');
}

function formatSessionDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
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
                            <label for="sessionMaxParticipants">Max Participants</label>
                            <input type="number" id="sessionMaxParticipants" min="2" max="20" value="10" required>
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
    
    //setting minimum date to today
    const today = new Date().toISOString().slice(0, 16);
    document.getElementById('sessionDate').min = today;
    
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
    if (!document.querySelector('#modal-styles')) {
        const modalStyles = `
            <style id="modal-styles">
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
}

async function createNewSession(form) {
    const sessionData = {
        title: document.getElementById('sessionTitle').value,
        description: document.getElementById('sessionDescription').value,
        scheduled_time: document.getElementById('sessionDate').value,
        duration_minutes: parseInt(document.getElementById('sessionDuration').value) * 60,
        max_participants: parseInt(document.getElementById('sessionMaxParticipants').value),
        group_id: 1 //default group for now
    };
    
    try {
        showNotification('Creating your session...', 'info');
        
        await apiRequest('/api/sessions', {
            method: 'POST',
            body: JSON.stringify(sessionData)
        });
        
        showNotification('Session created successfully!', 'success');
        closeModal();
        await loadSessionsFromAPI(); //refresh the session list
        
    } catch (error) {
        showNotification('Failed to create session', 'error');
    }
}

//auth functionality
function initAuthFunctionality() {
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showLoginModal(); //show modal instead of redirect
        });
    }
    
    if (signupBtn) {
        signupBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showSignupModal(); //show modal instead of redirect
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

//modal utility functions
function showModal(modalHTML, modalId) {
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const modal = document.getElementById(modalId);
    const closeBtn = modal.querySelector('.close-modal');
    const cancelBtn = modal.querySelector(`#cancel${modalId.replace('Modal', '')}`);
    
    setTimeout(() => {
        modal.classList.add('active');
    }, 10);
    
    closeBtn.addEventListener('click', () => closeModal());
    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => closeModal());
    }
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    function closeModal() {
        modal.classList.remove('active');
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
            }
        }, 300);
    }
}

function closeModal() {
    const modal = document.querySelector('.modal-overlay.active');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
            }
        }, 300);
    }
}

function smoothScrollToElement(element) {
    const headerHeight = document.querySelector('header').offsetHeight;
    const targetPosition = element.offsetTop - headerHeight;
    
    window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
    });
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