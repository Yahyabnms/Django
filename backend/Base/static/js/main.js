// ============================================
// DARK/LIGHT TOGGLE - VERSION SIMPLIFIÉE
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle functionality
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
            
            // Toggle dark mode class
            const isDarkMode = document.body.classList.toggle('dark-mode');
            
            // Add transition effect
            document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
            
            if (isDarkMode) {
                // Switch to dark mode
                toggleThemeBtn.innerHTML = '<i class="fas fa-sun"></i>';
                toggleThemeBtn.classList.add('is-dark');
                toggleThemeBtn.setAttribute('aria-label', 'Passer en mode clair');
                localStorage.setItem(darkModeKey, 'enabled');
                console.log('Mode sombre activé');
            } else {
                // Switch to light mode
                toggleThemeBtn.innerHTML = '<i class="fas fa-moon"></i>';
                toggleThemeBtn.classList.remove('is-dark');
                toggleThemeBtn.setAttribute('aria-label', 'Passer en mode sombre');
                localStorage.setItem(darkModeKey, 'disabled');
                console.log('Mode clair activé');
            }
            
            // Remove transition after animation
            setTimeout(() => {
                document.body.style.transition = '';
            }, 300);
        });
    } else {
        console.log('Bouton toggle non trouvé!');
    }

    // Smooth scrolling for anchor links - keep welcome always visible
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const welcomeSection = document.querySelector('#accueil');
                const welcomeHeight = welcomeSection.offsetHeight;
                
                // For links to sections other than #accueil, scroll to show section but keep welcome visible
                if (this.getAttribute('href') === '#accueil') {
                    // Scroll to top for accueil
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                } else {
                    // For other sections, position to show section but keep welcome visible
                    const targetPosition = target.offsetTop - welcomeHeight - navbarHeight - 50;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Navbar collapse on link click (mobile)
    const navbarLinks = document.querySelectorAll('.navbar-nav a:not(.dropdown-toggle)');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navbarLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                const collapseInstance = bootstrap.Collapse.getInstance(navbarCollapse) || new bootstrap.Collapse(navbarCollapse, { toggle: false });
                collapseInstance.hide();
            }
        });
    });

    // Active navigation link on scroll (anchors only)
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar-nav a[href^="#"]');

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

    // Add hover effects to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    console.log('AutoLocation - Page chargée avec succès!');
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
