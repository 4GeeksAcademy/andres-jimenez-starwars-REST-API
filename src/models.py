from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    favorites = relationship("Favorite", back_populates="user")

class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[str] = mapped_column(String(20))
    gender: Mapped[str] = mapped_column(String(20))

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    terrain: Mapped[str] = mapped_column(String(100))
    population: Mapped[str] = mapped_column(String(100))

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)

    user = relationship("User", back_populates="favorites")
    planet = relationship("Planet")
    people = relationship("People")

   