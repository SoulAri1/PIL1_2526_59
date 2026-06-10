document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');
    if (sidebar && toggleBtn) {
        let sidebarVisible = true;
        toggleBtn.addEventListener('click', function() {
            if (sidebarVisible) {
                sidebar.style.transform = 'translateX(-100%)';
                sidebar.style.position = 'fixed';
                sidebar.style.zIndex = '1050';
                toggleBtn.innerHTML = '<i class="bi bi-arrow-right-circle-fill"></i>';
                toggleBtn.classList.add('btn-primary');
                toggleBtn.classList.remove('btn-secondary');
            } else {
                sidebar.style.transform = 'translateX(0)';
                sidebar.style.position = '';
                toggleBtn.innerHTML = '<i class="bi bi-arrow-left-circle-fill"></i>';
                toggleBtn.classList.add('btn-secondary');
                toggleBtn.classList.remove('btn-primary');
            }
            sidebarVisible = !sidebarVisible;
        });
    }
    const cards = document.querySelectorAll('.card-stat');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.transition = 'all 0.3s ease';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});