DROP TABLE IF EXISTS answers CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS users CASCADE;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE SEQUENCE IF NOT EXISTS increment_pkey
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE IF NOT EXISTS answers (
    answer_id numeric DEFAULT nextval('increment_pkey'::regclass) NOT NULL,
    question_id numeric NOT NULL,
    user_id numeric NOT NULL,
    text character varying(1000) NOT NULL,
    up_votes numeric DEFAULT 0,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    user_preferred boolean DEFAULT false
);

COMMENT ON TABLE answers IS 'This tables stores the answers given by users on the platform';

CREATE TABLE IF NOT EXISTS blacklist (
    tokens character varying(200) NOT NULL
);

COMMENT ON TABLE blacklist IS 'This tables stores the blacklisted tokens';


CREATE TABLE IF NOT EXISTS questions (
    question_id numeric DEFAULT nextval('increment_pkey'::regclass) NOT NULL,
    user_id numeric NOT NULL,
    text character varying(200) NOT NULL,
    description character varying(1000),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
);

COMMENT ON TABLE questions IS 'This tables stores the details of a question asked on the platform';

CREATE TABLE IF NOT EXISTS users (
    user_id numeric DEFAULT nextval('increment_pkey'::regclass) NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50),
    username character varying(50) NOT NULL,
    email character varying(50),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    password character varying(500) NOT NULL
);

COMMENT ON TABLE users IS 'Store user details';

ALTER TABLE ONLY answers
    ADD CONSTRAINT answers_pkey PRIMARY KEY (answer_id);

ALTER TABLE ONLY questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (question_id);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);

ALTER TABLE ONLY answers
    ADD CONSTRAINT questions_question_id_fkey FOREIGN KEY (question_id) REFERENCES questions(question_id) ON UPDATE CASCADE NOT VALID;

ALTER TABLE ONLY questions
    ADD CONSTRAINT users_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE NOT VALID;

ALTER TABLE ONLY answers
    ADD CONSTRAINT users_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE NOT VALID;

ALTER TABLE users ADD UNIQUE (email, username);