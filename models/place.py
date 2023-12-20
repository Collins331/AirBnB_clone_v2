#!/usr/bin/python3
"""Defines the Place class."""
import models
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

association_table = Table(
    "place_amenity", Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"), primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """Represents a Place in the MySQL database.
    Inherits from SQLAlchemy Base. Connects to the MySQL table 'places'.
    Attributes:
        __tablename__ (str): The name of the MySQL table storing places.
        city_id (Column): Place's city id (SQLAlchemy String).
        user_id (Column): Place's user id (SQLAlchemy String).
        name (Column): The name (SQLAlchemy String).
        description (Column): The description (SQLAlchemy String).
        number_rooms (Column): The number of rooms (SQLAlchemy Integer).
        number_bathrooms (Column): The number of bathrooms (SQLAlchemy Integer).
        max_guest (Column): Maximum number of guests (SQLAlchemy Integer).
        price_by_night (Column): Price per night (SQLAlchemy Integer).
        latitude (Column): Place's latitude (SQLAlchemy Float).
        longitude (Column): Place's longitude (SQLAlchemy Float).
        reviews (relationship): Relationship with Review model.
        amenities (relationship): Relationship with Amenity model.
        amenity_ids (list): List of linked amenity IDs.
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def all_reviews(self):
            """Get a list of all linked Reviews."""
            review_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def linked_amenities(self):
            """Get/set linked Amenities."""
            amenity_list = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @linked_amenities.setter
        def linked_amenities(self, value):
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
