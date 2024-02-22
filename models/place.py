#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy import Table
from models.amenity import Amenity
from sqlalchemy.orm import relationship
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"), primary_key=True,
                                 nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"), primary_key=True,
                                 nullable=False)
                          )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", cascade="all, delete", backref="place")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False, backref="place_amenities")
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """reviews -> getter"""
            from models import storage
            from models import Review
            rev_dict = storage.all(Review)
            rev_list = [rev for rev in rev_dict.values()
                        if rev.place_id == self.id]
            return rev_list

        @property
        def amenities(self):
            """amenities -> getter"""
            am_list = []
            for i in list(models.storage.all(Amenity).values()):
                if i.place_id == self.id:
                    am_list.append(i)
            return am_list

        @amenities.setter
        def amenities(self, obj):
            """amenities -> setter"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
