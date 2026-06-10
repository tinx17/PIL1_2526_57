--
-- PostgreSQL database dump
--

\restrict pELQ6eGdWQFVplAoolIqQQnSp0XxYcue3Ux3nprhq6GWXKaowhMrKsG77C84HCR

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.messaging_message DROP CONSTRAINT messaging_message_conversation_id_3db4d3d1_fk_messaging;
ALTER TABLE ONLY public.messaging_message DROP CONSTRAINT messaging_message_auteur_id_c6e9c1dc_fk_accounts_userprofile_id;
ALTER TABLE ONLY public.messaging_conversation_participants DROP CONSTRAINT messaging_conversati_userprofile_id_24abd37d_fk_accounts_;
ALTER TABLE ONLY public.messaging_conversation_participants DROP CONSTRAINT messaging_conversati_conversation_id_890e9e37_fk_messaging;
ALTER TABLE ONLY public.matching_offrementorat_matieres DROP CONSTRAINT matching_offrementor_offrementorat_id_33b7381b_fk_matching_;
ALTER TABLE ONLY public.matching_offrementorat_matieres DROP CONSTRAINT matching_offrementor_matiere_id_02223384_fk_accounts_;
ALTER TABLE ONLY public.matching_offrementorat DROP CONSTRAINT matching_offrementor_auteur_id_85e6bdb0_fk_accounts_;
ALTER TABLE ONLY public.matching_matching DROP CONSTRAINT matching_matching_mentore_id_5061f29b_fk_accounts_;
ALTER TABLE ONLY public.matching_matching DROP CONSTRAINT matching_matching_mentor_id_55b626be_fk_accounts_userprofile_id;
ALTER TABLE ONLY public.matching_matching_matieres_communes DROP CONSTRAINT matching_matching_ma_matiere_id_6a2fbd96_fk_accounts_;
ALTER TABLE ONLY public.matching_matching_matieres_communes DROP CONSTRAINT matching_matching_ma_matching_id_808fed7e_fk_matching_;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_accounts_userprofile_id;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE ONLY public.accounts_userprofile_groups DROP CONSTRAINT accounts_userprofile_userprofile_id_b7fb6469_fk_accounts_;
ALTER TABLE ONLY public.accounts_userprofile_competences DROP CONSTRAINT accounts_userprofile_userprofile_id_80d51889_fk_accounts_;
ALTER TABLE ONLY public.accounts_userprofile_user_permissions DROP CONSTRAINT accounts_userprofile_userprofile_id_4acaf5a0_fk_accounts_;
ALTER TABLE ONLY public.accounts_userprofile_lacunes DROP CONSTRAINT accounts_userprofile_userprofile_id_0f580f02_fk_accounts_;
ALTER TABLE ONLY public.accounts_userprofile_user_permissions DROP CONSTRAINT accounts_userprofile_permission_id_a9b2b32b_fk_auth_perm;
ALTER TABLE ONLY public.accounts_userprofile_lacunes DROP CONSTRAINT accounts_userprofile_matiere_id_ab8ea11a_fk_accounts_;
ALTER TABLE ONLY public.accounts_userprofile_competences DROP CONSTRAINT accounts_userprofile_matiere_id_9468ec3a_fk_accounts_;
ALTER TABLE ONLY public.accounts_userprofile_groups DROP CONSTRAINT accounts_userprofile_groups_group_id_74ae51cf_fk_auth_group_id;
DROP INDEX public.messaging_message_conversation_id_3db4d3d1;
DROP INDEX public.messaging_message_auteur_id_c6e9c1dc;
DROP INDEX public.messaging_conversation_participants_userprofile_id_24abd37d;
DROP INDEX public.messaging_conversation_participants_conversation_id_890e9e37;
DROP INDEX public.matching_offrementorat_matieres_offrementorat_id_33b7381b;
DROP INDEX public.matching_offrementorat_matieres_matiere_id_02223384;
DROP INDEX public.matching_offrementorat_auteur_id_85e6bdb0;
DROP INDEX public.matching_matching_mentore_id_5061f29b;
DROP INDEX public.matching_matching_mentor_id_55b626be;
DROP INDEX public.matching_matching_matieres_communes_matiere_id_6a2fbd96;
DROP INDEX public.matching_matching_matieres_communes_matching_id_808fed7e;
DROP INDEX public.django_session_session_key_c0390e0f_like;
DROP INDEX public.django_session_expire_date_a5c62663;
DROP INDEX public.django_admin_log_user_id_c564eba6;
DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX public.auth_permission_content_type_id_2f476e4b;
DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX public.auth_group_name_a6ea08ec_like;
DROP INDEX public.accounts_userprofile_username_8e8bc851_like;
DROP INDEX public.accounts_userprofile_user_permissions_userprofile_id_4acaf5a0;
DROP INDEX public.accounts_userprofile_user_permissions_permission_id_a9b2b32b;
DROP INDEX public.accounts_userprofile_telephone_20e45166_like;
DROP INDEX public.accounts_userprofile_lacunes_userprofile_id_0f580f02;
DROP INDEX public.accounts_userprofile_lacunes_matiere_id_ab8ea11a;
DROP INDEX public.accounts_userprofile_groups_userprofile_id_b7fb6469;
DROP INDEX public.accounts_userprofile_groups_group_id_74ae51cf;
DROP INDEX public.accounts_userprofile_email_2dffe4f7_like;
DROP INDEX public.accounts_userprofile_competences_userprofile_id_80d51889;
DROP INDEX public.accounts_userprofile_competences_matiere_id_9468ec3a;
DROP INDEX public.accounts_matiere_nom_3ce65962_like;
ALTER TABLE ONLY public.messaging_message DROP CONSTRAINT messaging_message_pkey;
ALTER TABLE ONLY public.messaging_conversation DROP CONSTRAINT messaging_conversation_pkey;
ALTER TABLE ONLY public.messaging_conversation_participants DROP CONSTRAINT messaging_conversation_participants_pkey;
ALTER TABLE ONLY public.messaging_conversation_participants DROP CONSTRAINT messaging_conversation_p_conversation_id_userprof_f9ada44b_uniq;
ALTER TABLE ONLY public.matching_offrementorat DROP CONSTRAINT matching_offrementorat_pkey;
ALTER TABLE ONLY public.matching_offrementorat_matieres DROP CONSTRAINT matching_offrementorat_matieres_pkey;
ALTER TABLE ONLY public.matching_offrementorat_matieres DROP CONSTRAINT matching_offrementorat_m_offrementorat_id_matiere_876339ef_uniq;
ALTER TABLE ONLY public.matching_matching DROP CONSTRAINT matching_matching_pkey;
ALTER TABLE ONLY public.matching_matching DROP CONSTRAINT matching_matching_mentor_id_mentore_id_2d55abcc_uniq;
ALTER TABLE ONLY public.matching_matching_matieres_communes DROP CONSTRAINT matching_matching_matieres_communes_pkey;
ALTER TABLE ONLY public.matching_matching_matieres_communes DROP CONSTRAINT matching_matching_matier_matching_id_matiere_id_9bacf9e5_uniq;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_username_key;
ALTER TABLE ONLY public.accounts_userprofile_user_permissions DROP CONSTRAINT accounts_userprofile_user_permissions_pkey;
ALTER TABLE ONLY public.accounts_userprofile_user_permissions DROP CONSTRAINT accounts_userprofile_use_userprofile_id_permissio_22053107_uniq;
ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_telephone_key;
ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_pkey;
ALTER TABLE ONLY public.accounts_userprofile_lacunes DROP CONSTRAINT accounts_userprofile_lacunes_pkey;
ALTER TABLE ONLY public.accounts_userprofile_lacunes DROP CONSTRAINT accounts_userprofile_lac_userprofile_id_matiere_i_e20a6434_uniq;
ALTER TABLE ONLY public.accounts_userprofile_groups DROP CONSTRAINT accounts_userprofile_groups_pkey;
ALTER TABLE ONLY public.accounts_userprofile_groups DROP CONSTRAINT accounts_userprofile_gro_userprofile_id_group_id_36cd9fa6_uniq;
ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_email_key;
ALTER TABLE ONLY public.accounts_userprofile_competences DROP CONSTRAINT accounts_userprofile_competences_pkey;
ALTER TABLE ONLY public.accounts_userprofile_competences DROP CONSTRAINT accounts_userprofile_com_userprofile_id_matiere_i_ceac407a_uniq;
ALTER TABLE ONLY public.accounts_matiere DROP CONSTRAINT accounts_matiere_pkey;
ALTER TABLE ONLY public.accounts_matiere DROP CONSTRAINT accounts_matiere_nom_key;
DROP TABLE public.messaging_message;
DROP TABLE public.messaging_conversation_participants;
DROP TABLE public.messaging_conversation;
DROP TABLE public.matching_offrementorat_matieres;
DROP TABLE public.matching_offrementorat;
DROP TABLE public.matching_matching_matieres_communes;
DROP TABLE public.matching_matching;
DROP TABLE public.django_session;
DROP TABLE public.django_migrations;
DROP TABLE public.django_content_type;
DROP TABLE public.django_admin_log;
DROP TABLE public.auth_permission;
DROP TABLE public.auth_group_permissions;
DROP TABLE public.auth_group;
DROP TABLE public.accounts_userprofile_user_permissions;
DROP TABLE public.accounts_userprofile_lacunes;
DROP TABLE public.accounts_userprofile_groups;
DROP TABLE public.accounts_userprofile_competences;
DROP TABLE public.accounts_userprofile;
DROP TABLE public.accounts_matiere;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts_matiere; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts_matiere (
    id bigint NOT NULL,
    nom character varying(100) NOT NULL
);


--
-- Name: accounts_matiere_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.accounts_matiere ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_matiere_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_userprofile; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts_userprofile (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    nom character varying(100) NOT NULL,
    prenom character varying(100) NOT NULL,
    email character varying(254) NOT NULL,
    telephone character varying(20) NOT NULL,
    photo_profil character varying(100),
    filiere character varying(10) NOT NULL,
    niveau character varying(5) NOT NULL,
    disponibilites jsonb NOT NULL,
    bio text NOT NULL,
    date_inscription timestamp with time zone NOT NULL
);


--
-- Name: accounts_userprofile_competences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts_userprofile_competences (
    id bigint NOT NULL,
    userprofile_id bigint NOT NULL,
    matiere_id bigint NOT NULL
);


--
-- Name: accounts_userprofile_competences_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.accounts_userprofile_competences ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_userprofile_competences_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_userprofile_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts_userprofile_groups (
    id bigint NOT NULL,
    userprofile_id bigint NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: accounts_userprofile_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.accounts_userprofile_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_userprofile_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.accounts_userprofile ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_userprofile_lacunes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts_userprofile_lacunes (
    id bigint NOT NULL,
    userprofile_id bigint NOT NULL,
    matiere_id bigint NOT NULL
);


--
-- Name: accounts_userprofile_lacunes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.accounts_userprofile_lacunes ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_userprofile_lacunes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_userprofile_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts_userprofile_user_permissions (
    id bigint NOT NULL,
    userprofile_id bigint NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: accounts_userprofile_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.accounts_userprofile_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_userprofile_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: matching_matching; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.matching_matching (
    id bigint NOT NULL,
    score_compatibilite double precision NOT NULL,
    disponibilites_communes jsonb NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    mentor_id bigint NOT NULL,
    mentore_id bigint NOT NULL
);


--
-- Name: matching_matching_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.matching_matching ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.matching_matching_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: matching_matching_matieres_communes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.matching_matching_matieres_communes (
    id bigint NOT NULL,
    matching_id bigint NOT NULL,
    matiere_id bigint NOT NULL
);


--
-- Name: matching_matching_matieres_communes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.matching_matching_matieres_communes ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.matching_matching_matieres_communes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: matching_offrementorat; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.matching_offrementorat (
    id bigint NOT NULL,
    type character varying(10) NOT NULL,
    disponibilites jsonb NOT NULL,
    format character varying(15) NOT NULL,
    description text NOT NULL,
    statut character varying(10) NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    auteur_id bigint NOT NULL
);


--
-- Name: matching_offrementorat_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.matching_offrementorat ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.matching_offrementorat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: matching_offrementorat_matieres; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.matching_offrementorat_matieres (
    id bigint NOT NULL,
    offrementorat_id bigint NOT NULL,
    matiere_id bigint NOT NULL
);


--
-- Name: matching_offrementorat_matieres_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.matching_offrementorat_matieres ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.matching_offrementorat_matieres_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: messaging_conversation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messaging_conversation (
    id bigint NOT NULL,
    date_creation timestamp with time zone NOT NULL
);


--
-- Name: messaging_conversation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.messaging_conversation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.messaging_conversation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: messaging_conversation_participants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messaging_conversation_participants (
    id bigint NOT NULL,
    conversation_id bigint NOT NULL,
    userprofile_id bigint NOT NULL
);


--
-- Name: messaging_conversation_participants_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.messaging_conversation_participants ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.messaging_conversation_participants_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: messaging_message; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messaging_message (
    id bigint NOT NULL,
    contenu text NOT NULL,
    date_envoi timestamp with time zone NOT NULL,
    lu boolean NOT NULL,
    auteur_id bigint NOT NULL,
    conversation_id bigint NOT NULL
);


--
-- Name: messaging_message_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.messaging_message ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.messaging_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: accounts_matiere; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_matiere (id, nom) FROM stdin;
51	React
52	Node.js
53	Python
54	Java
55	C++
56	TypeScript
57	SQL
58	Machine Learning
59	DevOps
60	Cybersécurité
61	Algorithmique
62	UML
63	Cloud AWS
64	Linux
65	GraphQL
66	Statistiques
\.


--
-- Data for Name: accounts_userprofile; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_userprofile (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, nom, prenom, email, telephone, photo_profil, filiere, niveau, disponibilites, bio, date_inscription) FROM stdin;
18	pbkdf2_sha256$1200000$GhdLQxqmZLlHWcdKkl76Qk$qK/QNTFbxcajscW3yLzKiRgoqciLOSzY7jmxYJ0h7PA=	\N	f	eckson.ahouansou@uac.bj			f	t	2026-06-10 17:00:50.966004+01	AHOUANSOU	Eckson	eckson.ahouansou@uac.bj	+22990909090		GL	L3	{"lundi": ["8h-10h", "14h-16h"], "mercredi": ["16h-18h"]}	Étudiant en L3 Génie Logiciel passionné par le Web et les bases de données.	2026-06-10 17:00:52.232094+01
19	pbkdf2_sha256$1200000$eVawU6nCtgavr2nnwVuoPs$sILsxjkfYwAdf7VZPMgS+9JK5kNTF7PoI30auw4x/X8=	\N	f	giovanni.gbasse@uac.bj			f	t	2026-06-10 17:00:52.29533+01	GBASSE	Giovanni	giovanni.gbasse@uac.bj	+22991919191		IA	L2	{"jeudi": ["14h-16h"], "mardi": ["10h-12h"]}	Intéressé par le Machine Learning et la programmation Python.	2026-06-10 17:00:53.567493+01
20	pbkdf2_sha256$1200000$KZ8WGEeo6Z5UKh46skpUJA$VhspzuDHPMHibd9z5WxT+U8oTbb4z9hi7RF/DVl1DzI=	\N	f	exaucee.bognon@uac.bj			f	t	2026-06-10 17:00:53.588844+01	BOGNON	Exaucée	exaucee.bognon@uac.bj	+22992929292		SI	L3	{"vendredi": ["8h-10h", "18h-20h"]}	Future experte en sécurité informatique et administration système Linux.	2026-06-10 17:00:54.843239+01
21	pbkdf2_sha256$1200000$wE5km2Uu6EWohaA13tTJGe$AW2hDSZ+kdvqyh2tnypSLksmQUiKYxZwBtUxGiVtPTQ=	\N	f	malik.fagnon@uac.bj			f	t	2026-06-10 17:00:54.899432+01	FAGNON	Malik	malik.fagnon@uac.bj	+22993939393		IM	L1	{"lundi": ["14h-16h"], "mardi": ["10h-12h"]}	Débutant motivé à l'IFRI en Licence 1 Internet & Multimédia.	2026-06-10 17:00:56.157931+01
22	pbkdf2_sha256$1200000$XZnToIqT2vrNBKu99sgRkf$iKo3UXX0xIUU4F5XGtme0oA5uFsfdZF1KTxgZMh3adE=	\N	f	royal.ahoumenou@uac.bj			f	t	2026-06-10 17:00:56.209087+01	AHOUMENOU	Royal	royal.ahoumenou@uac.bj	+22994949494		SE_IoT	L2	{"jeudi": ["14h-16h"], "mercredi": ["16h-18h"]}	Passionné par l'IoT, Arduino et les microcontrôleurs.	2026-06-10 17:00:57.456445+01
\.


--
-- Data for Name: accounts_userprofile_competences; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_userprofile_competences (id, userprofile_id, matiere_id) FROM stdin;
62	18	51
63	18	53
64	18	61
65	19	53
66	19	58
67	19	66
68	20	60
69	20	64
70	20	57
71	21	56
72	21	62
73	22	55
74	22	64
75	22	59
\.


--
-- Data for Name: accounts_userprofile_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_userprofile_groups (id, userprofile_id, group_id) FROM stdin;
\.


--
-- Data for Name: accounts_userprofile_lacunes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_userprofile_lacunes (id, userprofile_id, matiere_id) FROM stdin;
45	18	57
46	18	59
47	19	51
48	19	56
49	20	65
50	20	51
51	21	61
52	21	53
53	22	53
54	22	58
\.


--
-- Data for Name: accounts_userprofile_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_userprofile_user_permissions (id, userprofile_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	3	add_permission
6	Can change permission	3	change_permission
7	Can delete permission	3	delete_permission
8	Can view permission	3	view_permission
9	Can add group	2	add_group
10	Can change group	2	change_group
11	Can delete group	2	delete_group
12	Can view group	2	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Matière	6	add_matiere
22	Can change Matière	6	change_matiere
23	Can delete Matière	6	delete_matiere
24	Can view Matière	6	view_matiere
25	Can add Profil utilisateur	7	add_userprofile
26	Can change Profil utilisateur	7	change_userprofile
27	Can delete Profil utilisateur	7	delete_userprofile
28	Can view Profil utilisateur	7	view_userprofile
29	Can add Offre de mentorat	9	add_offrementorat
30	Can change Offre de mentorat	9	change_offrementorat
31	Can delete Offre de mentorat	9	delete_offrementorat
32	Can view Offre de mentorat	9	view_offrementorat
33	Can add Matching	8	add_matching
34	Can change Matching	8	change_matching
35	Can delete Matching	8	delete_matching
36	Can view Matching	8	view_matching
37	Can add Conversation	10	add_conversation
38	Can change Conversation	10	change_conversation
39	Can delete Conversation	10	delete_conversation
40	Can view Conversation	10	view_conversation
41	Can add Message	11	add_message
42	Can change Message	11	change_message
43	Can delete Message	11	delete_message
44	Can view Message	11	view_message
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	contenttypes	contenttype
5	sessions	session
6	accounts	matiere
7	accounts	userprofile
8	matching	matching
9	matching	offrementorat
10	messaging	conversation
11	messaging	message
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-06-10 06:04:58.730141+01
2	contenttypes	0002_remove_content_type_name	2026-06-10 06:04:58.748512+01
3	auth	0001_initial	2026-06-10 06:04:58.816679+01
4	auth	0002_alter_permission_name_max_length	2026-06-10 06:04:58.825446+01
5	auth	0003_alter_user_email_max_length	2026-06-10 06:04:58.829834+01
6	auth	0004_alter_user_username_opts	2026-06-10 06:04:58.8347+01
7	auth	0005_alter_user_last_login_null	2026-06-10 06:04:58.843787+01
8	auth	0006_require_contenttypes_0002	2026-06-10 06:04:58.845614+01
9	auth	0007_alter_validators_add_error_messages	2026-06-10 06:04:58.848615+01
10	auth	0008_alter_user_username_max_length	2026-06-10 06:04:58.852961+01
11	auth	0009_alter_user_last_name_max_length	2026-06-10 06:04:58.858852+01
12	auth	0010_alter_group_name_max_length	2026-06-10 06:04:58.868396+01
13	auth	0011_update_proxy_permissions	2026-06-10 06:04:58.871965+01
14	auth	0012_alter_user_first_name_max_length	2026-06-10 06:04:58.876754+01
15	accounts	0001_initial	2026-06-10 06:04:59.007759+01
16	admin	0001_initial	2026-06-10 06:04:59.042966+01
17	admin	0002_logentry_remove_auto_add	2026-06-10 06:04:59.052502+01
18	admin	0003_logentry_add_action_flag_choices	2026-06-10 06:04:59.059583+01
19	matching	0001_initial	2026-06-10 06:04:59.173002+01
20	messaging	0001_initial	2026-06-10 06:04:59.224528+01
21	sessions	0001_initial	2026-06-10 06:04:59.237518+01
22	accounts	0002_add_m1_m2_niveaux	2026-06-10 13:42:59.371387+01
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
o7b0b0sya6yblrhnsgg6jo3xtvuod7i2	.eJxVjMsKwjAQRf8layl5NQ-Xgmv9gzCTmZCittA0K_HfpdCFbs8997xFgr7V1BuvaSJxFkqL0y9EyA-e9wVyXvq8teFAbbi-YHre1ntdZr4c3t-5Qqt7kw1aCDKoQqCNsyNnF01mJYMBKS1SKRmlB-0iYsDRea9JRVLWk3Pi8wUbWzaZ:1wXKss:8UBgJ8rQIlCzrGOqTU33a05ef45GV4hx-XEto48L54A	2026-06-24 16:30:26.330404+01
w1z4fmxg2cpqq5q0a754r7awvsv6uip0	.eJxVi0sKwjAQQO8yaynNb5J0KbjWG4RJJiFFbaFpVuLdRehCt-_zgkB9r6G3vIWZYQIFp18WKd3z8hWU0tqXvQ0HasPlSfPjut3quuTz0f3NlVqFCWzRwjs5Fm84s2XDMhoRk9BoUBP6KHX03mWFmVGN1ilJhKytc8qYAu8P5v811A:1wXBGB:j6LeVZgZXZBlUTIZ9lhtLeGgrpVFuMwh-YSxGwouu-o	2026-06-24 06:13:51.501274+01
rwqjwtgmbcp0nbiijm0idimht7j777ho	.eJxVi0sKwjAQQO8yaylJzG-6FLrWG4RJJiFFbaFpVuLdRehCt-_zgkB9r6G3vIWZYQQNp18WKd3z8hWU0tqXvQ0HasP0pPlx3W51XfLl6P7mSq3CCNIz2cgCvXCGEb0uRTFZgcxnVDI6hcKJotFGL42TWmSbrM_SGWkMwfsD39E1bA:1wXBHJ:tFjnyTnOP0c1YoWbtLrV26XXBVkgEsEEEBHqH6MFYJY	2026-06-24 06:15:01.569057+01
hsm1ds8to3km3y5u07v9z49cdbmsw6z5	.eJxVi0sKwjAQQO8yaylJzG-6FLrWG4RJJiFFbaFpVuLdRehCt-_zgkB9r6G3vIWZYQQNp18WKd3z8hWU0tqXvQ0HasP0pPlx3W51XfLl6P7mSq3CCNIz2cgCvXCGEb0uRTFZgcxnVDI6hcKJotFGL42TWmSbrM_SGWkMwfsD39E1bA:1wXJ5p:m6uziaIvoRW6L11w53WnkQGajtDFg-h7hKK5XbDlwCg	2026-06-24 14:35:41.566758+01
2f258pyjd2ann36bfcv3oh79nhq2ozdh	.eJxVi0sKwjAQQO8yaynJ5GuXQtd6gzKdSUhRU2jalXh3EbrQ7fu8YKR9K-Pe0jrOAj1oDadfOBHfU_0aYl72urXuQK0bnjQ_ruutLDVdju5vLtQK9GCcRFKa0AUyPmYmlowkKuiJY0afrD5bI4FEskenMloyyGiitSlmeH8AKEg29A:1wXKex:r_LGUHPovR_-b2a0WqR-PSX8_eg_gwenvjzKOMULI-s	2026-06-24 16:16:03.22363+01
\.


--
-- Data for Name: matching_matching; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.matching_matching (id, score_compatibilite, disponibilites_communes, date_creation, mentor_id, mentore_id) FROM stdin;
\.


--
-- Data for Name: matching_matching_matieres_communes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.matching_matching_matieres_communes (id, matching_id, matiere_id) FROM stdin;
\.


--
-- Data for Name: matching_offrementorat; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.matching_offrementorat (id, type, disponibilites, format, description, statut, date_creation, auteur_id) FROM stdin;
10	offre	{"lundi": ["8h-10h"], "mercredi": ["16h-18h"]}	les_deux	Je propose mon aide pour le développement frontend avec React ou pour préparer les TPs d'algorithmique.	active	2026-06-10 17:00:57.479645+01	18
11	offre	{"mardi": ["10h-12h"]}	en_ligne	Tutorat en Python et initiation au Machine Learning.	active	2026-06-10 17:00:57.489976+01	19
12	demande	{"lundi": ["14h-16h"]}	presentiel	Recherche de l'aide en algorithmique pour mieux comprendre la complexité des algorithmes et les structures de données.	active	2026-06-10 17:00:57.497395+01	21
\.


--
-- Data for Name: matching_offrementorat_matieres; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.matching_offrementorat_matieres (id, offrementorat_id, matiere_id) FROM stdin;
12	10	51
13	10	61
14	11	58
15	11	53
16	12	61
\.


--
-- Data for Name: messaging_conversation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messaging_conversation (id, date_creation) FROM stdin;
9	2026-06-10 17:00:57.504904+01
\.


--
-- Data for Name: messaging_conversation_participants; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messaging_conversation_participants (id, conversation_id, userprofile_id) FROM stdin;
17	9	18
18	9	21
\.


--
-- Data for Name: messaging_message; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messaging_message (id, contenu, date_envoi, lu, auteur_id, conversation_id) FROM stdin;
26	Bonjour Eckson, j'ai vu que tu proposes du mentorat en Algorithmique. J'aurais besoin d'aide pour le prochain TP.	2026-06-10 16:00:57.514769+01	t	21	9
27	Salut Malik ! Avec plaisir. On peut s'organiser un créneau en présentiel à la bibliothèque de l'IFRI.	2026-06-10 16:15:57.520366+01	t	18	9
28	Super ! Le lundi à 14h te convient-il ?	2026-06-10 16:30:57.525784+01	f	21	9
\.


--
-- Name: accounts_matiere_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_matiere_id_seq', 66, true);


--
-- Name: accounts_userprofile_competences_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_userprofile_competences_id_seq', 75, true);


--
-- Name: accounts_userprofile_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_userprofile_groups_id_seq', 1, false);


--
-- Name: accounts_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_userprofile_id_seq', 22, true);


--
-- Name: accounts_userprofile_lacunes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_userprofile_lacunes_id_seq', 54, true);


--
-- Name: accounts_userprofile_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_userprofile_user_permissions_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 44, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 11, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 22, true);


--
-- Name: matching_matching_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.matching_matching_id_seq', 2, true);


--
-- Name: matching_matching_matieres_communes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.matching_matching_matieres_communes_id_seq', 1, false);


--
-- Name: matching_offrementorat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.matching_offrementorat_id_seq', 12, true);


--
-- Name: matching_offrementorat_matieres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.matching_offrementorat_matieres_id_seq', 16, true);


--
-- Name: messaging_conversation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.messaging_conversation_id_seq', 9, true);


--
-- Name: messaging_conversation_participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.messaging_conversation_participants_id_seq', 18, true);


--
-- Name: messaging_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.messaging_message_id_seq', 28, true);


--
-- Name: accounts_matiere accounts_matiere_nom_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_matiere
    ADD CONSTRAINT accounts_matiere_nom_key UNIQUE (nom);


--
-- Name: accounts_matiere accounts_matiere_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_matiere
    ADD CONSTRAINT accounts_matiere_pkey PRIMARY KEY (id);


--
-- Name: accounts_userprofile_competences accounts_userprofile_com_userprofile_id_matiere_i_ceac407a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_competences
    ADD CONSTRAINT accounts_userprofile_com_userprofile_id_matiere_i_ceac407a_uniq UNIQUE (userprofile_id, matiere_id);


--
-- Name: accounts_userprofile_competences accounts_userprofile_competences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_competences
    ADD CONSTRAINT accounts_userprofile_competences_pkey PRIMARY KEY (id);


--
-- Name: accounts_userprofile accounts_userprofile_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_email_key UNIQUE (email);


--
-- Name: accounts_userprofile_groups accounts_userprofile_gro_userprofile_id_group_id_36cd9fa6_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_groups
    ADD CONSTRAINT accounts_userprofile_gro_userprofile_id_group_id_36cd9fa6_uniq UNIQUE (userprofile_id, group_id);


--
-- Name: accounts_userprofile_groups accounts_userprofile_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_groups
    ADD CONSTRAINT accounts_userprofile_groups_pkey PRIMARY KEY (id);


--
-- Name: accounts_userprofile_lacunes accounts_userprofile_lac_userprofile_id_matiere_i_e20a6434_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_lacunes
    ADD CONSTRAINT accounts_userprofile_lac_userprofile_id_matiere_i_e20a6434_uniq UNIQUE (userprofile_id, matiere_id);


--
-- Name: accounts_userprofile_lacunes accounts_userprofile_lacunes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_lacunes
    ADD CONSTRAINT accounts_userprofile_lacunes_pkey PRIMARY KEY (id);


--
-- Name: accounts_userprofile accounts_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_pkey PRIMARY KEY (id);


--
-- Name: accounts_userprofile accounts_userprofile_telephone_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_telephone_key UNIQUE (telephone);


--
-- Name: accounts_userprofile_user_permissions accounts_userprofile_use_userprofile_id_permissio_22053107_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_user_permissions
    ADD CONSTRAINT accounts_userprofile_use_userprofile_id_permissio_22053107_uniq UNIQUE (userprofile_id, permission_id);


--
-- Name: accounts_userprofile_user_permissions accounts_userprofile_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_user_permissions
    ADD CONSTRAINT accounts_userprofile_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: accounts_userprofile accounts_userprofile_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_username_key UNIQUE (username);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: matching_matching_matieres_communes matching_matching_matier_matching_id_matiere_id_9bacf9e5_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_matching_matieres_communes
    ADD CONSTRAINT matching_matching_matier_matching_id_matiere_id_9bacf9e5_uniq UNIQUE (matching_id, matiere_id);


--
-- Name: matching_matching_matieres_communes matching_matching_matieres_communes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_matching_matieres_communes
    ADD CONSTRAINT matching_matching_matieres_communes_pkey PRIMARY KEY (id);


--
-- Name: matching_matching matching_matching_mentor_id_mentore_id_2d55abcc_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_matching
    ADD CONSTRAINT matching_matching_mentor_id_mentore_id_2d55abcc_uniq UNIQUE (mentor_id, mentore_id);


--
-- Name: matching_matching matching_matching_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_matching
    ADD CONSTRAINT matching_matching_pkey PRIMARY KEY (id);


--
-- Name: matching_offrementorat_matieres matching_offrementorat_m_offrementorat_id_matiere_876339ef_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_offrementorat_matieres
    ADD CONSTRAINT matching_offrementorat_m_offrementorat_id_matiere_876339ef_uniq UNIQUE (offrementorat_id, matiere_id);


--
-- Name: matching_offrementorat_matieres matching_offrementorat_matieres_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_offrementorat_matieres
    ADD CONSTRAINT matching_offrementorat_matieres_pkey PRIMARY KEY (id);


--
-- Name: matching_offrementorat matching_offrementorat_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_offrementorat
    ADD CONSTRAINT matching_offrementorat_pkey PRIMARY KEY (id);


--
-- Name: messaging_conversation_participants messaging_conversation_p_conversation_id_userprof_f9ada44b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messaging_conversation_participants
    ADD CONSTRAINT messaging_conversation_p_conversation_id_userprof_f9ada44b_uniq UNIQUE (conversation_id, userprofile_id);


--
-- Name: messaging_conversation_participants messaging_conversation_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messaging_conversation_participants
    ADD CONSTRAINT messaging_conversation_participants_pkey PRIMARY KEY (id);


--
-- Name: messaging_conversation messaging_conversation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messaging_conversation
    ADD CONSTRAINT messaging_conversation_pkey PRIMARY KEY (id);


--
-- Name: messaging_message messaging_message_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messaging_message
    ADD CONSTRAINT messaging_message_pkey PRIMARY KEY (id);


--
-- Name: accounts_matiere_nom_3ce65962_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_matiere_nom_3ce65962_like ON public.accounts_matiere USING btree (nom varchar_pattern_ops);


--
-- Name: accounts_userprofile_competences_matiere_id_9468ec3a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_competences_matiere_id_9468ec3a ON public.accounts_userprofile_competences USING btree (matiere_id);


--
-- Name: accounts_userprofile_competences_userprofile_id_80d51889; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_competences_userprofile_id_80d51889 ON public.accounts_userprofile_competences USING btree (userprofile_id);


--
-- Name: accounts_userprofile_email_2dffe4f7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_email_2dffe4f7_like ON public.accounts_userprofile USING btree (email varchar_pattern_ops);


--
-- Name: accounts_userprofile_groups_group_id_74ae51cf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_groups_group_id_74ae51cf ON public.accounts_userprofile_groups USING btree (group_id);


--
-- Name: accounts_userprofile_groups_userprofile_id_b7fb6469; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_groups_userprofile_id_b7fb6469 ON public.accounts_userprofile_groups USING btree (userprofile_id);


--
-- Name: accounts_userprofile_lacunes_matiere_id_ab8ea11a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_lacunes_matiere_id_ab8ea11a ON public.accounts_userprofile_lacunes USING btree (matiere_id);


--
-- Name: accounts_userprofile_lacunes_userprofile_id_0f580f02; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_lacunes_userprofile_id_0f580f02 ON public.accounts_userprofile_lacunes USING btree (userprofile_id);


--
-- Name: accounts_userprofile_telephone_20e45166_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_telephone_20e45166_like ON public.accounts_userprofile USING btree (telephone varchar_pattern_ops);


--
-- Name: accounts_userprofile_user_permissions_permission_id_a9b2b32b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_user_permissions_permission_id_a9b2b32b ON public.accounts_userprofile_user_permissions USING btree (permission_id);


--
-- Name: accounts_userprofile_user_permissions_userprofile_id_4acaf5a0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_user_permissions_userprofile_id_4acaf5a0 ON public.accounts_userprofile_user_permissions USING btree (userprofile_id);


--
-- Name: accounts_userprofile_username_8e8bc851_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_userprofile_username_8e8bc851_like ON public.accounts_userprofile USING btree (username varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: matching_matching_matieres_communes_matching_id_808fed7e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matching_matching_matieres_communes_matching_id_808fed7e ON public.matching_matching_matieres_communes USING btree (matching_id);


--
-- Name: matching_matching_matieres_communes_matiere_id_6a2fbd96; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matching_matching_matieres_communes_matiere_id_6a2fbd96 ON public.matching_matching_matieres_communes USING btree (matiere_id);


--
-- Name: matching_matching_mentor_id_55b626be; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matching_matching_mentor_id_55b626be ON public.matching_matching USING btree (mentor_id);


--
-- Name: matching_matching_mentore_id_5061f29b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matching_matching_mentore_id_5061f29b ON public.matching_matching USING btree (mentore_id);


--
-- Name: matching_offrementorat_auteur_id_85e6bdb0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matching_offrementorat_auteur_id_85e6bdb0 ON public.matching_offrementorat USING btree (auteur_id);


--
-- Name: matching_offrementorat_matieres_matiere_id_02223384; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matching_offrementorat_matieres_matiere_id_02223384 ON public.matching_offrementorat_matieres USING btree (matiere_id);


--
-- Name: matching_offrementorat_matieres_offrementorat_id_33b7381b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matching_offrementorat_matieres_offrementorat_id_33b7381b ON public.matching_offrementorat_matieres USING btree (offrementorat_id);


--
-- Name: messaging_conversation_participants_conversation_id_890e9e37; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX messaging_conversation_participants_conversation_id_890e9e37 ON public.messaging_conversation_participants USING btree (conversation_id);


--
-- Name: messaging_conversation_participants_userprofile_id_24abd37d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX messaging_conversation_participants_userprofile_id_24abd37d ON public.messaging_conversation_participants USING btree (userprofile_id);


--
-- Name: messaging_message_auteur_id_c6e9c1dc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX messaging_message_auteur_id_c6e9c1dc ON public.messaging_message USING btree (auteur_id);


--
-- Name: messaging_message_conversation_id_3db4d3d1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX messaging_message_conversation_id_3db4d3d1 ON public.messaging_message USING btree (conversation_id);


--
-- Name: accounts_userprofile_groups accounts_userprofile_groups_group_id_74ae51cf_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_groups
    ADD CONSTRAINT accounts_userprofile_groups_group_id_74ae51cf_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_userprofile_competences accounts_userprofile_matiere_id_9468ec3a_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_competences
    ADD CONSTRAINT accounts_userprofile_matiere_id_9468ec3a_fk_accounts_ FOREIGN KEY (matiere_id) REFERENCES public.accounts_matiere(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_userprofile_lacunes accounts_userprofile_matiere_id_ab8ea11a_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_lacunes
    ADD CONSTRAINT accounts_userprofile_matiere_id_ab8ea11a_fk_accounts_ FOREIGN KEY (matiere_id) REFERENCES public.accounts_matiere(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_userprofile_user_permissions accounts_userprofile_permission_id_a9b2b32b_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_user_permissions
    ADD CONSTRAINT accounts_userprofile_permission_id_a9b2b32b_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_userprofile_lacunes accounts_userprofile_userprofile_id_0f580f02_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_lacunes
    ADD CONSTRAINT accounts_userprofile_userprofile_id_0f580f02_fk_accounts_ FOREIGN KEY (userprofile_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_userprofile_user_permissions accounts_userprofile_userprofile_id_4acaf5a0_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_user_permissions
    ADD CONSTRAINT accounts_userprofile_userprofile_id_4acaf5a0_fk_accounts_ FOREIGN KEY (userprofile_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_userprofile_competences accounts_userprofile_userprofile_id_80d51889_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_competences
    ADD CONSTRAINT accounts_userprofile_userprofile_id_80d51889_fk_accounts_ FOREIGN KEY (userprofile_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_userprofile_groups accounts_userprofile_userprofile_id_b7fb6469_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_userprofile_groups
    ADD CONSTRAINT accounts_userprofile_userprofile_id_b7fb6469_fk_accounts_ FOREIGN KEY (userprofile_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_accounts_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_accounts_userprofile_id FOREIGN KEY (user_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_matching_matieres_communes matching_matching_ma_matching_id_808fed7e_fk_matching_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_matching_matieres_communes
    ADD CONSTRAINT matching_matching_ma_matching_id_808fed7e_fk_matching_ FOREIGN KEY (matching_id) REFERENCES public.matching_matching(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_matching_matieres_communes matching_matching_ma_matiere_id_6a2fbd96_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_matching_matieres_communes
    ADD CONSTRAINT matching_matching_ma_matiere_id_6a2fbd96_fk_accounts_ FOREIGN KEY (matiere_id) REFERENCES public.accounts_matiere(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_matching matching_matching_mentor_id_55b626be_fk_accounts_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_matching
    ADD CONSTRAINT matching_matching_mentor_id_55b626be_fk_accounts_userprofile_id FOREIGN KEY (mentor_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_matching matching_matching_mentore_id_5061f29b_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_matching
    ADD CONSTRAINT matching_matching_mentore_id_5061f29b_fk_accounts_ FOREIGN KEY (mentore_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_offrementorat matching_offrementor_auteur_id_85e6bdb0_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_offrementorat
    ADD CONSTRAINT matching_offrementor_auteur_id_85e6bdb0_fk_accounts_ FOREIGN KEY (auteur_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_offrementorat_matieres matching_offrementor_matiere_id_02223384_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_offrementorat_matieres
    ADD CONSTRAINT matching_offrementor_matiere_id_02223384_fk_accounts_ FOREIGN KEY (matiere_id) REFERENCES public.accounts_matiere(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_offrementorat_matieres matching_offrementor_offrementorat_id_33b7381b_fk_matching_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matching_offrementorat_matieres
    ADD CONSTRAINT matching_offrementor_offrementorat_id_33b7381b_fk_matching_ FOREIGN KEY (offrementorat_id) REFERENCES public.matching_offrementorat(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: messaging_conversation_participants messaging_conversati_conversation_id_890e9e37_fk_messaging; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messaging_conversation_participants
    ADD CONSTRAINT messaging_conversati_conversation_id_890e9e37_fk_messaging FOREIGN KEY (conversation_id) REFERENCES public.messaging_conversation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: messaging_conversation_participants messaging_conversati_userprofile_id_24abd37d_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messaging_conversation_participants
    ADD CONSTRAINT messaging_conversati_userprofile_id_24abd37d_fk_accounts_ FOREIGN KEY (userprofile_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: messaging_message messaging_message_auteur_id_c6e9c1dc_fk_accounts_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messaging_message
    ADD CONSTRAINT messaging_message_auteur_id_c6e9c1dc_fk_accounts_userprofile_id FOREIGN KEY (auteur_id) REFERENCES public.accounts_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: messaging_message messaging_message_conversation_id_3db4d3d1_fk_messaging; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messaging_message
    ADD CONSTRAINT messaging_message_conversation_id_3db4d3d1_fk_messaging FOREIGN KEY (conversation_id) REFERENCES public.messaging_conversation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict pELQ6eGdWQFVplAoolIqQQnSp0XxYcue3Ux3nprhq6GWXKaowhMrKsG77C84HCR

