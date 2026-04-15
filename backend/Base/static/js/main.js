// ============================================
// INTERACTIONS JAVASCRIPT
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Navbar collapse on link click
    const navbarLinks = document.querySelectorAll('.navbar-nav a:not(.btn-admin)');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navbarLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            }
        });
    });

    // Add animation classes on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe cards for animation
    document.querySelectorAll('.stat-card, .service-card, .category-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });

    // Active navigation link on scroll
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar-nav a[href^="#"]');

    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 200) {
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

    // Add hover effects to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Dark Mode Toggle
    const toggleThemeBtn = document.getElementById('toggleTheme');
    const darkModeKey = 'darkMode';
    
    // Check if dark mode is already enabled from localStorage
    if (localStorage.getItem(darkModeKey) === 'enabled') {
        document.body.classList.add('dark-mode');
        if (toggleThemeBtn) {
            toggleThemeBtn.innerHTML = '<i class="fas fa-sun"></i>';
        }
    }
    
    if (toggleThemeBtn) {
        toggleThemeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('Toggle clicked');
            document.body.classList.toggle('dark-mode');
            console.log('Dark mode enabled:', document.body.classList.contains('dark-mode'));
            
            if (document.body.classList.contains('dark-mode')) {
                toggleThemeBtn.innerHTML = '<i class="fas fa-sun"></i>';
                localStorage.setItem(darkModeKey, 'enabled');
                console.log('Switched to dark mode');
            } else {
                toggleThemeBtn.innerHTML = '<i class="fas fa-moon"></i>';
                localStorage.setItem(darkModeKey, 'disabled');
                console.log('Switched to light mode');
            }
        });
    } else {
        console.log('Toggle button not found!');
    }

    console.log('AutoLocation - Page loaded successfully!');
});

// ============================================
// UTILITY FUNCTIONS
// ============================================

function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

function toggleNavbar() {
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('navbar-expanded');
}
