# Тестовое задание REST API

## Опиание проекта

- Сервис для сохранения и получения информации о городах, улицах и магазинах
- Реализован с использованием _FastAPI_ и _SQLAlchemy_
- База данных _PostgreSQL_
- Сервис запускается с помощью _docker-compose_

---

## Функционал

В случае успешной обработки сервис отвечает статусом 200, в случае любой ошибки - статус 400.

#### /city/ (GET) Получение всех городов

##### Args

    db: Сессия базы данных

##### Returns:

    Список всех городов

##### Example:

Request URL:

```bash
    curl -X 'GET' \
    'http://127.0.0.1:8080/city/' \
    -H 'accept: application/json'
```

Response body:

```json
    {
        "id": 1,
        "name": "Ульяновск"
    },
    {
        "id": 2,
        "name": "Москва"
    },
    {
        "id": 3,
        "name": "Волгоград"
    },
    {
        "id": 4,
        "name": "Пермь"
    }
```

#### /city/ (POST) Создание города

##### Args

    city:
        id: int
        name: str

    db: Сессия базы данных

##### Returns:

    ID созданного города

##### Example:

Request:

```bash
    curl -X 'POST' \
    'http://127.0.0.1:8080/city/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "id": 0,
    "name": "Пермь"
    }'
```

Response body:

```
    ID of the created object: 4
```

#### /city//street (GET) Получение всех улиц города

##### Args

    city_id: int

    db: Сессия базы данных

##### Returns:

    Список всех улиц города

##### Example:

Request URL:

```bash
    curl -X 'GET' \
    'http://127.0.0.1:8080/city//street/?city_id=1' \
    -H 'accept: application/json'
```

Response body:

```json
    {
        "id": 1,
        "name": "Ленина",
        "city": "Ульяновск"
    },
    {
        "id": 2,
        "name": "Октябрьская",
        "city": "Ульяновск"
    }
```

#### /city//street (POST) Создание улицы в указанном города

##### Args

    street:
        id: int
        name: str
        city_id: int

    db: Сессия базы данных

##### Returns:

    ID созданной улицы

##### Example:

Request URL:

```bash
    curl -X 'POST' \
    'http://127.0.0.1:8080/city//street/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "id": 0,
    "name": "Кирова",
    "city_id": 1
    }'
```

Response body:

```
    ID of the created object: 3
```

#### /shop (GET) Получение списка магазинов

Метод принимает параметры для фильтрации. Параметры не обязательны. В случае отсутствия параметров выводятся все магазины, если хоть один параметр есть, то по нему выполняется фильтрация.

##### Args

    street_id: int
    city_id: int
    is_open: int (0 - закрыт, 1 - открыт)
    (Данный статус определяется исходя из параметров
    «Время открытия», «Время закрытия» и текущего
    времени сервера)

    db: Сессия базы данных

##### Returns:

    Список магазинов удовлетворяющих параметрам

##### Example 1:

Request URL:

```bash
    curl -X 'GET' \
    'http://127.0.0.1:8080/shop/' \
    -H 'accept: application/json'
```

Response body:

```json
    {
        "id": 1,
        "name": "Магнит",
        "city": "Ульяновск",
        "street": "Ленина",
        "house": 14,
        "opening_time": "08:00:00",
        "closing_time": "22:00:00"
    },
    {
        "id": 2,
        "name": "Спортмастер",
        "city": "Москва",
        "street": "Рябикова",
        "house": 14,
        "opening_time": "08:00:00",
        "closing_time": "22:00:00"
    }
```

##### Example 2:

Request URL:

```bash
    curl -X 'GET' \
    'http://127.0.0.1:8080/shop/?street_id=1&city_id=1&is_open=1' \
    -H 'accept: application/json'
```

Response body:

```json
    {
        "id": 1,
        "name": "Магнит",
        "city": "Ульяновск",
        "street": "Ленина",
        "house": 14,
        "opening_time": "08:00:00",
        "closing_time": "22:00:00"
    },
```

#### /shop (POST) Создание магазина

##### Args

    shop:
        id: int
        name: str
        city_id: int
        street_id: int
        house: int
        opening_time: str (00:00:00)
        closing_time: str (23:59:59)

    db: Сессия базы данных

##### Returns:

    ID созданного магазина

##### Example:

Request URL:

```bash
    curl -X 'POST' \
    'http://127.0.0.1:8080/shop/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "id": 0,
    "name": "Спортмастер",
    "city_id": 2,
    "street_id": 4,
    "house": 14,
    "opening_time": "8:00:00",
    "closing_time": "22:00:00"
    }'
```

Response body:

```
    ID of the created object: 2
```

---

## Запуск проекта

#### Для успешной работы проекта необходимо выполнить следующие шаги:

1. Установить _Docker_ на свой компьютер, если он еще не установлен: [_Get Started with Docker_](https://www.docker.com/get-started)

2. Склонировать данный репозиторий

```bash
    git clone https://github.com/VadimBarinov/Test-Task-API.git
```

3. Перейти в директорию с проектом

```bash
    cd Test-Task-API
```

4. Запустить приложение

```bash
   docker-compose up
```

#### После запуска приложения будут созданы необходимые таблицы:

```bash
    ./db/init_script.sql
```

#### Для доступа к базе данных используются следующие параметры:

- Database : mediasoft_shops
- User : postgres
- Password : qwerty1234
- Host : db
- Port : 5432

---

## Подключение к проекту

После выполнения подготовительных действий проект будет доступен по адресу

```bash
    http://localhost:8080/
```

Проект также будет доступен по внутреннему _ip_ адресу вашего компьютера

---

## Swagger UI

Swagger UI будет доступен по адресу:

```bash
    http://localhost:8080/docs
```

Также доступ будет по внутреннему _ip_ адресу

![](github_images/Swagger_UI.png)

---
