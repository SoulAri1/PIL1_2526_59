-- =========================================================================
-- SCRIPT DE CRÉATION DE LA BASE DE DONNÉES : IFRI_MentorLink
-- =========================================================================

-- 1. Table des Utilisateurs (Comptes et Profils)
CREATE TABLE IF NOT EXISTS utilisateurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL, -- Stockera le mot de passe hashé
    filiere VARCHAR(100),
    niveau_etudes VARCHAR(50),
    bio TEXT,
    photo_profil VARCHAR(255),
    disponibilites TEXT, -- Format texte libre ou JSON (ex: "Lundi 14h-16h")
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table des Matières / Compétences
CREATE TABLE IF NOT EXISTS matieres (
    id SERIAL PRIMARY KEY,
    nom_matiere VARCHAR(100) UNIQUE NOT NULL
);

-- 3. Table de liaison pour les COMPÉTENCES (Points forts / Mentors)
CREATE TABLE IF NOT EXISTS competences_mentor (
    utilisateur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
    matiere_id INT REFERENCES matieres(id) ON DELETE CASCADE,
    PRIMARY KEY (utilisateur_id, matiere_id)
);

-- 4. Table de liaison pour les LACUNES (Points faibles / Mentorés)
CREATE TABLE IF NOT EXISTS lacunes_mentore (
    utilisateur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
    matiere_id INT REFERENCES matieres(id) ON DELETE CASCADE,
    PRIMARY KEY (utilisateur_id, matiere_id)
);

-- 5. Table des Annonces (Offres et Demandes de mentorat)
CREATE TABLE IF NOT EXISTS annonces (
    id SERIAL PRIMARY KEY,
    utilisateur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
    type_annonce VARCHAR(10) CHECK (type_annonce IN ('OFFRE', 'DEMANDE')) NOT NULL,
    format_mentorat VARCHAR(20) CHECK (format_mentorat IN ('PRESENTIEL', 'EN_LIGNE', 'LES_DEUX')) NOT NULL,
    date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statut VARCHAR(20) DEFAULT 'ACTIF' CHECK (statut IN ('ACTIF', 'RESOLU'))
);

-- Table de liaison entre Annonces et Matières (Une annonce peut cibler plusieurs matières)
CREATE TABLE IF NOT EXISTS annonces_matieres (
    annonce_id INT REFERENCES annonces(id) ON DELETE CASCADE,
    matiere_id INT REFERENCES matieres(id) ON DELETE CASCADE,
    PRIMARY KEY (annonce_id, matiere_id)
);

-- 6. Table de la Messagerie Instantanée
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    expediteur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
    destinataire_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
    contenu TEXT NOT NULL,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);