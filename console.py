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
        print("Quit command to exit the program\n")

    def do_EOF(self, arg):     
        """ Exits the program """
    
        print("")
        return True

    def help_EOF(self):
        """ Print help for the EOF command """
        print("EOF command to exit the program\n")

    def emptyline(self):
        """ does nothing when an empty line + ENTER are executed """
        pass

    def do_create(self, arg):
        """ Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        Ex: $ create BaseModel
        """
        arg_list = HBNBCommand.cmd_parse(arg)

        if len(arg_list) == 0:
            print("** class name missing **")
            return False

        if len(arg_list) > 1:
            print("** Too many arguments **")
            return False

        if (arg_list[0] in HBNBCommand.__class_list.keys()):
            new_obj = HBNBCommand.__class_list[arg_list[0]]()
            new_obj.save()
            print(new_obj.id)
        else:
            print("** class doesn't exist **")

    def help_create(self):
        """
        Print help for the create command
        """
        print("""
        Creates a new instance of the class passed as the
        1st argument, saves it (to the JSON file) and prints the id
        Ex: $ create BaseModel 1234-1234-1234""")

    def do_show(self, arg):
        """ Prints the string representation of an instance based
        on the class name and id. Ex: $ show BaseModel 1234-1234-1234 """
        arg_list = HBNBCommand.cmd_parse(arg)
        db = storage.all()

        if not len(arg_list):
            print("** class name missing **")
        elif (arg_list[0] not in HBNBCommand.__class_list.keys()):
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in db:
            print("** no instance found **")
        else:
            print(db["{}.{}".format(arg_list[0], arg_list[1])])

    def help_show(self):
        """
        Print help for the show command
        """
        print("""
        Prints the string representation of an
        instance based on the class name and id
        Ex: $ show BaseModel 1234-1234-1234""")

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234"""
        arg_list = HBNBCommand.cmd_parse(arg)
        storage.reload()
        db = storage.all()
 
        if not len(arg_list):
            print("** class name missing **")
        elif (arg_list[0] not in HBNBCommand.__class_list.keys()):
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in db:
            print("** no instance found **")
        else:
            del db["{}.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def help_destroy(self):
        """ Print help for the destroy command """
        print("""
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234
        """)

    def do_all(self, arg):
        """ Prints all string representations of all the instances based or not on the class name
        Ex: $ all BaseModel or $ all"""
        arg_list = HBNBCommand.cmd_parse(arg)

        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.__class_list.keys():
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg_list) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def help_all(self):
        """ Print help for the all command """
        print("""
        Prints all string representation of all instances
        based or not on the class name. Ex: $ all BaseModel or $ all
        """)

    def do_update(self, arg):
        """ Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file)"""
        arg_list = HBNBCommand.cmd_parse(arg)
        obj_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False

        if arg_list[0] not in HBNBCommand.__class_list:
            print("** class doesn't exist **")
            return False

        if len(arg_list) == 1:
            print("** instance id missing **")
            return False

        if "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False

        if len(arg_list) == 2:
            print("** attribute name missing **")

        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_list) == 4:
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
        adding or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """)
    def emptyline(self):
        """
            Does nothing if Empty line + enter is inserted.
            Used for overriding the emptyline function
        """
        pass

    def do_count(self, arg):
        """
            Prnits the number of elements inside the FileStorage that
            are of instances of cls
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

    def default(self, line):
        """
            Handles the case where the the command has no equivlaent
            do_ method
        """

        line_p = HBNBCommand.cmd_parse(line, '.')
        if line_p[0] in HBNBCommand.__class_list.keys() and len(line_p) > 1:
            if line_p[1][:-2] in HBNBCommand.__class_funcs:
                func = line_p[1][:-2]
                cls = HBNBCommand.__class_list[line_p[0]]
                eval("self.do_" + func)(cls.__name__)
            else:
                print("** class doesn't exist **")
        else:
            super().default(line)
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
