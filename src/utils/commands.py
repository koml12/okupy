"""Functions to run when command line flags are specified."""

from settings import APPS

def add_app(name, path):
    if not APPS.get(name):
        APPS[name] = path
        print('App \'{}\' installed'.format(name))
    else:
        if APPS.get(name) != path:
            old_path = APPS.get(name)
            APPS[name] = path
            print('Changed path of \'{}\' from \'{}\' to \'{}\''
                   .format(name, old_path, path))
        else:
            print('App \'{}\' is already included.'.format(name))