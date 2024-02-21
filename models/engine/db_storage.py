#!/usr/bin/python3
"""DB storage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """DB storage engine definition"""
    __engine = None
    __session = None

    def __init__(self):
        """init method -> constructor"""
        self.__engine = create_engine(
                "mysql+mysqldb://{}:{}@{}/{}".format(
                    getenv("HBNB_MYSQL_USER"),
                    getenv("HBNB_MYSQL_PWD"),
                    getenv("HBNB_MYSQL_HOST"),
                    getenv("HBNB_MYSQL_DB")
                    ),
                pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """queries to return objects based on `cls"""
        objects = {}
        #classes = [State, City, Place, Amenity, Review, User]
        classes = [State, City, User, Place]
        if cls is not None:
            if isinstance(cls, str):
                try:
                    cls = eval(cls)
                except Exception:
                    pass
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for obj in classes:
                objs = self.__session.query(obj).all()
                for ob in objs:
                    key = "{}.{}".format(type(ob).__name__, ob.id)
                    objects[key] = ob
        return objects

    def new(self, obj):
        """adds the object to the current session"""
        if obj:
            self.__session.merge(obj)

    def save(self):
        """commits all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from the session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in the db, reloads"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
