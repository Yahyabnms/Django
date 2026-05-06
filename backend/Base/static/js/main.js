// ============================================
// AUTOLOCATION - MAIN JAVASCRIPT
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-scroll to contact if #contact is in URL
    if (window.location.hash === '#contact') {
        setTimeout(() => {
            const contactSection = document.getElementById('contact');
            if (contactSection) {
                contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }, 100);
    }
    
    initDarkMode();
    initNavbar();
    initScrollEffects();
    initContactSection();
});

// ============================================
// DARK MODE TOGGLE
// ============================================

function initDarkMode() {
    const toggleThemeBtn = document.getElementById('toggleTheme');
    const darkModeKey = 'darkMode';
    
    // Check if dark mode is already enabled from localStorage
    if (localStorage.getItem(darkModeKey) === 'enabled') {
        document.body.classList.add('dark-mode');
        if (toggleThemeBtn) {
            toggleThemeBtn.innerHTML = '<i class="fas fa-sun"></i>';
            toggleThemeBtn.classList.add('is-dark');
            toggleThemeBtn.setAttribute('aria-label', 'Passer en mode clair');
        }
    }
    
    if (toggleThemeBtn) {
        toggleThemeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const isDarkMode = document.body.classList.toggle('dark-mode');
            document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
            
            if (isDarkMode) {
                toggleThemeBtn.innerHTML = '<i class="fas fa-sun"></i>';
                toggleThemeBtn.classList.add('is-dark');
                toggleThemeBtn.setAttribute('aria-label', 'Passer en mode clair');
                localStorage.setItem(darkModeKey, 'enabled');
            } else {
                toggleThemeBtn.innerHTML = '<i class="fas fa-moon"></i>';
                toggleThemeBtn.classList.remove('is-dark');
                toggleThemeBtn.setAttribute('aria-label', 'Passer en mode sombre');
                localStorage.setItem(darkModeKey, 'disabled');
            }
            
            setTimeout(() => {
                document.body.style.transition = '';
            }, 300);
        });
    }
}

// ============================================
// NAVBAR FUNCTIONALITY
// ============================================

function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarLinks = document.querySelectorAll('.navbar-nav a:not(.dropdown-toggle)');
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Close navbar on link click (mobile)
    navbarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href').startsWith('#') && !this.classList.contains('dropdown-toggle')) {
                if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                    bootstrap.Collapse.getOrCreateInstance(navbarCollapse).hide();
                }
            }
        });
    });

    // Add hover effects to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// ============================================
// SCROLL EFFECTS
// ============================================

function initScrollEffects() {
    // Smooth scroll animation for all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '#contact') {  // Skip contact, handled separately
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Active navigation link on scroll (anchors only) - excluding contact link
    const sections = document.querySelectorAll('section[id]:not(#contact)');
    const navLinks = document.querySelectorAll('.navbar-nav a[href^="#"]:not(.nav-contact)');

    if (sections.length && navLinks.length) {
        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                if (window.pageYOffset >= sectionTop - 200) {
                    current = section.getAttribute('id');
                }
            });
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href').slice(1) === current) {
                    link.classList.add('active');
                }
            });
        });
    }
}

// ============================================
// CONTACT SECTION
// ============================================

function initContactSection() {
    // Add animation to contact cards on scroll
    const contactCards = document.querySelectorAll('.contact-card');
    if (contactCards.length > 0) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        contactCards.forEach(card => {
            observer.observe(card);
        });

        // Add CSS animation if not already present
        if (!document.querySelector('style:contains(fadeInUp)')) {
            const style = document.createElement('style');
            style.textContent = `
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(30px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function toggleNavbar() {
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('navbar-expanded');
}

// Handle contact click - now works on all pages
function handleContactClick(event) {
    event.preventDefault();
    event.stopPropagation();
    
    // Close mobile menu if open
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
        bootstrap.Collapse.getOrCreateInstance(navbarCollapse).hide();
    }
    
    // Scroll to contact section (now available on all pages)
    const contactSection = document.getElementById('contact');
    if (contactSection) {
        setTimeout(() => {
            contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            window.history.pushState(null, null, '#contact');
        }, 300);
    }
}

console.log('AutoLocation - Page chargée avec succès!');

console.log('AutoLocation - Page chargée avec succès!');
