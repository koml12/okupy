#!/usr/bin/env python3

import sys
from src.utils.times import str_to_secs, TimeThread
from settings import APPS
from importlib import import_module
import importlib

def main():
    if len(sys.argv) != 2:
        # Invalid invocation.
        print('Error: Usage is ./okupy <time>')
        sys.exit(1)

    secs = str_to_secs(sys.argv[1])
    
    if (secs == -1):
        # Invalid time input.
        print('Invalid time input. Suffixes of \'s\', \'m\', or \'h\' are allowed.')
        sys.exit(1)
    
    """
    The code below is used to import the classes from the settings.py file.
    We can then instantiate the classes however we want by just iterating over
    the list.

    The app list should be passed over to another thread that actually runs 
    the applications in the background.

    app_list = []
    for app_name in APPS:
        module = import_module(APPS.get(app_name))
        app = getattr(module, app_name)
        app_list.append(app)
    print(app_list)
    """
    time_thread = TimeThread(secs)
    time_thread.run()

if __name__ == '__main__':
    main()