--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg120+1)
-- Dumped by pg_dump version 17.5 (Debian 17.5-1.pgdg120+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cities; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.cities (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.cities OWNER TO admin;

--
-- Name: cities_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.cities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cities_id_seq OWNER TO admin;

--
-- Name: cities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.cities_id_seq OWNED BY public.cities.id;


--
-- Name: shops; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.shops (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    city_id integer NOT NULL,
    street_id integer NOT NULL,
    house character varying(255) NOT NULL,
    opening_time time without time zone NOT NULL,
    closing_time time without time zone NOT NULL
);


ALTER TABLE public.shops OWNER TO admin;

--
-- Name: shops_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.shops_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shops_id_seq OWNER TO admin;

--
-- Name: shops_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.shops_id_seq OWNED BY public.shops.id;


--
-- Name: streets; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.streets (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    city_id integer NOT NULL
);


ALTER TABLE public.streets OWNER TO admin;

--
-- Name: streets_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.streets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.streets_id_seq OWNER TO admin;

--
-- Name: streets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.streets_id_seq OWNED BY public.streets.id;


--
-- Name: cities id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.cities ALTER COLUMN id SET DEFAULT nextval('public.cities_id_seq'::regclass);


--
-- Name: shops id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.shops ALTER COLUMN id SET DEFAULT nextval('public.shops_id_seq'::regclass);


--
-- Name: streets id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.streets ALTER COLUMN id SET DEFAULT nextval('public.streets_id_seq'::regclass);


--
-- Data for Name: cities; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.cities (id, name) FROM stdin;
1	Ульяновск
2	Москва
3	Казань
5	Пермь
6	Волгоград
\.


--
-- Data for Name: shops; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.shops (id, name, city_id, street_id, house, opening_time, closing_time) FROM stdin;
4	Продукты	1	1	22б	10:00:00	22:00:00
5	Электроника	1	3	10а	08:00:00	21:00:00
6	Продукты	2	2	13	08:00:00	22:00:00
\.


--
-- Data for Name: streets; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.streets (id, name, city_id) FROM stdin;
1	Кирова	1
2	Соборная	2
3	Рябикова	1
4	Набережная	1
\.


--
-- Name: cities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.cities_id_seq', 6, true);


--
-- Name: shops_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.shops_id_seq', 6, true);


--
-- Name: streets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.streets_id_seq', 4, true);


--
-- Name: cities cities_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_pkey PRIMARY KEY (id);


--
-- Name: shops shops_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_pkey PRIMARY KEY (id);


--
-- Name: streets streets_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.streets
    ADD CONSTRAINT streets_pkey PRIMARY KEY (id);


--
-- Name: shops shops_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.cities(id);


--
-- Name: shops shops_street_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_street_id_fkey FOREIGN KEY (street_id) REFERENCES public.streets(id);


--
-- Name: streets streets_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.streets
    ADD CONSTRAINT streets_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.cities(id);


--
-- PostgreSQL database dump complete
--

