
```markdown
# 🌟 IFRI MentorLink

<p align="center">
  <img src="static/img/IFRI_MentorLink.png" alt="Logo IFRI MentorLink" width="150px"/>
</p>

<h3 align="center">Plateforme d'entraide académique</h3>

<p align="center">
  Connecter les mentors et mentorés de l'Institut de Formation et de Recherche en Informatique (IFRI / UAC)
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-blue?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-Supabase-green?logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap" alt="Bootstrap">
  <img src="https://img.shields.io/badge/Statut-Terminé-brightgreen" alt="Statut">
</p>

---

## 📖 À propos

**IFRI MentorLink** est une application web développée avec **Flask** qui permet aux étudiants de l'IFRI de se connecter pour du mentorat académique. L'application propose :

- ✨ **Matching intelligent** avec score de compatibilité en pourcentage
- 💬 **Messagerie instantanée** avec notifications en temps réel
- 👤 **Profils détaillés** (compétences, lacunes, bio, photo)
- 📢 **Annonces** d'offres et demandes de mentorat
- 📊 **Dashboard** avec statistiques et suivi des binômes

<p align="center">
  <img src="static/img/mentorlink-demo.png" alt="Aperçu IFRI MentorLink" width="800px" style="border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
</p>

---

## 👥 Équipe Groupe 59

| # | Nom & Prénom | Filière | Rôle |
|---|--------------|---------|------|
| 1 | **AGOSSOU Ariel Gracias** | IA | Intégrateur Principal / Chef de projet |
| 2 | **MEHINTO Miclette** | SI | Authentification & Sécurité |
| 3 | **MENSAH Eliel Othny** | GL | Gestion des profils |
| 4 | **DJIKPESSE Théoson Moralèce Mawutin** | GL | Base de données |
| 5 | **HOUNHOWAKOU Prince Freddy** | IA | Design UI / UX |
| 6 | **KPOMALEGNI Josias Précieux Bidossessi** | SI | Algorithme de matching |
| 7 | **AIZAN Yves Lauriano** | SE&IoT | Messagerie initiale |

> 📦 **Dépôt GitHub :** [https://github.com/SoulAri1/PIL1_2526_59.git](https://github.com/SoulAri1/PIL1_2526_59.git)

---

## 🚀 Fonctionnalités

### 🔐 Authentification
- Inscription sécurisée avec hachage des mots de passe
- Connexion / Déconnexion
- **Mot de passe oublié** avec lien de réinitialisation

### 👤 Profil utilisateur
- 40+ matières informatiques pré-définies
- Ajout dynamique de matières personnalisées
- **Bio** et **centres d'intérêt**
- **Upload de photo de profil** (PNG, JPG, JPEG, GIF)
- Masquage/affichage des sections compétences/lacunes

### 🎯 Matching intelligent
- Score de compatibilité calculé en **pourcentage (0-100%)**
- Basé sur :
  - Matières communes (60%)
  - Même filière (20%)
  - Même niveau (10%)
  - Disponibilités communes (10%)

### 💬 Messagerie instantanée
- Envoi et réception en **temps réel** (polling 3s)
- **Notifications navigateur** à la réception
- Historique des conversations
- Compteur de caractères (2000 max)
- Envoi par touche **Entrée**

### 📢 Annonces
- Publication d'offres ou demandes de mentorat
- Réponse aux annonces
- Suppression de ses propres annonces

### 📊 Dashboard
- **Menu latéral rétractable**
- Cartes statistiques avec **compteurs animés**
- Recherche en temps réel dans le tableau des binômes

---

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| **Backend** | Python 3.10+ / Flask 3.0 |
| **Base de données** | PostgreSQL (Supabase) |
| **Frontend** | Bootstrap 5 / Jinja2 / JavaScript |
| **Sécurité** | Werkzeug (hachage) |
| **Communication** | AJAX + Polling |

<p align="center">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
</p>

---

## 📦 Installation

### Prérequis

- Python 3.10 ou supérieur
- Git
- Compte Supabase (gratuit)

### Étapes d'installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/SoulAri1/PIL1_2526_59.git
cd PIL1_2526_59

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement virtuel
# Windows :
venv\Scripts\activate
# Mac / Linux :
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
python app.py
```

### Accès à l'application

Ouvrez votre navigateur et accédez à : **http://127.0.0.1:5000**

### 🔐 Comptes de test

| Email | Mot de passe | Rôle |
|-------|--------------|------|
| amadou.diallo@ifri-uac.bj | password123 | Mentor (IA) |
| fatou.kouma@ifri-uac.bj | password123 | Mentor (GL) |
| benoit.houndji@ifri-uac.bj | password123 | Mentoré (IA) |

---

## 📁 Structure du projet

```
PIL1_2526_59/
├── app.py                      # Point d'entrée Flask
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── rapport.html                # Rapport de projet
│
├── modules/                    # Backend - Blueprints
│   ├── auth.py                 # Authentification
│   ├── profil.py               # Gestion des profils
│   ├── matching.py             # Algorithme de matching
│   ├── messagerie.py           # API messagerie
│   ├── annonces.py             # Module annonces
│   └── dashboard.py            # Tableau de bord
│
├── templates/                  # Frontend - Vues Jinja2
│   ├── base.html               # Layout parent
│   ├── index.html              # Page d'accueil
│   ├── login.html              # Connexion
│   ├── register.html           # Inscription
│   ├── forgot_password.html    # Mot de passe oublié
│   ├── reset_password.html     # Réinitialisation
│   ├── profil.html             # Formulaire profil
│   ├── matching.html           # Résultats matching
│   ├── chat.html               # Messagerie
│   ├── dashboard.html          # Tableau de bord
│   └── annonces.html           # Annonces
│
├── static/                     # Assets
│   ├── css/style.css           # Styles
│   ├── js/                     # JavaScript
│   ├── img/                    # Images
│   └── uploads/                # Photos de profil
│
└── database/                   # Base de données
    ├── connection.py           # Connexion Supabase
    ├── schema.sql              # Structure SQL
    └── seed.sql                # Données de test
```

---

## 🧮 Algorithme de matching

Le score de compatibilité est calculé sur **100 points** :

| Critère | Calcul | Points max |
|---------|--------|------------|
| 📚 Matières communes | 3 points par matière (max 20) | 60 |
| 🏫 Même filière | 20 points si identique | 20 |
| 📖 Même niveau | 10 points si identique | 10 |
| ⏰ Disponibilités communes | 1 point par créneau (max 10) | 10 |
| **Total** | | **100 points = 100%** |

> 💡 **Exemple :** 4 matières communes (12 pts) + même filière (20 pts) + même niveau (10 pts) + 3 créneaux (3 pts) = **45% de compatibilité**

---

## 📡 API Messagerie

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/messagerie/api/envoyer` | Envoi d'un message |
| `GET` | `/messagerie/api/historique` | Historique des messages |
| `GET` | `/messagerie/api/nouveaux_messages` | Nouveaux messages (polling) |
| `GET` | `/messagerie/conversations` | Liste des conversations |
| `GET` | `/messagerie/chat/<id>` | Page du chat |

---

## 📸 Aperçu

| Page | Description |
|------|-------------|
| 🏠 **Accueil** | Landing page avec présentation du projet |
| 🔐 **Connexion/Inscription** | Formulaires sécurisés |
| 👤 **Profil** | Gestion des compétences, lacunes, bio, photo |
| 🎯 **Matching** | Suggestions de mentors/mentorés avec score |
| 💬 **Messagerie** | Chat en temps réel avec notifications |
| 📢 **Annonces** | Offres et demandes de mentorat |
| 📊 **Dashboard** | Statistiques et suivi des binômes |

---

## 🤝 Contribution

Ce projet a été réalisé par le **Groupe 59** dans le cadre du cours **Projet Intégrateur** (PIL1) à l'IFRI.


## 📝 État du projet

| Module | Statut | Responsable |
|--------|--------|-------------|
| Authentification | ✅ 100% | Membre 2 |
| Profil utilisateur | ✅ 100% | Membre 3 |
| Matching (pourcentage) | ✅ 100% | Membre 6 |
| Messagerie (polling + notifications) | ✅ 100% | Membre 1 & 7 |
| Dashboard (menu rétractable) | ✅ 100% | Membre 1 |
| Annonces (offres/demandes) | ✅ 100% | Membre 1 |
| Base de données | ✅ 100% | Membre 4 |
| Design UI | ✅ 100% | Membre 5 |
| Documentation | ✅ 100% | Membre 1 |

---

## 📄 Licence

Ce projet est réalisé dans un cadre pédagogique à l'**Institut de Formation et de Recherche en Informatique (IFRI)** – Université d'Abomey-Calavi.

---

## 🙏 Remerciements

<p align="center">
  <i>« Seul on va plus vite, ensemble on va plus loin.🍀 »</i> — Proverbe africain
</p>

---

<p align="center">
  <b>© 2025-2026 IFRI MentorLink — Groupe 59 — Projet réalisé en 7 jours</b>
</p>
```

## ✅ Ce que contient ce README

| Section | Description |
|---------|-------------|
| 🎨 Badges | Statut, technologies, version |
| 👥 Équipe | Tableau des 7 membres avec rôles |
| 🚀 Fonctionnalités | Liste complète |
| 🛠️ Stack technique | Technologies utilisées |
| 📦 Installation | Guide pas à pas |
| 📁 Structure | Arborescence du projet |
| 🧮 Algorithme | Tableau du matching en pourcentage |
| 📡 API | Endpoints disponibles |
| 📸 Aperçu | Description des pages |
| 🤝 Contribution | Encadrement et accès GitHub |
| 📝 État | Tableau d'avancement |

---

