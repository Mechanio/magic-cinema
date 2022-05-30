![PyPI - Python Version](https://img.shields.io/pypi/pyversions/privat_exchange_rates?style=for-the-badge)

## Magic cinema
#### What that project can do?

The Cinema service provides opportunities to purchase tickets for a particular session, as well as search for available sessions by movie name, genre, actors, director, date and time of session. Also the ability to sort available sessions by date.

API is implemented in Flask, database - postgresql, front-end - ReactJS, documentation - Swagger.

Also Docker implementation

---
## How to install it?

#### - Python 3.10
#### - PIP dependencies
```bash
pip install -r requirements.txt
```
---
#### - React(NodeJS)

For Ubuntu 20.04

```bash
sudo apt install npm
```
---
#### - Docker (docker-compose)
```bash
sudo apt install docker docker-compose
```
---
## How to start it?

#### API with Swagger
```bash
python3 run.py
```
#### React (in front-end directory)
```bash
npm install
npm start
```
#### Docker
 
```bash
sudo docker-compose build
sudo docker-compose up
```
To stop containers
- Ctrl-C
- ```sudo docker-compose down```

To connect:
- API with Swagger: 0.0.0.0:5000
- React front-end: localhost:3000
---
#### Additional links for front-end (as admin)

- /auditoriums
- /users

#### Initial Data:

```commandline
actors:
{
  "firstname": "Emma",
  "lastname": "Stone"
}
{
  "firstname": "Ryan",
  "lastname": "Gosling"
}
{
  "firstname": "Bruce",
  "lastname": "Campbell"
}

auditorium
{
  "seats": 60
}
{
  "seats": 30
}

authentication:
{
  "firstname": "John",
  "lastname": "Doe",
  "email": "test@gmail.com",
  "password": "password",
  "is_admin": false
}
{
  "firstname": "Johan",
  "lastname": "Doe",
  "email": "test1@gmail.com",
  "password": "password",
  "is_admin": true
}

directors:
{
  "firstname": "Damien",
  "lastname": "Chazelle"
}
{
  "firstname": "Sam",
  "lastname": "Raimi"
}

genres:
{
  "genre": "drama"
}
{
  "genre": "musical"
}
{
  "genre": "comedy"
}
{
  "genre": "horror"
}
{
  "genre": "slasher"
}

movies:
{
  "name": "La La Land",
  "description": "It is about a struggling jazz pianist and an aspiring actress,respectively, who meet and fall in love.",
  "director_id": 1,
  "year": 2016,
  "month": 8,
  "day": 31,
  "genres": ["drama", "musical"],
  "actors": ["Ryan Gosling", "Emma Stone"]
}
{
  "name": "Evil Dead",
  "description": "It is about Necronomicon which ressurects demons.",
  "director_id": 2,
  "year": 1981,
  "month": 10,
  "day": 15,
  "genres": ["horror", "slasher"],
  "actors": ["Bruce Campbell"]
}

movie session:
{
  "movie_id": 1,
  "auditorium_id": 1,
  "year": 2022,
  "month": 5,
  "day": 15,
  "hour": 15,
  "minute": 30
}
{
  "movie_id": 1,
  "auditorium_id": 1,
  "year": 2022,
  "month": 5,
  "day": 16,
  "hour": 15,
  "minute": 30
}
{
  "movie_id": 1,
  "auditorium_id": 1,
  "year": 2022,
  "month": 5,
  "day": 17,
  "hour": 15,
  "minute": 30
}
{
  "movie_id": 2,
  "auditorium_id": 2,
  "year": 2022,
  "month": 5,
  "day": 17,
  "hour": 15,
  "minute": 30
}

tickets:
{
  "session_id": 1,
  "user_id": 1
}
{
  "session_id": 1,
  "user_id": 1
}
{
  "session_id": 1,
  "user_id": 1
}
{
  "session_id": 3,
  "user_id": 1
}
{
  "session_id": 4,
  "user_id": 1
}

```
