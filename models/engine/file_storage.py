#!/usr/bin/python3
""" module that defines a class FileStorage for AirBnB clone """
import json
from os.path import exists


class FileStorage:
    """ class that serializes and deserializes between JSON file and instances """
    __file_path = "file.json"
    __objects = dict()

    def all(self):
        """ returns the dictionary __objects """
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        self.__objects[obj.__class__.__name__ + "." + obj.id] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """
        temp = dict()
        for key in self.__objects.keys():
            temp[key] = self.__objects[key].to_dict()
        with open(self.__file_path, mode="w") as jsonFile:
            json.dump(temp, jsonFile)

    def reload(self):
        """ deserializes the JSON file to __objects """
        from ..base_model import BaseModel
        from ..user import User
        from ..state import State
        from ..city import City
        from ..amenity import Amenity
        from ..place import Place
        from ..review import Review

        if exists(self.__file_path):
            with open(self.__file_path) as jsonFile:
                deserialize = json.load(jsonFile)
            for key in deserialize.keys():
                if deserialize[key]['__class__'] == "BaseModel":
                    self.__objects[key] = BaseModel(**deserialize[key])
                elif deserialize[key]['__class__'] == "User":
                    self.__objects[key] = User(**deserialize[key])
                elif deserialize[key]['__class__'] == "State":
                    self.__objects[key] = State(**deserialize[key])
                elif deserialize[key]['__class__'] == "City":
                    self.__objects[key] = City(**deserialize[key])
                elif deserialize[key]['__class__'] == "Amenity":
                    self.__objects[key] = Amenity(**deserialize[key])
                elif deserialize[key]['__class__'] == "Place":
                    self.__objects[key] = Place(**deserialize[key])
                elif deserialize[key]['__class__'] == "Review":
                    self.__objects[key] = Review(**deserialize[key])
