#!/usr/bin/env python3

"""Main program. Handles command line inputs and spawns processes as defined
in src/utils/processes.py
"""

import os
import sys
from importlib import import_module
from multiprocessing import Manager, Pool

from settings import APPS, ARGS, KWARGS
from src.utils.processes import run_apps, sleep_process
from src.utils.times import str_to_secs


def main():
    if len(sys.argv) != 2:
        # Invalid invocation.
        print('Error: Usage is ./okupy <time>')
        sys.exit(1)

    secs = str_to_secs(sys.argv[1])

    if secs == -1:
        # Invalid time input.
        print('Invalid time input. Suffixes of \'s\', \'m\', or \'h\' are allowed.')
        sys.exit(1)

    # Get the <class> objects for each class specified in the APPS dictionary.
    # Each element app in app_list can be instantiated by calling app().
    app_list = []
    for app_name in APPS:
        module = import_module(APPS.get(app_name))
        app = getattr(module, app_name)
        app_list.append(app)
    print(app_list)

    print('okupy pid is {}'.format(os.getpid()))

    # Create a queue from a manager so we can share it through out processes.
    manager = Manager()
    queue = manager.Queue()

    pool = Pool(processes=2)
    pool.apply_async(sleep_process, args=(secs, queue))
    pool.apply(run_apps, args=(app_list, ARGS, KWARGS, queue))


if __name__ == '__main__':
    main()
