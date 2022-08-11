#!/usr/bin/python3
""" A Command interpreter for AirBnB clone"""
import cmd


from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ cmd class for the AirBnB clone project """
    prompt = '(hbnb) '
    __class_list = {
        BaseModel.__name__: BaseModel,
        User.__name__: User,
        State.__name__: State,
        City.__name__: City,
        Amenity.__name__: Amenity,
        Review.__name__: Review,
        Place.__name__: Place
    }
    __class_funcs = ["all", "count", "show", "destroy", "update"]

    @staticmethod
    def cmd_parse(arg, id=" "):
        """ Returns a list containing
        parsed arguments from a string """
        arg_list = arg.split(id)
        new_arg_list = []

        for string in arg_list:
            if string != '':
                new_arg_list.append(string)
        return new_arg_list

    def do_quit(self, arg):
        """ Exits the program """
        return True

    def help_quit(self):
        """ Print help for the quit command """
        print("Exits the program\n")

    def do_EOF(self, arg):
        """ Exits the program """

        print("")
        return True

    def help_EOF(self):
        """ Print help for the EOF command """
        print("Exits the program\n")

    def emptyline(self):
        """ Does nothing when empty line + ENTER is executed """
        pass

    def do_create(self, arg):
        """ Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        Ex: $ create BaseModel
        """
        if arg == '' or arg is None:
            print("** class name missing **")

        elif arg not in storage.classes():
            print("** class doesn't exist **")

        else:
            new_obj = storage.classes()[arg]()
            new_obj.save()
            print(new_obj.id)

    def help_create(self):
        """
        Print help for the create command
        """
        print("""
        Creates a new instance of the class passed as the
        argument, saves it and prints its id
        Ex: $ create BaseModel""")

    def do_show(self, arg):
        """ Prints the string representation of an instance based
        on the class name and id.
        """
        db = storage.all()

        if arg == "" or arg is None:
            print("** class name missing **")
        else:
            arg_list = arg.split(' ')
            if arg_list[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(arg_list) == 1:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(arg_list[0], arg_list[1])
                if key not in db:
                    print("** no instance found **")
                else:
                    print(db[key])

    def help_show(self):
        """
        Print help for the show command
        """
        print("""
        Prints the string representation of an instance
        based on the class name and id
        Ex: $ show BaseModel 1234-1234-1234""")

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name and id """
        db = storage.all()

        if arg == "" or arg is None:
            print("** class name missing **")
        else:
            arg_list = arg.split(' ')
            if arg_list[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(arg_list) == 1:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(arg_list[0], arg_list[1])
                if key not in db:
                    print("** no instance found **")
                else:
                    del db[key]
                    storage.save()

    def help_destroy(self):
        """ Print help for the destroy command """
        print("""
        Deletes an instance based on the class name and id
        Ex: $ destroy BaseModel 1234-1234-1234
        """)

    def do_all(self, arg):
        """ Prints all string representations of all the instances
        based on or not on the class name
        """
        obj_list = []
        if arg != "":
            arg_list = arg.split(' ')

            if arg_list[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                for key, obj in storage.all().items():
                    if type(obj).__name__ == arg_list[0]:
                        obj_list.append(obj.__str__())
                print(obj_list)
        else:
            for key, obj in storage.all().items():
                obj_list.append(obj.__str__())
            print(obj_list)

    def help_all(self):
        """ Print help for the all command """
        print("""
        Prints all string representations of all instances
        based on or not on the class name.
        Ex: $ all BaseModel
          : $ all
        """)

    def do_update(self, arg):
        """ Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file)"""
        arg_list = HBNBCommand.cmd_parse(arg)
        obj_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False

        elif arg_list[0] not in HBNBCommand.__class_list:
            print("** class doesn't exist **")
            return False

        elif len(arg_list) == 1:
            print("** instance id missing **")
            return False

        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False

        elif len(arg_list) == 2:
            print("** attribute name missing **")

        elif len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        elif len(arg_list) == 4:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = valtype(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            for k, v in eval(arg_list[2]).items():
                if (k in obj.__class__.__dict__.keys() and type(
                        obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v

        storage.save()

    def help_update(self):
        """ Print help for the update command """
        print("""
        Updates an instance based on the class name and id by
        adding or updating attribute.
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """)

    def do_count(self, arg):
        """
            Prints the number of elements inside the FileStorage that
            are instances of cls
        """
        arg_list = HBNBCommand.cmd_parse(arg)
        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.__class_list:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg_list) == 0:
                    obj_list.append(obj.__str__())
            print(len(obj_list))

    def parse(self, args):
        """strtok"""
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """ Handles cases where the the command has no equivalent
        do_method
        """
        args = line.split('.')
        if len(args) >= 2:
            if args[1] == "all()":
                self.do_all(args[0])
            elif args[1] == "count()":
                self.do_count(args[0])
            elif args[1][:4] == "show":
                self.do_show(self.parse(args))
            elif args[1][:7] == "destroy":
                self.do_destroy(self.parse(args))
            elif args[1][:6] == "update":
                arg = self.parse(args)
                if isinstance(arg, list):
                    obj = models.storage.all()
                    key = arg[0] + ' ' + arg[1]
                    for k, v in arg[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(arg)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
