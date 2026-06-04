-- ============================================================================
-- 1. SUPPRESSION DES TABLES 
-- ============================================================================
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS demandes;
DROP TABLE IF EXISTS offres;
DROP TABLE IF EXISTS lacunes;
DROP TABLE IF EXISTS competences;
DROP TABLE IF EXISTS users;

-- ============================================================================
  ----CRÉATION DES TABLES
-- ============================================================================

-- TABLE: users
CREATE TABLE users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    telephone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    photo VARCHAR(255),
    filiere VARCHAR(100),
    niveau VARCHAR(50),
    bio_courte TEXT,
    centres_interet TEXT,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLE: competences
CREATE TABLE competences (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    disponibilite VARCHAR(255),
    CONSTRAINT fk_competence_user  
        FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
); 

-- TABLE: lacunes
CREATE TABLE lacunes (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    disponibilite VARCHAR(255),    
    CONSTRAINT fk_lacunes_user      
        FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
); 

-- TABLE: offres
CREATE TABLE offres (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    disponibilite VARCHAR(255) NOT NULL,
    format VARCHAR(20) NOT NULL,
    description_offres TEXT,
    date_offre TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_offres_user  
        FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_format_offres 
        CHECK (format IN ('présentiel', 'en ligne', 'mixte'))
);

-- TABLE: demandes
CREATE TABLE demandes (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    disponibilite VARCHAR(255) NOT NULL,
    format VARCHAR(20) NOT NULL,
    description_demande TEXT,
    date_demande TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    CONSTRAINT fk_demandes_user
        FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_format_demandes 
        CHECK (format IN ('présentiel', 'en ligne', 'mixte'))
);

-- TABLE: conversations
CREATE TABLE conversations (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user1_id INT NOT NULL,
    user2_id INT NOT NULL,
    date_conversation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_conversations_user1 
        FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_conversations_user2  
        FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT uk_unique_conversation 
        UNIQUE (user1_id, user2_id)
);

-- TABLE: messages
CREATE TABLE messages (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    conversation_id INT NOT NULL,
    sender_id INT NOT NULL,
    contenu TEXT NOT NULL,
    lu BOOLEAN DEFAULT FALSE,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_messages_conversation  
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_messages_sender 
        FOREIGN KEY (sender_id) REFERENCES users(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
);