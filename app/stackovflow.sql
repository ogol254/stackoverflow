CREATE TABLE IF NOT EXISTS answers (
    answer_id serial PRIMARY KEY NOT NULL,
    question_id numeric NOT NULL,
    user_id numeric NOT NULL,
    text character varying(1000) NOT NULL,
    up_votes numeric DEFAULT 0,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    user_preferred boolean DEFAULT false
);


CREATE TABLE IF NOT EXISTS blacklist (
    tokens character varying(200) NOT NULL
);



CREATE TABLE IF NOT EXISTS questions (
    question_id serial PRIMARY KEY NOT NULL,
    user_id numeric NOT NULL,
    text character varying(200) NOT NULL,
    description character varying(1000),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50),
    username character varying(50) NOT NULL,
    email character varying(50),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    password character varying(500) NOT NULL
);




