# AirBnB clone - The Console

![hbnb-image](https://github.com/akakiplimo/AirBnB_clone/tree/main/imgs/hbnb.png)

## Description
This is an AirBnB clone project that allows users to search for a place to stay in a location of their choice and book it for whatever period of time as per the agreement with the owner of the stay.
This team project is the first step towards building a first full web application.
It consists of a custom command-line interface(console) and the base classes for data storage.

`console' capabilities:
- Create a new object (ex: a new User or a new Place)
- Retrieve an object from a file, a database etc…
- Do operations on objects (count, compute stats, etc…)
- Update attributes of an object
- Destroy an object

## Installation
```
git clone https://github.com/akakiplimo/AirBnB_clone.git
cd AirBnB_clone
```
## Usage
The **console** works both in interactive and non-interactive mode.
It prints a prompt `(hbnb)` and waits for user input.

Interactive mode example
```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(hbnb)
(hbnb)
(hbnb) quit
```
Non-interactive mode example
```
$ echo "help" | ./console.py
(hbnb)
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(hbnb)
$
$ echo "help create" | ./console.py
(hbnb)
	Creates a new instance of the class passed as the
        argument, saves it and prints its id
        Ex: $ create BaseModel
(hbnb)
```

## Command Syntax and Usage

Command | Syntax | Use
------- | ------ | ------
console | `./console` | Run the console
help | `help`, `help [option]` | Display help information for a command
EOF | `EOF` | Exit the console
quit | `quit` | Exit the console
create | `create [class_name]` | Create an instance of class_name (prints its id)
show | `show [class_name] [object_id]` | Display all attributes of an object
all | `all`, `all [class_name]` | Display all instances saved to file or Display all class_name instances
update | `update [class_name] [object_id] [attribute_name] [attribute]` | Update an instance's attributes
destroy | `destroy [class_name] [object_id]` | Delete an object
count | `count [class_name]` | Count all instances of class_name

## Models
All classes for the project are in the folder [models](./models/)

File | Description | Attributes
---- | ----------- | ----------
[base_model.py](./models/base_model.py) | BaseModel class for all the other classes | id, created_at, updated_at
[user.py](./models/user.py) | User class for future user information | email, password, first_name, last_name
[amenity.py](./models/amenity.py) | Amenity class for future amenity information | name
[city.py](./models/city.py) | City class for future location information | state_id, name
[state.py](./models/state.py) | State class for future location information | name
[place.py](./models/place.py) | Place class for future accomodation information | city_id, user_id, name, description, number_rooms, number_bathrooms, max_guest, price_by_night, latitude, longitude, amenity_ids
[review.py](./models/review.py) | Review class for future user/host review information | place_id, user_id, text

## File Storage
Data serialization and deserialization is done using JSON format. This is handled by [engine](./models/engine/)

The [FileStorage](./models/engine/file_storage.py) class has methods enabling it to follow this flow:
```<object> -> to_dict() -> <dictionary> -> JSON dump -> <json string> -> FILE -> <json string> -> JSON load -> <dictionary> -> <object>```
The [__init__.py](./models/__init__.py) file contains an instantiation of the FileStorage class called **storage**, followed by a call to the method reload() on that instance allowing storage to be reloaded automatically at initialization, which recovers the serialized data.

## Tests
Testing is done using the **unittest** module
The tests can be found in the test_models(./tests/test_models/) folder.

## Authors
- [Adrian Abraham Kiplimo](https://github.com/akakiplimo)
- [Sharon Nderi](https://github.com/SNderi)
