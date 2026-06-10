/**
 * IFRI MentorLink - Profil dynamique (Version stable)
 * Boutons Masquer/Voir + Ajout de matière personnalisée
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log("=== PROFIL JS ACTIVE ===");

    // ===== 1. SECTION COMPÉTENCES =====
    let compGroup = document.querySelector('.competences-section .custom-checkbox-group');
    if (!compGroup) {
        // Recherche alternative
        const allGroups = document.querySelectorAll('.custom-checkbox-group');
        for (let group of allGroups) {
            const prevText = group.previousElementSibling?.innerText || '';
            if (prevText.includes('Compétence') || prevText.includes('compétence')) {
                compGroup = group;
                break;
            }
        }
    }
    
    if (compGroup) {
        console.log("✅ Groupe COMPÉTENCES trouvé");
        
        let compBtn = document.getElementById('compToggleBtn');
        if (!compBtn) {
            compBtn = document.createElement('button');
            compBtn.id = 'compToggleBtn';
            compBtn.type = 'button';
            compBtn.className = 'btn btn-sm btn-outline-primary mb-3';
            compBtn.innerHTML = '🔽 Masquer les compétences';
            compGroup.parentNode.insertBefore(compBtn, compGroup);
        }
        
        let compVisible = true;
        compBtn.onclick = function(e) {
            e.preventDefault();
            if (compVisible) {
                compGroup.style.display = 'none';
                compBtn.innerHTML = '▶️ Voir les compétences';
                console.log("Compétences masquées");
            } else {
                compGroup.style.display = '';
                compBtn.innerHTML = '🔽 Masquer les compétences';
                console.log("Compétences affichées");
            }
            compVisible = !compVisible;
        };
    } else {
        console.log("⚠️ Groupe COMPÉTENCES non trouvé");
    }

    // ===== 2. SECTION LACUNES =====
    let lacGroup = document.querySelector('.lacunes-section .custom-checkbox-group');
    if (!lacGroup) {
        const allGroups = document.querySelectorAll('.custom-checkbox-group');
        for (let group of allGroups) {
            const prevText = group.previousElementSibling?.innerText || '';
            if (prevText.includes('Lacune') || prevText.includes('lacune') || prevText.includes('renforcer')) {
                lacGroup = group;
                break;
            }
        }
    }
    
    if (lacGroup) {
        console.log("✅ Groupe LACUNES trouvé");
        
        let lacBtn = document.getElementById('lacToggleBtn');
        if (!lacBtn) {
            lacBtn = document.createElement('button');
            lacBtn.id = 'lacToggleBtn';
            lacBtn.type = 'button';
            lacBtn.className = 'btn btn-sm btn-outline-danger mb-3';
            lacBtn.innerHTML = '🔽 Masquer les lacunes';
            lacGroup.parentNode.insertBefore(lacBtn, lacGroup);
        }
        
        let lacVisible = true;
        lacBtn.onclick = function(e) {
            e.preventDefault();
            if (lacVisible) {
                lacGroup.style.display = 'none';
                lacBtn.innerHTML = '▶️ Voir les lacunes';
                console.log("Lacunes masquées");
            } else {
                lacGroup.style.display = '';
                lacBtn.innerHTML = '🔽 Masquer les lacunes';
                console.log("Lacunes affichées");
            }
            lacVisible = !lacVisible;
        };
    } else {
        console.log("⚠️ Groupe LACUNES non trouvé");
    }

    // ===== 3. AJOUT MATIÈRE PERSONNALISÉE =====
    const addBtn = document.getElementById('btnAddMatiere');
    const inputMatiere = document.getElementById('customMatiere');
    
    if (addBtn && inputMatiere) {
        console.log("✅ Bouton ajout matière trouvé");
        
        addBtn.onclick = function() {
            const newMatiere = inputMatiere.value.trim();
            if (!newMatiere) {
                alert("Veuillez entrer un nom de matière");
                return;
            }
            
            console.log("Ajout de :", newMatiere);
            
            // Ajouter aux compétences
            if (compGroup) {
                const newId = 'comp_' + Date.now();
                const div = document.createElement('div');
                div.className = 'form-check custom-checkbox-wrapper';
                div.innerHTML = `
                    <input class="form-check-input custom-checkbox" type="checkbox" name="competences" value="${escapeHtml(newMatiere)}" id="${newId}" checked>
                    <label class="form-check-label ms-2" for="${newId}">${escapeHtml(newMatiere)}</label>
                `;
                compGroup.appendChild(div);
            }
            
            // Ajouter aux lacunes
            if (lacGroup) {
                const newId2 = 'lac_' + Date.now();
                const div = document.createElement('div');
                div.className = 'form-check custom-checkbox-wrapper-danger';
                div.innerHTML = `
                    <input class="form-check-input custom-checkbox checkbox-danger" type="checkbox" name="lacunes" value="${escapeHtml(newMatiere)}" id="${newId2}">
                    <label class="form-check-label ms-2" for="${newId2}">${escapeHtml(newMatiere)}</label>
                `;
                lacGroup.appendChild(div);
            }
            
            inputMatiere.value = '';
            alert("Matière '" + newMatiere + "' ajoutée avec succès !");
        };
    }
    
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }
    
    console.log("=== PROFIL JS TERMINE ===");
});