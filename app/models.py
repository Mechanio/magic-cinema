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
        movie = session.query(cls).filter_by(id=id).first()
        if not movie:
            return {}
        if to_dict:
            return cls.to_dict(movie, without_sessions)
        else:
            return movie

    @classmethod
    def find_by_director_id(cls, director_id, offset, limit):
        movies = session.query(cls).filter_by(director_id=director_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie) for movie in movies]

    @classmethod
    def find_by_name(cls, name, to_dict=True):
        movie = session.query(cls).filter_by(name=name).order_by(cls.id).first()
        if not movie:
            return {}
        if to_dict:
            return cls.to_dict(movie)
        else:
            return movie

    @classmethod
    def return_all(cls, offset, limit):
        movies = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie) for movie in movies]

    @classmethod
    def delete_by_id(cls, id):
        movie = session.query(cls).filter_by(id=id).first()
        if movie:
            session.delete(movie)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(movie, without_sessions=False):
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
        director = session.query(cls).filter_by(id=id).first()
        if not director:
            return {}
        if to_dict:
            return cls.to_dict(director, without_movies, without_sessions)
        else:
            return director

    @classmethod
    def find_by_name(cls, firstname, lastname, to_dict=True, without_sessions=False):
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
        directors = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(director, without_sessions=without_sessions) for director in directors]

    @classmethod
    def delete_by_id(cls, id):
        director = session.query(cls).filter_by(id=id).first()
        if director:
            session.delete(director)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(director, without_movies=False, without_sessions=False):
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
        actor = session.query(cls).filter_by(id=id).first()
        if not actor:
            return {}
        if to_dict:
            return cls.to_dict(actor, without_movies, without_sessions)
        else:
            return actor

    @classmethod
    def find_by_name(cls, firstname, lastname, to_dict=True, without_sessions=False):
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
        actors = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(actor, without_sessions=without_sessions) for actor in actors]

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        actor = session.query(cls).filter_by(id=id).first()
        if actor:
            session.delete(actor)
            session.commit()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(actor, without_movies=False, without_sessions=False):
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
        searched_row = session.query(cls).filter_by(movie_id=movie_id, actor_id=actor_id).first()
        if not searched_row:
            return {}
        else:
            return searched_row

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def delete(cls, row):
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
        genre = session.query(cls).filter_by(id=id).first()
        if not genre:
            return {}
        if to_dict:
            return cls.to_dict(genre, without_movies, without_sessions)
        else:
            return genre

    @classmethod
    def find_by_genre(cls, genre, to_dict=True, without_sessions=False):
        genre = session.query(cls).filter_by(genre=genre).order_by(cls.id).first()
        if not genre:
            return {}
        if to_dict:
            return cls.to_dict(genre, without_sessions)
        else:
            return genre

    @classmethod
    def return_all(cls, offset, limit, without_sessions=False):
        genres = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(genre, without_sessions=without_sessions) for genre in genres]

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        genre = session.query(cls).filter_by(id=id).first()
        if genre:
            session.delete(genre)
            session.commit()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(genre, without_movies=False, without_sessions=False):
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
        searched_row = session.query(cls).filter_by(movie_id=movie_id, genre_id=genre_id).first()
        if not searched_row:
            return {}
        else:
            return searched_row

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def delete(cls, row):
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
        audit = session.query(cls).filter_by(id=id).first()
        if not audit:
            return {}
        if to_dict:
            return cls.to_dict(audit, without_sessions)
        else:
            return audit

    @classmethod
    def return_all(cls, offset, limit):
        auditoriums = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(audit) for audit in auditoriums]

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        audit = session.query(cls).filter_by(id=id).first()
        if audit:
            session.delete(audit)
            session.commit()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(audit, without_sessions=False):
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
        movie_session = session.query(cls).filter_by(id=id).first()
        if not movie_session:
            return {}
        if to_dict:
            return cls.to_dict(movie_session)
        else:
            return movie_session

    @classmethod
    def find_by_dates(cls, left_date, right_date, offset, limit):
        movie_sessions = session.query(cls).filter(cls.date <= right_date, cls.date >= left_date) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie_session) for movie_session in movie_sessions]

    @classmethod
    def find_by_movie_id(cls, movie_id, offset, limit):
        movie_sessions = session.query(cls).filter_by(movie_id=movie_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie_session) for movie_session in movie_sessions]

    @classmethod
    def find_by_auditorium_id(cls, auditorium_id, offset, limit):
        movie_sessions = session.query(cls).filter_by(auditorium_id=auditorium_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie_session) for movie_session in movie_sessions if movie_session.is_active]

    @classmethod
    def return_all(cls, offset, limit, without_tickets=False):
        movie_sessions = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie_session, without_tickets=without_tickets) for movie_session in movie_sessions
                if movie_session.is_active]

    @classmethod
    def delete_by_id(cls, id):
        movie_session = session.query(cls).filter_by(id=id).first()
        if movie_session:
            movie_session.is_active = False
            movie_session.save_to_db()
            for ticket in movie_session.tickets:
                TicketsModel.delete_by_id(ticket)
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(movie_session, without_tickets=False):
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
        users = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(user) for user in users if user.is_active]

    @classmethod
    def delete_by_id(cls, id):
        user = session.query(cls).filter_by(id=id).first()
        if user:
            user.is_active = False
            user.save_to_db()
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(user):
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
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


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
        ticket = session.query(cls).filter_by(id=id).first()
        if not ticket:
            return {}
        if to_dict:
            return cls.to_dict(ticket)
        else:
            return ticket

    @classmethod
    def find_by_session_id(cls, session_id, offset, limit):
        tickets = session.query(cls).filter_by(session_id=session_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(ticket) for ticket in tickets]

    @classmethod
    def find_by_user_id(cls, user_id, offset, limit):
        tickets = session.query(cls).filter_by(user_id=user_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(ticket) for ticket in tickets]

    @classmethod
    def return_all(cls, offset, limit):
        tickets = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(ticket) for ticket in tickets]

    @classmethod
    def delete_by_id(cls, id):
        ticket = session.query(cls).filter_by(id=id).first()
        if ticket:
            ticket.is_active = False
            ticket.save_to_db()

            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(ticket):
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
        session.add(self)
        session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = session.query(cls).filter_by(jti=jti).first()
        return bool(query)
