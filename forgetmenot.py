#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""forget me not"""


def create_todo(todos, title, description, level):
    """function that creates the tasks.  Asks for 3 parameters.

    Args:
        todos (str): list of things to do.
        title (str): name of task.
        description (str): description of the task.
        level (str): Level of importance for task (important, medium,
        unimportant).

    """
    todo = {
        'title': title,
        'description': description,
        'level': level,
    }
    todos.append(todo)
    return 'Created task #', len(todos)


def save_todo_list():
    """Function that saves the tasks."""
    save_file = file("todos.pickle", "w")
    pickle.dump(todos, save_file)
    save_file.close()


def load_todo_list():
    """function that loads the file containing saved tasks."""
    global todos
    if os.access("todos.pickle", os.F_OK):
        save_file = file("todos.pickle")
        todos = pickle.load(save_file)


def delete_todo(todos, which):
    """function that deletes a task.  Asks for the number of the task."""
    if not which.isdigit():
        return ("'" + which +
                "' needs to be the number of a task!")
    which = int(which)
    if which < 1 or which > len(todos):
        return ("'" + str(which) +
                " ' needs to be the number of a task!")
    del todos[which - 1]
    return "Deleted task #" + str(which)


def edit_todo(todos, which, title, description, level):
    """function that edits the tasks.  Asks for the number of the task."""
    if not which.isdigit():
        return ("'" + which +
                "' needs to be the number of a task!")
    which = int(which)
    if which < 1 or which > len(todos):
        return ("'" + str(which) +
                "' needs to be the number of a task!")

    todo = todos[which - 1]
    if title != "":
        todo['title'] = title
    if description != "":
        todo['description'] = description
    if level != "":
        todo['level'] = level

    sort_todos()
    return "Edited task #" + str(which)


def capitalize(todo):
    """function that capitalizes 'important' tasks for more clarity."""
    todo['level'] = todo['level'].upper()
    return todo


def show_todo(todo, index):
    """function that shows tasks categorized."""
    wrapped_title = textwrap.wrap(todo['title'], 16)
    wrapped_descr = textwrap.wrap(todo['description'], 24)

    output = str(index + 1).ljust(8) + "  "
    output += wrapped_title[0].ljust(16) + "  "
    output += wrapped_descr[0].ljust(24) + "  "
    output += todo['level'].ljust(16)
    output += "\n"

    max_len = max(len(wrapped_title),
                  len(wrapped_descr))
    for index in range(1, max_len):
        output += " " * 8 + "  "
        if index < len(wrapped_title):
            output += wrapped_title[index].ljust(16) + "  "
        else:
            output += " " * 16 + "  "
        if index < len(wrapped_descr):
            output += wrapped_descr[index].ljust(24) + "  "
        else:
            output += " " * 24 + " "
        output += "\n"
    return output


def sort_todos(todos):
    """Function that sorts the tasks."""
    important = [capitalize(todo) for todo in todos
                 if todo['level'].lower() == 'important']
    unimportant = [todo for todo in todos
                   if todo['level'].lower() == 'unimportant']
    medium = [todo for todo in todos
              if todo['level'].lower() != 'important' and
              todo['level'].lower() != 'unimportant']
    todos = important + medium + unimportant
    return todos


def show_todos(todos):
    """function that creates the header for the tasks."""
    output = ("Item      Title             "
              "Description               Level           \n")
    sorted_todos = sort_todos(todos)

    for index, todo in enumerate(todos):
        output += show_todo(todo, index)
    return output


def help_commands(todos = None):
    """function that returns the available commands."""
    return commands.keys()

commands = {
    'help':   [help_commands, []],
    'new':    [create_todo,   ['title', 'description', 'level']],
    'show':   [show_todos,    []],
    'delete': [delete_todo,   ['which']],
    'edit':   [edit_todo,     ['which', 'title', 'description', 'level']]
}

todos = []


def run_command(user_input, data=None):
    """function that lowers the cases for user input.  Also promts the user
       when presented with an invalid command."""
    user_input = user_input.lower()
    if user_input not in commands:
        return user_input + "?" \
                            " Sorry, I do not recognize that command."
    else:
        the_func = get_function(user_input)

    if data is None:
        the_fields = get_fields(user_input)
        data = get_input(the_fields)
    return the_func(todos, **data)


def get_function(command_name):
    return commands[command_name][0]


def get_fields(command_name):
    return commands[command_name][1]


def get_input(fields):
    """function that takes input"""
    user_input = {}
    for field in fields:
        user_input[field] = raw_input(field + " > ")
    return user_input


def main_loop():
    """function is the main loop of the program."""
    load_todo_list()
    print "*****Welcome To ForgetMeNot*****"
    print "This program will help you organize"
    print "your tasks by their 'Title', 'Decription',"
    print "and 'Level' of importance!"
    print "                                "
    print "Here are the available commands:"
    print "'new' = Create a new task."
    print "'edit' = Edit an existing task."
    print "'delete' = Delete an existing task."
    print "'show' = Show your existing tasks."
    print "'help' = Remind you of the existing commands."
    print "'quit' = Quit the program.\n"
    while True:
        user_input = raw_input("Enter your command > ")
        if user_input.lower().startswith("quit"):
            print "Exiting...  Thank You for using 'Forget Me Not'!"
            break
        print run_command(user_input)
    save_todo_list()


if __name__ == '__main__':
    main_loop()
