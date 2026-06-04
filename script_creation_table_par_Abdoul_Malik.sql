-------SUPPRIMER LES TABLES ---------
DROP TABLE IF EXISTS lacunes;
DROP TABLE IF EXISTS competences;
DROP TABLE IF EXISTS users;

-------CREATION DES TABLES --------


------- TABLE UTILISATEURS ---------

CREATE TABLE IF NOT EXISTS users (
    idusers INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom VARCHAR (30),
    prenom VARCHAR (50),
    email VARCHAR (40),
    telephone VARCHAR (20),
    niveau_etude VARCHAR (35),
    filiere VARCHAR (40),
    bio_courte VARCHAR (50),
    centre_d_interet VARCHAR(30),
    date_inscription TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP

);

---- TABLE LACUNES --------

CREATE TABLE IF NOT EXISTS lacunes (
    idcompetence INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    matiere VARCHAR(30),
    disponibilite VARCHAR (40),
    idusers INT,
    CONSTRAINT fk_users_lacunes
        FOREIGN KEY (idusers)
        REFERENCES users(idusers)
        ON DELETE CASCADE
        ON UPDATE CASCADE  
);

-----TABLE COMPETENCES--------
CREATE TABLE competences  (
    idcompetences INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    matiere VARCHAR (50),
    disponibilite VARCHAR(10),
    idusers INT,
    CONSTRAINT fk_competences_users
        FOREIGN KEY (idusers)
        REFERENCES users (idusers)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);