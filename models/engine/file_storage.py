#!/usr/bin/python3
""" File Storage module to serialize instances to a JSON file
and deserialize JSON file to instances
"""


import json
from os.path import exists


class FileStorage:
    """ Serializes instances to a JSON file and
    deserializes JSON file to instances.
    Attr:
        file_path: (private) string - Path to the JSON file
        objects: (private) dictionary - Stores all objects by <class name>.id

    Methods:
        all(): returns the dictionary __objects
        new(): sets in __objects the obj with key <obj class name>.id
        save(): serializes __objects to the JSON file
        reload(): deserializes the JSON file to __objects
    """
    __file_path = "file.json"
    __objects = dict()

    def all(self):
        """ Returns the dictionary __objects """
        return FileStorage.__objects

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id """
        FileStorage.__objects[obj.__class__.__name__ + "." + obj.id] = obj

    def save(self):
        """ Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists,
        If the file doesn’t exist, no exception is raised)
        """
        temp = dict()
        for key in FileStorage.__objects.keys():
            temp[key] = FileStorage.__objects[key].to_dict()
        with open(FileStorage.__file_path, mode="w", encoding='utf-8') as Fil:
            json.dump(temp, Fil)

    def reload(self):
        """ Deserializes the JSON file to __objects """
        from ..base_model import BaseModel
        from ..user import User
        from ..state import State
        from ..city import City
        from ..amenity import Amenity
        from ..place import Place
        from ..review import Review

        if exists(FileStorage.__file_path):
            with open(FileStorage.__file_path) as jsonFile:
                deserialize = json.load(jsonFile)
            for key in deserialize.keys():
                if deserialize[key]['__class__'] == "BaseModel":
                    FileStorage.__objects[key] = BaseModel(**deserialize[key])
                elif deserialize[key]['__class__'] == "User":
                    FileStorage.__objects[key] = User(**deserialize[key])
                elif deserialize[key]['__class__'] == "State":
                    FileStorage.__objects[key] = State(**deserialize[key])
                elif deserialize[key]['__class__'] == "City":
                    FileStorage.__objects[key] = City(**deserialize[key])
                elif deserialize[key]['__class__'] == "Amenity":
                    FileStorage.__objects[key] = Amenity(**deserialize[key])
                elif deserialize[key]['__class__'] == "Place":
                    FileStorage.__objects[key] = Place(**deserialize[key])
                elif deserialize[key]['__class__'] == "Review":
                    FileStorage.__objects[key] = Review(**deserialize[key])

    def classes(self):
        """ Returns a dictionary of valid classes and their references. """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes
