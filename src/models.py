from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    date_subscribed: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    # Relaciones
    posts = relationship("Post", back_populates="author")
    favorite_planets = relationship("FavoritePlanet", back_populates="user")
    favorite_characters = relationship(
        "FavoriteCharacter", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "lastname": self.lastname,
            "date_subscribed": self.date_subscribed,
            "is_active": self.is_active
            # No incluimos password por seguridad
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    terrain: Mapped[str] = mapped_column(String(120), nullable=True)
    diameter: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Relaciones
    characters = relationship("Character", back_populates="home_planet")
    favorited_by = relationship("FavoritePlanet", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "description": self.description
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    mass: Mapped[int] = mapped_column(Integer, nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    home_planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=True)

    # Relaciones
    home_planet = relationship("Planet", back_populates="characters")
    favorited_by = relationship(
        "FavoriteCharacter", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year,
            "description": self.description,
            "home_planet_id": self.home_planet_id
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)

    # Relaciones
    author = relationship("User", back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "publication_date": self.publication_date,
            "author_id": self.author_id
        }


class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=False)
    date_added: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    # Relaciones
    user = relationship("User", back_populates="favorite_planets")
    planet = relationship("Planet", back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "date_added": self.date_added
        }


class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=False)
    date_added: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    # Relaciones
    user = relationship("User", back_populates="favorite_characters")
    character = relationship("Character", back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "date_added": self.date_added
        }


# Esto genera el diagrama cuando ejecutas el archivo
if __name__ == "__main__":
    from eralchemy2 import render_er
    render_er(db.Model, 'diagram.png')
