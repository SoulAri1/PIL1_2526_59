// Attendre que le document HTML soit complètement chargé
document.addEventListener('DOMContentLoaded', function() {
    console.log("🧠 MentorLink Engine activé avec succès !");

    // ==========================================
    // 1. POPUP DE CONFIRMATION DE DÉCONNEXION
    // ==========================================
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(event) {
            event.preventDefault(); // Stoppe la redirection immédiate
            
            const conf = confirm("Êtes-vous sûr de vouloir vous déconnecter de l'espace administration ?");
            if (conf) {
                window.location.href = this.getAttribute('href'); // Redirige vers '/'
            }
        });
    }

    // ==========================================
    // 2. GESTION DES ONGLETS ACTIFS (SIDEBAR)
    // ==========================================
    const navLinks = document.querySelectorAll('#sidebarMenu .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Optionnel : Enlever e.preventDefault() si vos liens pointent vers de vraies URLs Flask plus tard
            e.preventDefault(); 
            
            // On retire la classe active de tous les liens
            navLinks.forEach(item => item.classList.remove('active'));
            
            // On l'ajoute sur le lien cliqué
            this.classList.add('active');
            
            const pageCible = this.getAttribute('data-page');
            console.log(`Navigation demandée vers : ${pageCible}`);
        });
    });

    // ==========================================
    // 3. BARRE DE RECHERCHE TEMPS RÉEL (FILTRE TABLEAU)
    // ==========================================
    const searchInput = document.getElementById('tableSearch');
    const tableRows = document.querySelectorAll('#suiviTable tbody tr');

    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filterValue = this.value.toLowerCase();

            tableRows.forEach(row => {
                // On récupère le texte des colonnes Étudiant (index 0) et Filière (index 1)
                const etudiantText = row.cells[0].textContent.toLowerCase();
                const filiereText = row.cells[1].textContent.toLowerCase();

                // Si le mot-clé est trouvé dans l'une des colonnes, on laisse la ligne visible, sinon on la cache
                if (etudiantText.includes(filterValue) || filiereText.includes(filterValue)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            });
        });
    }
});