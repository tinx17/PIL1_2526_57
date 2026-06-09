-- =========================================
-- IFRI_MentorLink - Schéma Base de Données version finale
-- =========================================
-- SGBD : PostgreSQL 12+
-- =========================================

-- =========================================
-- SUPPRESSION DES TABLES (ordre inverse dépendances)
-- =========================================
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS matchings;
DROP TABLE IF EXISTS demandes_creneaux;
DROP TABLE IF EXISTS offres_creneaux;
DROP TABLE IF EXISTS users_creneaux;
DROP TABLE IF EXISTS demandes;
DROP TABLE IF EXISTS offres;
DROP TABLE IF EXISTS lacunes;
DROP TABLE IF EXISTS points_forts;
DROP TABLE IF EXISTS users;

-- =========================================
-- CRÉATION DES TABLES
-- =========================================

-- TABLE 1 : USERS (table parent)
-- Contient les informations de base de chaque utilisateur
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    telephone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    filiere VARCHAR(100) NOT NULL,
    niveau VARCHAR(50) NOT NULL,
    bio_courte TEXT,
    centres_interet TEXT,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_mise_à_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes pour recherche rapide
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_telephone ON users(telephone);


-- TABLE 1B : USERS_CRENEAUX
-- Disponibilités habituelles de chaque utilisateur (pour le profil)
CREATE TABLE users_creneaux (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    jour VARCHAR(15) NOT NULL CHECK (jour IN('lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche')),
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    --Clé étrangère vers users
    CONSTRAINT fk_users_creneau 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_uc_user_id ON users_creneaux(user_id);
CREATE INDEX idx_uc_jour ON users_creneaux(jour);


-- TABLE 2 : POINTS_FORTS
-- Matières que l'utilisateur maîtrise (compétences)
-- Source de vérité pour valider les offres créées
CREATE TABLE points_forts (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    --Clé  étrangère vers users
    CONSTRAINT fk_points_forts_user 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_pf_user_id ON points_forts(user_id);
CREATE INDEX idx_pf_matiere ON points_forts(matiere);
CREATE INDEX idx_pf_user_matiere ON points_forts(user_id, matiere);

-- TABLE 3 : LACUNES
-- Matières où l'utilisateur a besoin d'aide
-- Source de vérité pour valider les demandes créées
CREATE TABLE lacunes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    --Clé étrangère vers users
    CONSTRAINT fk_lacunes_user 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_lac_user_id ON lacunes(user_id);
CREATE INDEX idx_lac_matiere ON lacunes(matiere);
CREATE INDEX idx_lac_user_matiere ON lacunes(user_id, matiere);

-- TABLE 4 : OFFRES
-- Mentorat proposé par un utilisateur
-- Matière doit exister dans points_forts de cet utilisateur
CREATE TABLE offres (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    format VARCHAR(50) NOT NULL CHECK (format IN ('presentiel', 'en ligne', 'mixte')),
    description_offre TEXT,
    date_creation_offre TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    --Clé étrangère vers users
    CONSTRAINT fk_offres_user 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_offres_user_id ON offres(user_id);
CREATE INDEX idx_offres_matiere ON offres(matiere);
CREATE INDEX idx_offres_date_creation_offre ON offres(date_creation_offre);
CREATE INDEX idx_offres_user_matiere ON offres(user_id, matiere);

-- TABLE 4B : OFFRES_CRENEAUX
-- Créneaux horaires disponibles pour chaque offre
-- Une offre peut avoir plusieurs créneaux (ex: Lundi 18h-20h, Mercredi 17h-19h, Vendredi 19h-21h)
CREATE TABLE offres_creneaux (
    id SERIAL PRIMARY KEY,
    offre_id INT NOT NULL,
    jour VARCHAR(15) NOT NULL CHECK (jour IN('lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche')),
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    --Clé étrangère vers offres
    CONSTRAINT fk_offres_creneau 
        FOREIGN KEY (offre_id) REFERENCES offres(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_oc_offre_id ON offres_creneaux(offre_id);
CREATE INDEX idx_oc_jour ON offres_creneaux(jour);
CREATE INDEX idx_oc_horaires ON offres_creneaux(jour, heure_debut, heure_fin);

-- TABLE 5 : DEMANDES
-- Mentorat recherché par un utilisateur
-- Matière doit exister dans lacunes de cet utilisateur
CREATE TABLE demandes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    format VARCHAR(50) NOT NULL CHECK (format IN ('presentiel', 'en ligne', 'mixte')),
    description_demande TEXT,
    date_creation_demande TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    --Clé étrangère vers users
    CONSTRAINT fk_demandes_user 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_demandes_user_id ON demandes(user_id);
CREATE INDEX idx_demandes_matiere ON demandes(matiere);
CREATE INDEX idx_demandes_date_creation_demande ON demandes(date_creation_demande);
CREATE INDEX idx_demandes_user_matiere ON demandes(user_id, matiere);

-- TABLE 5B : DEMANDES_CRENEAUX
-- Créneaux horaires disponibles pour chaque demande
-- Une demande peut avoir plusieurs créneaux (ex: Lundi 18h-20h, Mercredi 17h-19h, Vendredi 19h-21h)
CREATE TABLE demandes_creneaux (
    id SERIAL PRIMARY KEY,
    demande_id INT NOT NULL,
    jour VARCHAR(15) NOT NULL CHECK (jour IN('lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche')),
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    --Clé étrangère vers demandes
    CONSTRAINT fk_demandes_creneau 
        FOREIGN KEY (demande_id) REFERENCES demandes(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_dc_demande_id ON demandes_creneaux(demande_id);
CREATE INDEX idx_dc_jour ON demandes_creneaux(jour);
CREATE INDEX idx_dc_horaires ON demandes_creneaux(jour, heure_debut, heure_fin);

-- TABLE 6 : MATCHINGS
-- Résultats du matching entre demandes et offres
-- Utile pour l'historique et la performance
CREATE TABLE matchings (
    id SERIAL PRIMARY KEY,
    demande_id INT NOT NULL,
    offre_id INT NOT NULL,
    score INT,
    date_matching TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    --Clés étrangères vers demandes et offres respectivement
    CONSTRAINT fk_matching_demande 
        FOREIGN KEY (demande_id) REFERENCES demandes(id) ON DELETE CASCADE,
    CONSTRAINT fk_matching_offre 
        FOREIGN KEY (offre_id) REFERENCES offres(id) ON DELETE CASCADE
);

CREATE INDEX idx_matching_demande_id ON matchings(demande_id);
CREATE INDEX idx_matching_offre_id ON matchings(offre_id);
CREATE INDEX idx_matching_score ON matchings(score DESC);

-- TABLE 7 : CONVERSATIONS
-- Chat entre deux utilisateurs
-- Créée quand un utilisateur clique "Contacter ce mentor" depuis un matching
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user1_id INT NOT NULL,
    user2_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    --Clés étrangères vers users
    CONSTRAINT fk_conv_user1 
        FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_conv_user2 
        FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    
    -- Une seule conversation entre deux utilisateurs
    CONSTRAINT uk_unique_conversation UNIQUE (user1_id, user2_id)
);

CREATE INDEX idx_conv_user1_id ON conversations(user1_id);
CREATE INDEX idx_conv_user2_id ON conversations(user2_id);
CREATE INDEX idx_conv_double_users ON conversations(user1_id, user2_id);
CREATE INDEX idx_conv_created_at ON conversations(created_at);

-- TABLE 8 : MESSAGES
-- Messages échangés dans une conversation
-- Champ 'lu' pour suivre l'état de lecture
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL,
    sender_id INT NOT NULL,
    contenu TEXT NOT NULL,
    lu BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    --Clés étrangères vers conversations et users respectivement
    CONSTRAINT fk_msg_conversation 
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_msg_sender 
        FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_msg_conversation_id ON messages(conversation_id);
CREATE INDEX idx_msg_sender_id ON messages(sender_id);
CREATE INDEX idx_msg_lu ON messages(lu);
CREATE INDEX idx_msg_created_at ON messages(created_at);
CREATE INDEX idx_msg_unread ON messages(lu, conversation_id) WHERE lu = FALSE;