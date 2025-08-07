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
    house VARCHAR(255) NOT NULL,
    opening_time TIME NOT NULL,
    closing_time TIME NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities (id),
    FOREIGN KEY (street_id) REFERENCES streets (id)
);

INSERT INTO cities (name)
VALUES
    ('Ульяновск'),
    ('Москва'),
    ('Казань'),
    ('Пермь'),
    ('Волгоград');

INSERT INTO streets (name, city_id)
VALUES
    ('Кирова', 1),
    ('Соборная', 2),
    ('Рябикова', 1),
    ('Набережная', 1);

INSERT INTO shops (name, city_id, street_id, house, opening_time, closing_time)
VALUES
    ('Продукты', 1, 1, '22б', '10:00:00', '22:00:00'),
    ('Электроника',	1, 3, '10а', '08:00:00', '21:00:00'),
    ('Продукты', 2, 2, '13', '08:00:00', '22:00:00');