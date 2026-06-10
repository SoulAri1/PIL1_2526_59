-- =========================================================================
-- IFRI MentorLink - SCHEMA COMPLET (Version finale corrigée)
-- =========================================================================

-- Supprimer les tables existantes (ordre inverse des dépendances)
DROP TABLE IF EXISTS annonces_matieres CASCADE;
DROP TABLE IF EXISTS annonces CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS competences_mentor CASCADE;
DROP TABLE IF EXISTS lacunes_mentore CASCADE;
DROP TABLE IF EXISTS utilisateurs CASCADE;
DROP TABLE IF EXISTS matieres CASCADE;

-- 1. Table des Matières / Compétences
CREATE TABLE IF NOT EXISTS matieres (
    id SERIAL PRIMARY KEY,
    nom_matiere VARCHAR(100) UNIQUE NOT NULL
);

-- 2. Table des Utilisateurs (Comptes et Profils) - Version corrigée
CREATE TABLE IF NOT EXISTS utilisateurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    filiere VARCHAR(100),
    niveau_etudes VARCHAR(50),
    bio TEXT,
    centres_interet TEXT,
    photo_profil VARCHAR(255),
    disponibilites TEXT,
    reset_token VARCHAR(100),
    reset_token_expires TIMESTAMP,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    statut VARCHAR(20) DEFAULT 'ACTIF' CHECK (statut IN ('ACTIF', 'RESOLU')),
    date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table de liaison entre Annonces et Matières
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

-- 7. Index pour optimiser les performances
CREATE INDEX IF NOT EXISTS idx_messages_expediteur ON messages(expediteur_id);
CREATE INDEX IF NOT EXISTS idx_messages_destinataire ON messages(destinataire_id);
CREATE INDEX IF NOT EXISTS idx_annonces_type ON annonces(type_annonce);
CREATE INDEX IF NOT EXISTS idx_annonces_statut ON annonces(statut);