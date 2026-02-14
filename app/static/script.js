// 1. 2D Network Animation for Hero (Enhanced)
const canvas = document.getElementById('hero-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];
    // Mouse interaction state
    let mouse = { x: null, y: null, radius: 150 };

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = document.querySelector('.hero').offsetHeight;
    }

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 1.5;
            this.vy = (Math.random() - 0.5) * 1.5;
            this.size = Math.random() * 2 + 1;
            this.baseColor = Math.random() > 0.5 ? '212, 175, 55' : '255, 255, 255'; // RGB for Gold or White
            this.opacity = Math.random() * 0.5 + 0.1;
        }
        update() {
            this.x += this.vx;
            this.y += this.vy;

            // Bounce off edges
            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;

            // Mouse interaction
            if (mouse.x != null) {
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < mouse.radius) {
                    const forceDirectionX = dx / distance;
                    const forceDirectionY = dy / distance;
                    const force = (mouse.radius - distance) / mouse.radius;
                    const directionX = forceDirectionX * force * 3; // Push force
                    const directionY = forceDirectionY * force * 3;
                    this.x -= directionX;
                    this.y -= directionY;
                }
            }
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${this.baseColor}, ${this.opacity})`;
            ctx.fill();
        }
    }

    function initParticles() {
        particles = [];
        // Responsive particle count
        const particleCount = Math.floor(window.innerWidth / 12);
        for (let i = 0; i < particleCount; i++) particles.push(new Particle());
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
            for (let j = i; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 120) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(255,255, 255, ${0.15 - distance / 800})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }

    // Mouse Event Listeners
    window.addEventListener('mousemove', (event) => {
        const rect = canvas.getBoundingClientRect();
        mouse.x = event.clientX - rect.left;
        mouse.y = event.clientY - rect.top;
    });

    window.addEventListener('mouseout', () => {
        mouse.x = null;
        mouse.y = null;
    });

    window.addEventListener('resize', () => { resize(); initParticles(); });
    resize();
    initParticles();
    animate();
}

// 2. FLAGSHIP FILTERS LOGIC (for index.html)
const filterBtns = document.querySelectorAll('.filter-btn');
const flagshipCards = document.querySelectorAll('#flagship .flagship-card');

if (filterBtns.length > 0) {
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filterValue = btn.getAttribute('data-filter');
            flagshipCards.forEach(card => {
                if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {
                    card.classList.remove('hide');
                    card.classList.add('show');
                } else {
                    card.classList.remove('show');
                    card.classList.add('hide');
                }
            });
        });
    });
}

// 3. MOBILE MENU TOGGLE
const mobileBtn = document.getElementById('mobile-menu-btn');
const navbarMenu = document.getElementById('navbar-menu');

if (mobileBtn) {
    mobileBtn.addEventListener('click', () => {
        navbarMenu.classList.toggle('active');
    });
}

// 4. Detailed Programs Tabs (for programs.html)
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

if (tabBtns.length > 0) {
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            const tabContent = document.getElementById(tabId);
            if (tabContent) {
                tabContent.classList.add('active');
            }
        });
    });
}

// 5. Active Navigation Link Highlight
window.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.navbar-link');

    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href');
        if (linkPage === currentPage ||
            (currentPage === '' && linkPage === 'index.html') ||
            (currentPage === 'index.html' && linkPage === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// 6. Contact Form Submission - Let the server handle this now
// Handled by backend routes.py
document.addEventListener('DOMContentLoaded', () => {
    const timestampField = document.getElementById('form-timestamp');
    if (timestampField) {
        timestampField.value = Date.now();
    }
});

// 7. Smooth scrolling for anchor links within same page
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 100,
                behavior: 'smooth'
            });
        }
    });
});

// 8. Sponsors Ticker Loop
document.addEventListener('DOMContentLoaded', () => {
    const sponsorsTrack = document.querySelector('.sponsors-track');
    if (sponsorsTrack && sponsorsTrack.children.length > 0) {
        // Clone logos for seamless loop
        const logos = Array.from(sponsorsTrack.children);
        logos.forEach(logo => {
            const clone = logo.cloneNode(true);
            sponsorsTrack.appendChild(clone);
        });

        // Create keyframes dynamically
        const style = document.createElement('style');
        document.head.appendChild(style);

        const updateAnimation = () => {
            const trackWidth = sponsorsTrack.scrollWidth;
            const animationDistance = trackWidth / 2;
            const speed = 50; // pixels per second
            const duration = animationDistance / speed;

            style.innerHTML = `
                @keyframes scrollTicker {
                    0% { transform: translateX(0); }
                    100% { transform: translateX(-${animationDistance}px); }
                }
            `;
            sponsorsTrack.style.animation = `scrollTicker ${duration}s linear infinite`;
        };

        // Initial setup after images load
        window.addEventListener('load', updateAnimation);
    }
});