/**
 * IFRI MentorLink - Dashboard
 * Compteurs animés, recherche, confirmation déconnexion
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ========== 1. COMPTEURS ANIMÉS ==========
    const counters = document.querySelectorAll('.stat-counter[data-target]');
    
    function animateCounter(el) {
        const target = parseInt(el.getAttribute('data-target'), 10);
        if (isNaN(target)) return;
        let current = 0;
        const steps = 40;
        const increment = target / steps;
        let step = 0;
        
        const timer = setInterval(() => {
            step++;
            current += increment;
            if (step >= steps) {
                el.innerHTML = target + (el.querySelector('.percent') ? '<span class="percent">%</span>' : '');
                clearInterval(timer);
            } else {
                el.innerHTML = Math.floor(current) + (el.querySelector('.percent') ? '<span class="percent">%</span>' : '');
            }
        }, 25);
    }
    
    // Observer pour déclencher l'animation à l'apparition
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        counters.forEach(counter => observer.observe(counter));
    } else {
        counters.forEach(animateCounter);
    }
    
    // ========== 2. RECHERCHE DANS LE TABLEAU ==========
    const searchInput = document.getElementById('tableSearch');
    const tableRows = document.querySelectorAll('#suiviTable tbody tr');
    
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
    
    // ========== 3. CONFIRMATION DE DÉCONNEXION ==========
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
                window.location.href = this.getAttribute('href');
            }
        });
    }
    
    // ========== 4. ACTIVE LINK ==========
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && href !== '#' && currentPath.includes(href)) {
            link.classList.add('active');
        }
    });
});