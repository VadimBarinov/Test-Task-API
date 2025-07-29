CREATE ROLE mediasoft WITH LOGIN PASSWORD 'qwerty1234';

CREATE DATABASE mediasoft_shops OWNER mediasoft;

\c mediasoft_shops;

CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS streets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city_id INTEGER NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities (id)
);

CREATE TABLE IF NOT EXISTS shops (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city_id INTEGER NOT NULL,
    street_id INTEGER NOT NULL,
    house INTEGER NOT NULL,
    opening_time TIME NOT NULL,
    closing_time TIME NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities (id),
    FOREIGN KEY (street_id) REFERENCES streets (id)
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mediasoft;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO mediasoft;
