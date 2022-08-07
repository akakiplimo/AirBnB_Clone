#!/usr/bin/python3
""" Module for BaseModel the super class for the project """


import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """ A class that defines all common attributes/methods for other classes
    Attributes:
        id: BaseModel id
        created_at: time of instance creation
        updated_at: time of instance last update
    Methods:
        save(): Updates updated_at variable
        to_dict(): Returns a dictionary representation of an object
    """

    def __init__(self, *args, **kwargs):
        """ Initializes BaseModel
        Args:
            id (str): Object Universal Unique Identifier
            created_at (datetime): Time when an instance is created
            updated_at (datetime): Time when an instance is changed
        """
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
        """ Returns a string formatted version of an object """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """ Updates updated_at attribute with the current datetime """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """ Returns a dictionary containing
        all keys/values of __dict__ of the instance
        """
        self_dict = dict(self.__dict__)
        self_dict['__class__'] = self.__class__.__name__
        self_dict['created_at'] = datetime.isoformat(self.created_at)
        self_dict['updated_at'] = datetime.isoformat(self.updated_at)
        return self_dict
