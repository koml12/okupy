"""Functions to run when command line flags are specified."""

import json
from ast import literal_eval

from settings import ARGS, KWARGS


def get_app_info(app_list, info_list):
    """Prints out information for each app passed in.
    Prints out the app's documentation and its setup() args and kwargs.

    Arguments:
        app_list {List<class>} -- list of application classes.
        info_list {List<str>} -- list of app names to get info for.
    """

    app_names = [app.__name__ for app in app_list]
    for app in info_list:
        if app in app_names:
            class_obj = next(i for i in app_list if i.__name__ == app)
            print(app)
            print('    {}'.format(class_obj.__doc__))
            print('    setup args: {}'.format(ARGS.get(app)))
            print('    setup kwargs: {}'.format(KWARGS.get(app)))
            print('')

        else:
            print('App {} does not exist'.format(app.__name__))

def override(app_list, override_list):
    """Overrides the entries in ARGS or KWARGS from the global settings to
    customize arguments and keyword arguments for the current instance of
    okupy.

    Arguments:
        app_list {List<class>} -- list of applications that can be run.
        override_list {List<List<str>>} -- outer list of elements, each element
                                           is a three-element list. For each
                                           inner list, the first item is the
                                           app name, the second item is args to
                                           override, and the third item is the
                                           kwargs to override. Note: if either
                                           of the second or third items are '_',
                                           it means do not override the
                                           args/kwargs for the app.
    """

    for command in override_list:
        app_name = command[0]

        # Find if app_name is a valid app to override.
        class_obj = next((i for i in app_list if i.__name__ == app_name),
                         default=None)

        if not class_obj:
            print('Could not override for app {}'.format(app_name))
            continue

        if command[1] != '_':
            new_args = literal_eval(command[1])
            if isinstance(new_args, tuple):
                ARGS[app_name] = new_args
            else:
                print('Malformed args for app {}'.format(app_name))

        if command[2] != '_':
            try:
                new_kwargs = json.loads(command[2])
                KWARGS[app_name] = new_kwargs
            except json.JSONDecodeError:
                print('Malformed kwargs for app {}'.format(app_name))
