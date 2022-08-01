#!/usr/bin/python3
"""Module that contains a class BaseModel"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """ A class that defines all common attributes/methods for other classes
    Attributes:
        id: BaseModel id
        created_at: time of instance creation
        updated_at: time of instance last update
    """

    def __init__(self, *args, **kwargs):
        """ initializes BaseModel """
        if kwargs is None or len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, time)
                elif key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """ prints formal class description of the BaseModel instance """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """ updates updated_at attribute with the current datetime """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """ display a dictionary containing all keys of __dict__ of the instance """
        self_dict = dict(self.__dict__)
        self_dict['__class__'] = self.__class__.__name__
        self_dict['created_at'] = datetime.isoformat(self.created_at)
        self_dict['updated_at'] = datetime.isoformat(self.updated_at)
        return self_dict
