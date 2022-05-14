from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

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

    @classmethod
    def find_by_id(cls, id, to_dict=True):
        movie = session.query(cls).filter_by(id=id).first()
        if not movie:
            return {}
        if to_dict:
            return cls.to_dict(movie)
        else:
            return movie

    # TODO offset limit
    @classmethod
    def find_by_director_id(cls, director_id, offset, limit):
        movies = session.query(cls).filter_by(director_id=director_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(movie) for movie in movies]

    # TODO offset limit
    @classmethod
    def find_by_name(cls, name, to_dict=True):
        movie = session.query(cls).filter_by(name=name).order_by(cls.id).first()
        if not movie:
            return {}
        if to_dict:
            return cls.to_dict(movie)
        else:
            return movie

    # TODO offset limit
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
    def to_dict(movie):
        return {
           "id": movie.id,
           "name": movie.name,
           "description": movie.description,
           "release_date": movie.release_date,
           "director": DirectorsModel.find_by_id(movie.director_id, without_movies=True),
           "actors": [ActorsModel.find_by_id(actor.actor_id, without_movies=True) for actor in movie.actors],
           "genres": [GenresModel.find_by_id(genre.genre_id, without_movies=True) for genre in movie.genres]
        }


class DirectorsModel(base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    movies = relationship(MoviesModel, lazy='dynamic', cascade="all, delete-orphan",
                          foreign_keys="MoviesModel.director_id")

    @classmethod
    def find_by_id(cls, id, to_dict=True, without_movies=False):
        director = session.query(cls).filter_by(id=id).first()
        if not director:
            return {}
        if to_dict:
            return cls.to_dict(director, without_movies)
        else:
            return director

    @classmethod
    def find_by_name(cls, firstname, lastname, to_dict=True):
        director = session.query(cls).filter_by(firstname=firstname, lastname=lastname)\
            .order_by(cls.id).first()
        if not director:
            return {}
        if to_dict:
            return cls.to_dict(director)
        else:
            return director

    @classmethod
    def return_all(cls, offset, limit):
        directors = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(director) for director in directors]

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
    def to_dict(director, without_movies=False):
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
                "movies": [MoviesModel.to_dict(movie) for movie in director.movies]
            }


class ActorsModel(base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    movies = relationship("CastModel", lazy='dynamic', cascade="all, delete-orphan",
                          foreign_keys="CastModel.actor_id")

    @classmethod
    def find_by_id(cls, id, to_dict=True, without_movies=False):
        actor = session.query(cls).filter_by(id=id).first()
        if not actor:
            return {}
        if to_dict:
            return cls.to_dict(actor, without_movies)
        else:
            return actor

    @classmethod
    def find_by_name(cls, firstname, lastname, to_dict=True):
        actor = session.query(cls).filter_by(firstname=firstname, lastname=lastname) \
            .order_by(cls.id).first()
        if not actor:
            return {}
        if to_dict:
            return cls.to_dict(actor)
        else:
            return actor

    @classmethod
    def return_all(cls, offset, limit):
        actors = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(actor) for actor in actors]

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
    def to_dict(actor, without_movies=False):
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
                "movies": [MoviesModel.find_by_id(movie.movie_id) for movie in actor.movies]
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
    genre = Column(String(60), nullable=False)
    movies = relationship("MovieGenreModel", lazy='dynamic', cascade="all, delete-orphan",
                          foreign_keys="MovieGenreModel.genre_id")

    @classmethod
    def find_by_id(cls, id, to_dict=True, without_movies=False):
        genre = session.query(cls).filter_by(id=id).first()
        if not genre:
            return {}
        if to_dict:
            return cls.to_dict(genre, without_movies)
        else:
            return genre

    @classmethod
    def find_by_genre(cls, genre, to_dict=True):
        genre = session.query(cls).filter_by(genre=genre).order_by(cls.id).first()
        if not genre:
            return {}
        if to_dict:
            return cls.to_dict(genre)
        else:
            return genre

    @classmethod
    def return_all(cls, offset, limit):
        genres = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(genre) for genre in genres]

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
    def to_dict(genre, without_movies=False):
        if without_movies:
            return {
                "id": genre.id,
                "genre": genre.genre
            }
        else:
            return {
                "id": genre.id,
                "genre": genre.genre,
                "movies": [MoviesModel.find_by_id(movie.movie_id) for movie in genre.movies]
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
