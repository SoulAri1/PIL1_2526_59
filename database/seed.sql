-- =========================================================================
-- IFRI MentorLink - DONNÉES DE TEST (Version corrigée)
-- =========================================================================

-- Supprimer les anciennes données (ordre inverse des dépendances)
DELETE FROM annonces_matieres;
DELETE FROM annonces;
DELETE FROM messages;
DELETE FROM competences_mentor;
DELETE FROM lacunes_mentore;
DELETE FROM utilisateurs;
DELETE FROM matieres;

-- 1. Matières informatiques (40+)
INSERT INTO matieres (nom_matiere) VALUES
('Python'), ('Java'), ('JavaScript'), ('HTML/CSS'), ('SQL'), ('NoSQL'),
('Algorithmique'), ('Structures de données'), ('Génie logiciel'), ('UML'), ('Design patterns'),
('React'), ('Node.js'), ('Django'), ('Flask'), ('Spring Boot'),
('Machine Learning'), ('Deep Learning'), ('Traitement du langage naturel'), ('Vision par ordinateur'),
('Réseaux TCP/IP'), ('Cybersécurité'), ('DevOps'), ('Docker'), ('Kubernetes'),
('Cloud computing'), ('Big Data'), ('Spark'), ('Data visualization'),
('Sécurité web'), ('Tests unitaires'), ('CI/CD'), ('Git'), ('REST API'), ('GraphQL'),
('Programmation orientée objet'), ('Programmation fonctionnelle'), ('Base de données distribuées'),
('Systèmes d''exploitation'), ('Architecture logicielle');

-- 2. Utilisateurs tests
INSERT INTO utilisateurs (id, nom, prenom, email, telephone, mot_de_passe, filiere, niveau_etudes, bio, centres_interet, disponibilites) VALUES
(1, 'DIALLO', 'Amadou', 'amadou.diallo@ifri-uac.bj', '+229 97 00 00 01', 'scrypt:32768:8:1$lPWnZqrX9Z0jSPrZ$c8f5e9a7b2c4d6e8f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3', 'Licence Intelligence Artificielle(IA)', 'L3', 'Passionné par l''IA et le Machine Learning. Je veux aider les débutants.', 'IA, Deep Learning, Robotique', 'Lundi 14h-16h; Mercredi 10h-12h'),
(2, 'KOUMA', 'Fatou', 'fatou.kouma@ifri-uac.bj', '+229 97 00 00 02', 'scrypt:32768:8:1$lPWnZqrX9Z0jSPrZ$c8f5e9a7b2c4d6e8f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3', 'Licence Génie Logiciel(GL)', 'L2', 'Développeuse full-stack, je maîtrise React et Node.js.', 'Dev Web, UI/UX, Open Source', 'Mardi 16h-18h; Jeudi 14h-16h'),
(3, 'ZINSOU', 'Marc', 'marc.zinsou@ifri-uac.bj', '+229 97 00 00 03', 'scrypt:32768:8:1$lPWnZqrX9Z0jSPrZ$c8f5e9a7b2c4d6e8f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3', 'Master Cybersécurité', 'M1', 'Expert en cybersécurité et réseaux. Je propose de l''aide sur les CTF.', 'Cybersécurité, Ethical Hacking', 'Lundi 18h-20h; Samedi 10h-12h'),
(4, 'ADJOVI', 'Grace', 'grace.adjovi@ifri-uac.bj', '+229 97 00 00 04', 'scrypt:32768:8:1$lPWnZqrX9Z0jSPrZ$c8f5e9a7b2c4d6e8f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3', 'Licence Data Science', 'L3', 'Data analyste, je maîtrise Python, SQL et la visualisation.', 'Data Science, IA, Statistiques', 'Mercredi 16h-18h; Vendredi 14h-16h'),
(5, 'HOUNDJI', 'Benoit', 'benoit.houndji@ifri-uac.bj', '+229 97 00 00 05', 'scrypt:32768:8:1$lPWnZqrX9Z0jSPrZ$c8f5e9a7b2c4d6e8f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3', 'Licence Intelligence Artificielle(IA)', 'L2', 'Débutant en IA, j''ai besoin d''aide en Python et Machine Learning.', 'IA, Programmation', 'Lundi 10h-12h; Mercredi 14h-16h');

-- 3. Compétences des mentors
INSERT INTO competences_mentor (utilisateur_id, matiere_id) VALUES
(1, (SELECT id FROM matieres WHERE nom_matiere = 'Python')),
(1, (SELECT id FROM matieres WHERE nom_matiere = 'Machine Learning')),
(1, (SELECT id FROM matieres WHERE nom_matiere = 'Deep Learning')),
(2, (SELECT id FROM matieres WHERE nom_matiere = 'JavaScript')),
(2, (SELECT id FROM matieres WHERE nom_matiere = 'React')),
(2, (SELECT id FROM matieres WHERE nom_matiere = 'Node.js')),
(2, (SELECT id FROM matieres WHERE nom_matiere = 'Git')),
(3, (SELECT id FROM matieres WHERE nom_matiere = 'Cybersécurité')),
(3, (SELECT id FROM matieres WHERE nom_matiere = 'Réseaux TCP/IP')),
(3, (SELECT id FROM matieres WHERE nom_matiere = 'Sécurité web')),
(4, (SELECT id FROM matieres WHERE nom_matiere = 'Python')),
(4, (SELECT id FROM matieres WHERE nom_matiere = 'SQL')),
(4, (SELECT id FROM matieres WHERE nom_matiere = 'Data visualization'));

-- 4. Lacunes des mentorés
INSERT INTO lacunes_mentore (utilisateur_id, matiere_id) VALUES
(5, (SELECT id FROM matieres WHERE nom_matiere = 'Python')),
(5, (SELECT id FROM matieres WHERE nom_matiere = 'Algorithmique')),
(5, (SELECT id FROM matieres WHERE nom_matiere = 'Machine Learning'));

-- 5. Annonces
INSERT INTO annonces (utilisateur_id, type_annonce, format_mentorat, statut) VALUES
(1, 'OFFRE', 'LES_DEUX', 'ACTIF'),
(2, 'OFFRE', 'EN_LIGNE', 'ACTIF'),
(3, 'OFFRE', 'PRESENTIEL', 'ACTIF'),
(5, 'DEMANDE', 'EN_LIGNE', 'ACTIF');

INSERT INTO annonces_matieres (annonce_id, matiere_id) VALUES
(1, (SELECT id FROM matieres WHERE nom_matiere = 'Python')),
(1, (SELECT id FROM matieres WHERE nom_matiere = 'Machine Learning')),
(2, (SELECT id FROM matieres WHERE nom_matiere = 'JavaScript')),
(2, (SELECT id FROM matieres WHERE nom_matiere = 'React')),
(3, (SELECT id FROM matieres WHERE nom_matiere = 'Cybersécurité')),
(4, (SELECT id FROM matieres WHERE nom_matiere = 'Python'));

-- 6. Messages de test
INSERT INTO messages (expediteur_id, destinataire_id, contenu) VALUES
(1, 5, 'Bonjour Benoit, je peux t''aider en Python et Machine Learning. Contacte-moi !'),
(5, 1, 'Merci Amadou, j''ai vraiment besoin d''aide sur les algorithmes de ML.'),
(2, 1, 'Salut Amadou, intéressé par un échange sur les architectures full-stack ?');