-- =========================================================================
-- Structure de base de données PostgreSQL pour IFRI_MentorLink
-- Groupe 57 — PIL1_2526_57
-- Université d'Abomey-Calavi, Bénin
-- =========================================================================

-- Désactiver les contraintes temporairement pour réinitialisation propre si besoin
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- -------------------------------------------------------------------------
-- 1. CREATION DES TABLES
-- -------------------------------------------------------------------------

-- Matières
CREATE TABLE IF NOT EXISTS matieres (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE
);

-- Utilisateurs (Étendant AbstractUser)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    telephone VARCHAR(20) NOT NULL UNIQUE,
    photo_profil VARCHAR(100),
    filiere VARCHAR(10),
    niveau VARCHAR(5),
    disponibilites JSONB DEFAULT '{}'::jsonb,
    bio TEXT,
    date_inscription TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Relations de compétences utilisateurs (Many-to-Many)
CREATE TABLE IF NOT EXISTS user_competences (
    id SERIAL PRIMARY KEY,
    userprofile_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    matiere_id INTEGER NOT NULL REFERENCES matieres(id) ON DELETE CASCADE,
    CONSTRAINT unique_user_competence UNIQUE (userprofile_id, matiere_id)
);

-- Relations de lacunes utilisateurs (Many-to-Many)
CREATE TABLE IF NOT EXISTS user_lacunes (
    id SERIAL PRIMARY KEY,
    userprofile_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    matiere_id INTEGER NOT NULL REFERENCES matieres(id) ON DELETE CASCADE,
    CONSTRAINT unique_user_lacune UNIQUE (userprofile_id, matiere_id)
);

-- Offres/Demandes de Mentorat
CREATE TABLE IF NOT EXISTS offres_mentorat (
    id SERIAL PRIMARY KEY,
    auteur_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(10) NOT NULL CHECK (type IN ('offre', 'demande')),
    format VARCHAR(15) NOT NULL DEFAULT 'les_deux' CHECK (format IN ('presentiel', 'en_ligne', 'les_deux')),
    description TEXT,
    statut VARCHAR(10) NOT NULL DEFAULT 'active' CHECK (statut IN ('active', 'fermee')),
    disponibilites JSONB DEFAULT '{}'::jsonb,
    date_creation TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Relations de matières d'une offre (Many-to-Many)
CREATE TABLE IF NOT EXISTS offre_matieres (
    id SERIAL PRIMARY KEY,
    offrementorat_id INTEGER NOT NULL REFERENCES offres_mentorat(id) ON DELETE CASCADE,
    matiere_id INTEGER NOT NULL REFERENCES matieres(id) ON DELETE CASCADE,
    CONSTRAINT unique_offre_matiere UNIQUE (offrementorat_id, matiere_id)
);

-- Matchings
CREATE TABLE IF NOT EXISTS matchings (
    id SERIAL PRIMARY KEY,
    mentor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    mentore_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    score_compatibilite FLOAT NOT NULL DEFAULT 0.0,
    disponibilites_communes JSONB DEFAULT '{}'::jsonb,
    date_creation TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_mentor_mentore UNIQUE (mentor_id, mentore_id)
);

-- Relations de matières d'un matching (Many-to-Many)
CREATE TABLE IF NOT EXISTS matching_matieres (
    id SERIAL PRIMARY KEY,
    matching_id INTEGER NOT NULL REFERENCES matchings(id) ON DELETE CASCADE,
    matiere_id INTEGER NOT NULL REFERENCES matieres(id) ON DELETE CASCADE,
    CONSTRAINT unique_matching_matiere UNIQUE (matching_id, matiere_id)
);

-- Conversations
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    date_creation TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Participants des conversations (Many-to-Many)
CREATE TABLE IF NOT EXISTS conversation_participants (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    userprofile_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT unique_conversation_participant UNIQUE (conversation_id, userprofile_id)
);

-- Messages
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    auteur_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    contenu TEXT NOT NULL,
    date_envoi TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lu BOOLEAN NOT NULL DEFAULT FALSE
);

-- -------------------------------------------------------------------------
-- 2. INDEXATION DES CHAMPS CRITIQUES
-- -------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_telephone ON users(telephone);
CREATE INDEX IF NOT EXISTS idx_users_filiere ON users(filiere);
CREATE INDEX IF NOT EXISTS idx_offres_statut ON offres_mentorat(statut);
CREATE INDEX IF NOT EXISTS idx_messages_lu ON messages(lu);
CREATE INDEX IF NOT EXISTS idx_matchings_score ON matchings(score_compatibilite);

-- -------------------------------------------------------------------------
-- 3. JEU DE DONNÉES DE TEST (INSERTS)
-- -------------------------------------------------------------------------

-- Insertion des matières
INSERT INTO matieres (nom) VALUES
('Algorithmique'),
('Base de Données (SQL)'),
('Python'),
('Réseaux Informatiques'),
('Systèmes d exploitation'),
('Génie Logiciel'),
('Intelligence Artificielle'),
('Sécurité Informatique'),
('Web Development');

-- Insertion des utilisateurs (mots de passe hashés par défaut simulant PBKDF2 pour 'password123')
INSERT INTO users (password, username, nom, prenom, email, telephone, filiere, niveau, disponibilites, bio) VALUES
('pbkdf2_sha256$600000$randomSalt$encryptedPasswordHex1', 'jean.kodjo@uac.bj', 'KODJO', 'Jean', 'jean.kodjo@uac.bj', '+22990909090', 'GL', 'L3', '{"lundi": ["08h-10h", "14h-16h"], "mercredi": ["16h-18h"]}', 'Étudiant en L3 Génie Logiciel passionné par le Web et les bases de données.'),
('pbkdf2_sha256$600000$randomSalt$encryptedPasswordHex2', 'alice.adjovi@uac.bj', 'ADJOVI', 'Alice', 'alice.adjovi@uac.bj', '+22991919191', 'IA', 'L2', '{"mardi": ["10h-12h"], "jeudi": ["14h-16h"]}', 'Intéressée par le Machine Learning et la programmation Python.'),
('pbkdf2_sha256$600000$randomSalt$encryptedPasswordHex3', 'marc.sossa@uac.bj', 'SOSSA', 'Marc', 'marc.sossa@uac.bj', '+22992929292', 'SI', 'L3', '{"vendredi": ["08h-10h", "18h-20h"]}', 'Futur expert en sécurité informatique et cryptographie.'),
('pbkdf2_sha256$600000$randomSalt$encryptedPasswordHex4', 'clarisse.h@uac.bj', 'HOUNGBE', 'Clarisse', 'clarisse.h@uac.bj', '+22993939393', 'IM', 'L1', '{"lundi": ["14h-16h"], "mardi": ["10h-12h"]}', 'Débutante motivée à l IFRI en Licence 1 Internet & Multimédia.'),
('pbkdf2_sha256$600000$randomSalt$encryptedPasswordHex5', 'samuel.d@uac.bj', 'DOSSOU', 'Samuel', 'samuel.d@uac.bj', '+22994949494', 'SE_IoT', 'L2', '{"mercredi": ["16h-18h"], "jeudi": ["14h-16h"]}', 'Passionné par l IoT, Arduino et les microcontrôleurs.');

-- Insertion des compétences (Many-to-Many)
-- Jean (id 1) fort en Algorithmique (1) et Web (9)
INSERT INTO user_competences (userprofile_id, matiere_id) VALUES (1, 1), (1, 9);
-- Alice (id 2) forte en Python (3) et IA (7)
INSERT INTO user_competences (userprofile_id, matiere_id) VALUES (2, 3), (2, 7);
-- Marc (id 3) fort en Réseaux (4) et Sécurité (8)
INSERT INTO user_competences (userprofile_id, matiere_id) VALUES (3, 4), (3, 8);

-- Insertion des lacunes (Many-to-Many)
-- Clarisse (id 4) faible en Algorithmique (1) et Web (9)
INSERT INTO user_lacunes (userprofile_id, matiere_id) VALUES (4, 1), (4, 9);
-- Samuel (id 5) faible en Python (3) et Réseaux (4)
INSERT INTO user_lacunes (userprofile_id, matiere_id) VALUES (5, 3), (5, 4);

-- Insertion d'offres de mentorat
INSERT INTO offres_mentorat (auteur_id, type, format, description, disponibilites) VALUES
(1, 'offre', 'les_deux', 'Je peux vous accompagner sur les projets Web et les devoirs d algorithmique.', '{"lundi": ["08h-10h"], "mercredi": ["16h-18h"]}'),
(2, 'offre', 'en_ligne', 'Tutorat en Python et initiation au Machine Learning.', '{"mardi": ["10h-12h"]}'),
(4, 'demande', 'presentiel', 'Besoin d aide urgent pour assimiler les bases de l algorithmique.', '{"lundi": ["14h-16h"]}');

-- Insertion de matières pour les offres
INSERT INTO offre_matieres (offrementorat_id, matiere_id) VALUES (1, 1), (1, 9), (2, 3), (3, 1);

-- Insertion de matchings
INSERT INTO matchings (mentor_id, mentore_id, score_compatibilite, disponibilites_communes) VALUES
(1, 4, 0.85, '{"lundi": ["14h-16h"]}');

INSERT INTO matching_matieres (matching_id, matiere_id) VALUES (1, 1), (1, 9);

-- Insertion de conversations
INSERT INTO conversations (date_creation) VALUES (CURRENT_TIMESTAMP);

-- Insertion de participants de la conversation (Jean et Clarisse)
INSERT INTO conversation_participants (conversation_id, userprofile_id) VALUES (1, 1), (1, 4);

-- Insertion de messages de test
INSERT INTO messages (conversation_id, auteur_id, contenu, date_envoi, lu) VALUES
(1, 4, 'Bonjour Jean, j ai vu que tu proposes du mentorat en Algorithmique. J aurais besoin d aide pour le prochain TP.', CURRENT_TIMESTAMP - INTERVAL '1 hour', TRUE),
(1, 1, 'Salut Clarisse ! Avec plaisir. On peut s organiser un créneau en présentiel à la bibliothèque de l IFRI.', CURRENT_TIMESTAMP - INTERVAL '45 minutes', TRUE),
(1, 4, 'Super ! Le lundi à 14h te convient-il ?', CURRENT_TIMESTAMP - INTERVAL '30 minutes', FALSE);
