from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256

from app.database.database import base, session


class MoviesModel(base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(String(300), nullable=False)
    release_date = Column(DateTime())
    director_id = Column(Integer, ForeignKey('directors.id'))
    director = relationship("DirectorsModel", back_populates='movies')
    genres = relationship("MovieGenreModel", lazy='dynamic', cascade="all, delete-orphan",
                          foreign_keys="MovieGenreModel.movie_id")
    actors = relationship("CastModel", lazy='dynamic', cascade="all, delete-orphan",
                          foreign_keys="CastModel.movie_id")
    sessions = relationship("MovieSessionsModel", lazy='dynamic', cascade="all, delete-orphan",
                            foreign_keys="MovieSessionsModel.movie_id")

    @classmethod
    def find_by_id(cls, id, to_dict=True, without_sessions=False):
        """
        Find movie by id

        :param id: movie id
        :param to_dict: if True - returns dict representation of movie info, if False -
            returns model instance
        :param without_sessions: if True - returns dict representation of movie info without
            sessions, if False - with
        :return: dict representation of movie info or model instance
        """
        movie = session.query(cls).filter_by(id=id).first()
        if not movie:
            return {}
        if to_dict:
            return cls.to_dict(movie, without_sessions)
        else:
            return movie

    @classmethod
    def find_by_director_id(cls, director_id, offset, limit):
        """
        Find movie by director id

        :param director_id: director id
        :param offset: skip offset rows before beginning to return rows
        :param limit:  determines the number of rows returned by the query
        :return: list of dict representations of movie
        """
        movies = session.query(cls).filter_by(director_id=director_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie) for movie in movies]

    @classmethod
    def find_by_name(cls, name, to_dict=True):
        """
        Find movie by name

        :param name: name of movie
        :param to_dict: if True - returns dict representation of movie info, if False -
            returns model instance
        :return: dict representation of movie info or model instance
        """
        movie = session.query(cls).filter_by(name=name).order_by(cls.id).first()
        if not movie:
            return {}
        if to_dict:
            return cls.to_dict(movie)
        else:
            return movie

    @classmethod
    def return_all(cls, offset, limit):
        """
        Return all movies

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of movies
        """
        movies = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie) for movie in movies]

    @classmethod
    def delete_by_id(cls, id):
        """
        Delete movie by id

        :param id: movie id
        :return: code status (200, 404)
        """
        movie = session.query(cls).filter_by(id=id).first()
        if movie:
            session.delete(movie)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(movie, without_sessions=False):
        """
        Represent model instance (movie) information

        :param movie: model instance
        :param without_sessions: if True - returns dict representation of movie info without
            sessions, if False - with
        :return: dict representation of movie info
        """
        if without_sessions:
            return {
                "id": movie.id,
                "name": movie.name,
                "description": movie.description,
                "release_date": movie.release_date,
                "director": DirectorsModel.find_by_id(movie.director_id, without_movies=True),
                "actors": [ActorsModel.find_by_id(actor.actor_id, without_movies=True) for actor in movie.actors],
                "genres": [GenresModel.find_by_id(genre.genre_id, without_movies=True) for genre in movie.genres]
            }
        else:
            return {
               "id": movie.id,
               "name": movie.name,
               "description": movie.description,
               "release_date": movie.release_date,
               "director": DirectorsModel.find_by_id(movie.director_id, without_movies=True),
               "actors": [ActorsModel.find_by_id(actor.actor_id, without_movies=True) for actor in movie.actors],
               "genres": [GenresModel.find_by_id(genre.genre_id, without_movies=True) for genre in movie.genres],
               "sessions": [MovieSessionsModel.to_dict(movie_session, without_tickets=True) for movie_session in movie.sessions]
            }


class DirectorsModel(base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    movies = relationship(MoviesModel, lazy='dynamic', cascade="all, delete-orphan",
                          foreign_keys="MoviesModel.director_id")

    @classmethod
    def find_by_id(cls, id, to_dict=True, without_movies=False, without_sessions=False):
        """
        Find director by id

        :param id: director id
        :param to_dict: if True - returns dict representation of director info, if False -
            returns model instance
        :param without_movies: if True - returns dict representation of movie info without
            movies, if False - with
        :param without_sessions: if True - returns dict representation of movie info without
            sessions, if False - with
        :return: dict representation of director info or model instance
        """
        director = session.query(cls).filter_by(id=id).first()
        if not director:
            return {}
        if to_dict:
            return cls.to_dict(director, without_movies, without_sessions)
        else:
            return director

    @classmethod
    def find_by_name(cls, firstname, lastname, to_dict=True, without_sessions=False):
        """
        Find director by name

        :param firstname: director's firstname
        :param lastname: director's lastname
        :param to_dict: if True - returns dict representation of director info, if False -
            returns model instance
        :param without_sessions: if True - returns dict representation of movie info without
            sessions, if False - with
        :return: dict representation of director info or model instance
        """
        director = session.query(cls).filter_by(firstname=firstname, lastname=lastname)\
            .order_by(cls.id).first()
        if not director:
            return {}
        if to_dict:
            return cls.to_dict(director, without_sessions=without_sessions)
        else:
            return director

    @classmethod
    def return_all(cls, offset, limit, without_sessions=False):
        """
        Return all directors

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :param without_sessions: if True - returns dict representation of movie info without
            sessions, if False - with
        :return: list of dict representations of movies
        """
        directors = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(director, without_sessions=without_sessions) for director in directors]

    @classmethod
    def delete_by_id(cls, id):
        """
        Delete director by id

        :param id: director id
        :return: code status (200, 404)
        """
        director = session.query(cls).filter_by(id=id).first()
        if director:
            session.delete(director)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(director, without_movies=False, without_sessions=False):
        """
        Represent model instance (director) information

        :param director: model instance
        :param without_movies: if True - returns dict representation of movie info without
            movies, if False - with
        :param without_sessions: if True - returns dict representation of movie info without
            sessions, if False - with
        :return: dict representation of director info
        """
        if without_movies:
            return {
                "id": director.id,
                "firstname": director.firstname,
                "lastname": director.lastname,
            }
        else:
            return {
                "id": director.id,
                "firstname": director.firstname,
                "lastname": director.lastname,
                "movies": [MoviesModel.to_dict(movie, without_sessions) for movie in director.movies]
            }


class ActorsModel(base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    movies = relationship("CastModel", lazy='dynamic', cascade="all, delete-orphan",
                          foreign_keys="CastModel.actor_id")

    @classmethod
    def find_by_id(cls, id, to_dict=True, without_movies=False, without_sessions=False):
        """
        Find actor by id

        :param id: actor id
        :param to_dict: if True - returns dict representation of actor info, if False -
            returns model instance
        :param without_movies: if True - returns dict representation of actor info without
            movies, if False - with
        :param without_sessions: if True - returns dict representation of actor info without
            sessions, if False - with
        :return: dict representation of actor info or model instance
        """
        actor = session.query(cls).filter_by(id=id).first()
        if not actor:
            return {}
        if to_dict:
            return cls.to_dict(actor, without_movies, without_sessions)
        else:
            return actor

    @classmethod
    def find_by_name(cls, firstname, lastname, to_dict=True, without_sessions=False):
        """
        Find actor by name

        :param firstname: actor's firstname
        :param lastname: actor's lastname
        :param to_dict: if True - returns dict representation of actor info, if False -
            returns model instance
        :param without_sessions: if True - returns dict representation of actor info without
            sessions, if False - with
        :return: dict representation of actor info or model instance
        """
        actor = session.query(cls).filter_by(firstname=firstname, lastname=lastname) \
            .order_by(cls.id).first()
        if not actor:
            return {}
        if to_dict:
            return cls.to_dict(actor, without_sessions=without_sessions)
        else:
            return actor

    @classmethod
    def return_all(cls, offset, limit, without_sessions=False):
        """
        Return all actors

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :param without_sessions: if True - returns dict representation of actor info without
            sessions, if False - with
        :return: list of dict representations of actors
        """
        actors = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(actor, without_sessions=without_sessions) for actor in actors]

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        """
        Delete actor by id

        :param id: actor id
        :return: code status (200, 404)
        """
        actor = session.query(cls).filter_by(id=id).first()
        if actor:
            session.delete(actor)
            session.commit()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(actor, without_movies=False, without_sessions=False):
        """
        Represent model instance (actor) information

        :param actor: model instance
        :param without_movies: if True - returns dict representation of actor info without
            movies, if False - with
        :param without_sessions: if True - returns dict representation of actor info without
            sessions, if False - with
        :return: dict representation of actor info
        """
        if without_movies:
            return {
                "id": actor.id,
                "firstname": actor.firstname,
                "lastname": actor.lastname,
            }
        else:
            return {
                "id": actor.id,
                "firstname": actor.firstname,
                "lastname": actor.lastname,
                "movies": [MoviesModel.find_by_id(movie.movie_id, without_sessions=without_sessions) for movie in actor.movies]
            }


class CastModel(base):
    __tablename__ = "cast"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship("MoviesModel", back_populates='actors')
    actor_id = Column(Integer, ForeignKey('actors.id'))
    actor = relationship("ActorsModel", back_populates='movies')

    @classmethod
    def find_by_ids(cls, movie_id, actor_id):
        """
        Find row by movie and actor ids

        :param movie_id: movie id
        :param actor_id: actor id
        :return: model instance
        """
        searched_row = session.query(cls).filter_by(movie_id=movie_id, actor_id=actor_id).first()
        if not searched_row:
            return {}
        else:
            return searched_row

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @classmethod
    def delete(cls, row):
        """
        Delete row

        :param row: row
        :return: code status (200, 404)
        """
        if row:
            session.delete(row)
            session.commit()
            return 200
        else:
            return 404


class GenresModel(base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    genre = Column(String(60), nullable=False, unique=True)
    movies = relationship("MovieGenreModel", lazy='dynamic', cascade="all, delete-orphan",
                          foreign_keys="MovieGenreModel.genre_id")

    @classmethod
    def find_by_id(cls, id, to_dict=True, without_movies=False, without_sessions=False):
        """
        Find genre by id

        :param id: genre id
        :param to_dict: if True - returns dict representation of genre info, if False -
            returns model instance
        :param without_movies: if True - returns dict representation of genre info without
            movies, if False - with
        :param without_sessions: if True - returns dict representation of genre info without
            sessions, if False - with
        :return: dict representation of genre info or model instance
        """
        genre = session.query(cls).filter_by(id=id).first()
        if not genre:
            return {}
        if to_dict:
            return cls.to_dict(genre, without_movies, without_sessions)
        else:
            return genre

    @classmethod
    def find_by_genre(cls, genre, to_dict=True, without_sessions=False):
        """
        Find genre by genre name

        :param genre: genre name
        :param to_dict: if True - returns dict representation of genre info, if False -
            returns model instance
        :param without_sessions: if True - returns dict representation of genre info without
            sessions, if False - with
        :return: dict representation of genre info or model instance
        """
        genre = session.query(cls).filter_by(genre=genre).order_by(cls.id).first()
        if not genre:
            return {}
        if to_dict:
            return cls.to_dict(genre, without_sessions)
        else:
            return genre

    @classmethod
    def return_all(cls, offset, limit, without_sessions=False):
        """
        Return all genres

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :param without_sessions: if True - returns dict representation of genre info without
            sessions, if False - with
        :return: list of dict representations of genres
        """
        genres = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(genre, without_sessions=without_sessions) for genre in genres]

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        """
        Delete genre by id

        :param id: genre id
        :return: code status (200, 404)
        """
        genre = session.query(cls).filter_by(id=id).first()
        if genre:
            session.delete(genre)
            session.commit()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(genre, without_movies=False, without_sessions=False):
        """
        Represent model instance (genre) information

        :param genre: model instance
        :param without_movies: if True - returns dict representation of genre info without
            movies, if False - with
        :param without_sessions: if True - returns dict representation of genre info without
            sessions, if False - with
        :return: dict representation of genre info
        """
        if without_movies:
            return {
                "id": genre.id,
                "genre": genre.genre
            }
        else:
            return {
                "id": genre.id,
                "genre": genre.genre,
                "movies": [MoviesModel.find_by_id(movie.movie_id, without_sessions=without_sessions) for movie in genre.movies]
            }


class MovieGenreModel(base):
    __tablename__ = "moviegenre"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship("MoviesModel", back_populates='genres')
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship("GenresModel", back_populates='movies')

    @classmethod
    def find_by_ids(cls, movie_id, genre_id):
        """
        Find row by movie and genre ids

        :param movie_id: movie id
        :param genre_id: genre id
        :return: model instance
        """
        searched_row = session.query(cls).filter_by(movie_id=movie_id, genre_id=genre_id).first()
        if not searched_row:
            return {}
        else:
            return searched_row

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @classmethod
    def delete(cls, row):
        """
        Delete row

        :param row: row
        :return: code status (200, 404)
        """
        if row:
            session.delete(row)
            session.commit()
            return 200
        else:
            return 404


class AuditoriumModel(base):
    __tablename__ = "auditorium"
    id = Column(Integer, primary_key=True)
    seats = Column(Integer, nullable=False)
    movie_sessions = relationship("MovieSessionsModel", lazy='dynamic', cascade="all, delete-orphan",
                                  foreign_keys="MovieSessionsModel.auditorium_id")

    @classmethod
    def find_by_id(cls, id, to_dict=True, without_sessions=False):
        """
        Find auditorium by id

        :param id: auditorium id
        :param to_dict: if True - returns dict representation of auditorium info, if False -
            returns model instance
        :param without_sessions: if True - returns dict representation of auditorium info without
            sessions, if False - with
        :return: dict representation of auditorium info or model instance
        """
        audit = session.query(cls).filter_by(id=id).first()
        if not audit:
            return {}
        if to_dict:
            return cls.to_dict(audit, without_sessions)
        else:
            return audit

    @classmethod
    def return_all(cls, offset, limit):
        """
        Return all auditoriums

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of auditoriums
        """
        auditoriums = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(audit) for audit in auditoriums]

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        """
        Delete auditorium by id

        :param id: auditorium id
        :return: code status (200, 404)
        """
        audit = session.query(cls).filter_by(id=id).first()
        if audit:
            session.delete(audit)
            session.commit()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(audit, without_sessions=False):
        """
        Represent model instance (auditorium) information

        :param audit: model instance
        :param without_sessions: if True - returns dict representation of movie info without
            sessions, if False - with
        :return: dict representation of auditorium info
        """
        if without_sessions:
            return {
                "id": audit.id,
                "seats": audit.seats
            }
        else:
            return {
                "id": audit.id,
                "seats": audit.seats,
                "movie_sessions": [MovieSessionsModel.to_dict(movie_session) for movie_session in audit.movie_sessions]
            }


class MovieSessionsModel(base):
    __tablename__ = "moviesessions"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship("MoviesModel", back_populates='sessions')
    auditorium_id = Column(Integer, ForeignKey('auditorium.id'))
    auditorium = relationship("AuditoriumModel", back_populates='movie_sessions')
    date = Column(DateTime())
    tickets = relationship("TicketsModel", lazy='dynamic', cascade="all, delete-orphan",
                           foreign_keys="TicketsModel.session_id")
    remain_seats = Column(Integer, nullable=False)
    is_active = Column(Boolean(), nullable=False)

    @classmethod
    def find_by_id(cls, id, to_dict=True):
        """
        Find movie session by id

        :param id: movie session id
        :param to_dict: if True - returns dict representation of movie session info, if False -
            returns model instance
        :return: dict representation of movie session info or model instance
        """
        movie_session = session.query(cls).filter_by(id=id).first()
        if not movie_session:
            return {}
        if to_dict:
            return cls.to_dict(movie_session)
        else:
            return movie_session

    @classmethod
    def find_by_dates(cls, left_date, right_date, offset, limit):
        """
        Find movie session by dates

        :param left_date: left side of date range
        :param right_date: right side of date range
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of movies sessions
        """
        movie_sessions = session.query(cls).filter(cls.date <= right_date, cls.date >= left_date) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie_session) for movie_session in movie_sessions]

    @classmethod
    def find_by_movie_id(cls, movie_id, offset, limit):
        """
        Find movie session by movie id

        :param movie_id: movie id
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of movies sessions
        """
        movie_sessions = session.query(cls).filter_by(movie_id=movie_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie_session) for movie_session in movie_sessions]

    @classmethod
    def find_by_auditorium_id(cls, auditorium_id, offset, limit):
        """
        Find actual movie session by auditorium id

        :param auditorium_id: auditorium id
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of movies sessions
        """
        movie_sessions = session.query(cls).filter_by(auditorium_id=auditorium_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie_session) for movie_session in movie_sessions if movie_session.is_active]

    @classmethod
    def return_all(cls, offset, limit, without_tickets=False):
        """
        Return all actual movies sessions

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :param without_tickets: if True - returns dict representation of movie session info without
            tickets, if False - with
        :return: list of dict representations of movies sessions
        """
        movie_sessions = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie_session, without_tickets=without_tickets) for movie_session in movie_sessions
                if movie_session.is_active]

    @classmethod
    def return_all_inactive(cls, offset, limit):
        """
        Return all inactive movie seanses

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of users
        """
        movie_sessions = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie_session) for movie_session in movie_sessions if not movie_session.is_active]

    @classmethod
    def delete_by_id(cls, id):
        """
        Delete movie session by id and all tickets

        :param id: movie session  id
        :return: code status (200, 404)
        """
        movie_session = session.query(cls).filter_by(id=id).first()
        if movie_session:
            movie_session.is_active = False
            movie_session.save_to_db()
            for ticket in movie_session.tickets:
                TicketsModel.delete_by_id(ticket.id)
            return 200
        else:
            return 404

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(movie_session, without_tickets=False):
        """
        Represent model instance (movie session) information

        :param movie_session: model instance
        :param without_tickets: if True - returns dict representation of movie session info without
            tickets, if False - with
        :return: dict representation of movie session info
        """
        if without_tickets:
            return {
                "id": movie_session.id,
                "date": movie_session.date,
                "movie_id": movie_session.movie_id,
                "movie": MoviesModel.find_by_id(movie_session.movie_id, without_sessions=True),
                "remain_seats": movie_session.remain_seats,
                "is_active": movie_session.is_active,
                "auditorium": AuditoriumModel.find_by_id(movie_session.auditorium_id, without_sessions=True),
            }
        else:
            return {
                "id": movie_session.id,
                "date": movie_session.date,
                "movie_id": movie_session.movie_id,
                "movie": MoviesModel.find_by_id(movie_session.movie_id, without_sessions=True),
                "remain_seats": movie_session.remain_seats,
                "is_active": movie_session.is_active,
                "auditorium": AuditoriumModel.find_by_id(movie_session.auditorium_id, without_sessions=True),
                "tickets": [TicketsModel.to_dict(ticket) for ticket in movie_session.tickets]
            }


class UserModel(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_admin = Column(Boolean(), default=False)
    is_active = Column(Boolean(), nullable=False)
    tickets = relationship("TicketsModel", lazy='dynamic', cascade="all, delete-orphan",
                           foreign_keys="TicketsModel.user_id")

    @classmethod
    def find_by_id(cls, id, to_dict=True):
        """
        Find active user by id

        :param id: user id
        :param to_dict: if True - returns dict representation of user info, if False -
            returns model instance
        :return: dict representation of user info or model instance
        """
        user = session.query(cls).filter_by(id=id).first()
        if not user:
            return {}
        if user.is_active:
            if to_dict:
                return cls.to_dict(user)
            else:
                return user
        else:
            return {}

    @classmethod
    def find_by_name(cls, firstname, lastname, to_dict=True):
        """
        Find active user by name

        :param firstname: user firstname
        :param lastname: user lastname
        :param to_dict: if True - returns dict representation of user info, if False -
            returns model instance
        :return: dict representation of user info or model instance
        """
        user = session.query(cls).filter_by(firstname=firstname, lastname=lastname) \
            .order_by(cls.id).first()
        if not user:
            return {}
        if user.is_active:
            if to_dict:
                return cls.to_dict(user)
            else:
                return user
        else:
            return {}

    @classmethod
    def find_by_email(cls, email, to_dict=True):
        """
        Find active user by email

        :param email: user email
        :param to_dict: if True - returns dict representation of user info, if False -
            returns model instance
        :return: dict representation of user info or model instance
        """
        user = session.query(cls).filter_by(email=email).first()
        if not user:
            return {}
        if user.is_active:
            if to_dict:
                return cls.to_dict(user)
            else:
                return user
        else:
            return {}

    @classmethod
    def return_all(cls, offset, limit):
        """
        Return all active users

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of users
        """
        users = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(user) for user in users if user.is_active]

    @classmethod
    def return_all_inactive(cls, offset, limit):
        """
        Return all inactive users

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of users
        """
        users = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(user) for user in users if not user.is_active]

    @classmethod
    def delete_by_id(cls, id):
        """
        Delete user by id

        :param id: user id
        :return: code status (200, 404)
        """
        user = session.query(cls).filter_by(id=id).first()
        if user:
            user.is_active = False
            user.save_to_db()
            return 200
        else:
            return 404

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(user):
        """
        Represent model instance (user) information

        :param user: model instance
        :return: dict representation of user info
        """
        return {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "tickets": [TicketsModel.to_dict(ticket) for ticket in user.tickets]
        }

    @staticmethod
    def generate_hash(password):
        """
        Generate hashed password

        :param password: password to hash
        :return: hashed password
        """
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hashed):
        """
        Verify hashed password with imputed one

        :param password: imputed password
        :param hashed: hashed password
        :return: True or False
        """
        return sha256.verify(password, hashed)


class TicketsModel(base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('moviesessions.id'))
    session = relationship("MovieSessionsModel", back_populates='tickets')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserModel", back_populates='tickets')
    is_active = Column(Boolean(), default=False)

    @classmethod
    def find_by_id(cls, id, to_dict=True):
        """
        Find active ticket by id

        :param id: ticket id
        :param to_dict: if True - returns dict representation of ticket info, if False -
            returns model instance
        :return: dict representation of ticket info or model instance
        """
        ticket = session.query(cls).filter_by(id=id).first()
        if not ticket:
            return {}
        if ticket.is_active:
            if to_dict:
                return cls.to_dict(ticket)
            else:
                return ticket
        else:
            return {}

    @classmethod
    def find_by_session_id(cls, session_id, offset, limit):
        """
        Find active tickets by session id

        :param session_id: session id
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of tickets
        """
        tickets = session.query(cls).filter_by(session_id=session_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(ticket) for ticket in tickets if ticket.is_active]

    @classmethod
    def find_by_user_id(cls, user_id, offset, limit):
        """
        Find active tickets by user id

        :param user_id: user id
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of tickets
        """
        tickets = session.query(cls).filter_by(user_id=user_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(ticket) for ticket in tickets if ticket.is_active]

    @classmethod
    def return_all(cls, offset, limit):
        """
        Return all tickets

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of tickets
        """
        tickets = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(ticket) for ticket in tickets if ticket.is_active]

    @classmethod
    def find_by_session_id_inactive(cls, session_id, offset, limit):
        """
        Find inactive tickets by session id

        :param session_id: session id
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of tickets
        """
        tickets = session.query(cls).filter_by(session_id=session_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(ticket) for ticket in tickets if not ticket.is_active]

    @classmethod
    def find_by_user_id_inactive(cls, user_id, offset, limit):
        """
        Find inactive tickets by user id

        :param user_id: user id
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of tickets
        """
        tickets = session.query(cls).filter_by(user_id=user_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(ticket) for ticket in tickets if not ticket.is_active]

    @classmethod
    def return_all_inactive(cls, offset, limit):
        """
        Return all inactive tickets

        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of tickets
        """
        tickets = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(ticket) for ticket in tickets if not ticket.is_active]

    @classmethod
    def delete_by_id(cls, id):
        """
        Delete ticket by id

        :param id: ticket id
        :return: code status (200, 404)
        """
        ticket = session.query(cls).filter_by(id=id).first()
        if ticket:
            ticket.is_active = False
            ticket.save_to_db()

            return 200
        else:
            return 404

    def save_to_db(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(ticket):
        """
        Represent model instance (ticket) information

        :param ticket: model instance
        :return: dict representation of ticket info
        """
        return {
            "id": ticket.id,
            "session_id": ticket.session_id,
            "user_id": ticket.user_id,
            "is_active": ticket.is_active,
        }


class RevokedTokenModel(base):
    __tablename__ = 'revoked_tokens'
    id_ = Column(Integer, primary_key=True)
    jti = Column(String(120))
    blacklisted_on = Column(DateTime, default=datetime.utcnow)

    def add(self):
        """
        Save model instance to database

        :return: None
        """
        session.add(self)
        session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """
        Check if jwt token is blocklisted

        :param jti: signature
        :return: True or False
        """
        query = session.query(cls).filter_by(jti=jti).first()
        return bool(query)
