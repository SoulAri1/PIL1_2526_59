/**
 * IFRI MentorLink — Moteur d'interactions front-end
 */
document.addEventListener('DOMContentLoaded', function () {
    initPreloader();
    initNavbarScroll();
    initScrollReveal();
    initSmoothAnchors();
    initLogoutConfirm();
    initSidebarTabs();
    initTableSearch();
    initStatCounters();
});

/* --------------------------------------------------------------------------
   Preloader
   -------------------------------------------------------------------------- */
function initPreloader() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;

    window.addEventListener('load', function () {
        setTimeout(function () {
            preloader.classList.add('fade-out');
            setTimeout(function () {
                preloader.style.display = 'none';
            }, 800);
        }, 5000);
    });
}

/* --------------------------------------------------------------------------
   Navbar : ombre au scroll + lien actif selon section visible
   -------------------------------------------------------------------------- */
function initNavbarScroll() {
    const navbar = document.getElementById('mainNavbar');
    if (!navbar) return;

    const navLinks = navbar.querySelectorAll('.nav-link[data-nav]');
    const sections = [];

    navLinks.forEach(function (link) {
        const href = link.getAttribute('href') || '';
        const hash = href.includes('#') ? href.split('#')[1] : null;
        if (hash) {
            const section = document.getElementById(hash);
            if (section) sections.push({ id: hash, el: section, link: link });
        }
    });

    function onScroll() {
        if (window.scrollY > 20) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }

        let current = '';
        sections.forEach(function (item) {
            const top = item.el.offsetTop - 120;
            if (window.scrollY >= top) current = item.id;
        });

        navLinks.forEach(function (link) {
            link.classList.remove('active');
        });

        if (current === '' && window.location.pathname === '/') {
            const accueil = navbar.querySelector('[data-nav="accueil"]');
            if (accueil) accueil.classList.add('active');
        } else {
            sections.forEach(function (item) {
                if (item.id === current) item.link.classList.add('active');
            });
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}

/* --------------------------------------------------------------------------
   Animations au scroll (Intersection Observer)
   -------------------------------------------------------------------------- */
function initScrollReveal() {
    const elements = document.querySelectorAll('.reveal');
    if (!elements.length) return;

    if (!('IntersectionObserver' in window)) {
        elements.forEach(function (el) { el.classList.add('revealed'); });
        return;
    }

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    elements.forEach(function (el) { observer.observe(el); });
}

/* --------------------------------------------------------------------------
   Ancres fluides avec offset navbar
   -------------------------------------------------------------------------- */
function initSmoothAnchors() {
    document.querySelectorAll('a[href*="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (!href || href === '#') return;

            const hashIndex = href.indexOf('#');
            if (hashIndex === -1) return;

            const path = href.substring(0, hashIndex) || window.location.pathname;
            const hash = href.substring(hashIndex);

            if (path && path !== window.location.pathname) return;

            const target = document.querySelector(hash);
            if (!target) return;

            e.preventDefault();
            const offset = document.getElementById('mainNavbar') ? 80 : 0;
            const top = target.getBoundingClientRect().top + window.scrollY - offset;

            window.scrollTo({ top: top, behavior: 'smooth' });
            history.pushState(null, '', hash);
        });
    });
}

/* --------------------------------------------------------------------------
   Confirmation déconnexion (Dashboard)
   -------------------------------------------------------------------------- */
function initLogoutConfirm() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (!logoutBtn) return;

    logoutBtn.addEventListener('click', function (event) {
        event.preventDefault();
            const conf = confirm("Etes-vous sur de vouloir vous deconnecter ?");
        if (conf) {
            window.location.href = this.getAttribute('href');
        }
    });
}

/* --------------------------------------------------------------------------
   Onglets sidebar Dashboard
   -------------------------------------------------------------------------- */
function initSidebarTabs() {
    const navLinks = document.querySelectorAll('#sidebarMenu .nav-link');
    if (!navLinks.length) return;

    navLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            navLinks.forEach(function (item) { item.classList.remove('active'); });
            this.classList.add('active');
        });
    });
}

/* --------------------------------------------------------------------------
   Recherche tableau Dashboard
   -------------------------------------------------------------------------- */
function initTableSearch() {
    const searchInput = document.getElementById('tableSearch');
    const tableRows = document.querySelectorAll('#suiviTable tbody tr');
    if (!searchInput || !tableRows.length) return;

    searchInput.addEventListener('keyup', function () {
        const filterValue = this.value.toLowerCase();

        tableRows.forEach(function (row) {
            const etudiantText = row.cells[0].textContent.toLowerCase();
            const filiereText = row.cells[1].textContent.toLowerCase();

            if (etudiantText.includes(filterValue) || filiereText.includes(filterValue)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

/* --------------------------------------------------------------------------
   Compteurs animés (statistiques Dashboard)
   -------------------------------------------------------------------------- */
function initStatCounters() {
    const counters = document.querySelectorAll('.stat-counter[data-target]');
    if (!counters.length) return;

    function animateCounter(el) {
        const target = parseInt(el.getAttribute('data-target'), 10);
        if (isNaN(target)) return;

        const duration = 1200;
        const start = performance.now();

        function step(now) {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.floor(eased * target);
            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                el.textContent = target;
                el.classList.add('counted');
            }
        }

        requestAnimationFrame(step);
    }

    if (!('IntersectionObserver' in window)) {
        counters.forEach(animateCounter);
        return;
    }

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(function (el) { observer.observe(el); });
}
