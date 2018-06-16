#!/usr/bin/env python3

"""Main program. Handles command line inputs and spawns processes as defined
in src/utils/processes.py
"""

import argparse
import os
import sys
from importlib import import_module
from multiprocessing import Manager, Pool

from settings import APPS, ARGS, KWARGS
from src.utils.processes import run_apps, sleep_process
from src.utils.times import str_to_secs
from src.utils import commands


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--time', nargs=1, 
                        help='Amount of time to run application for')

    parser.add_argument('-e', '--exclude', nargs='*',
                        help='Exclude apps from running in the current instance'
                        + ' of okupy')

    parser.add_argument('-i', '--info', nargs='*',
                        help='Get info about specific apps')

    parser.add_argument('-o', '--override', nargs='*',
                        help='Override args and kwargs for apps at runtime')

    args = parser.parse_args()

    print(args)

    excluded_apps = []

    if args.exclude:
        for app in args.exclude:
            excluded_apps.append(app)

    if args.time:
        secs = str_to_secs(args.time[0])
        if secs == -1:
            # Invalid time input.
            print('Invalid time input. Suffixes of \'s\', \'m\', or \'h\' are allowed.')
            sys.exit(1)

        # Get the <class> objects for each class specified in the APPS dictionary.
        # Each element app in app_list can be instantiated by calling app().
        app_list = []
        for app_name in APPS:
            if app_name not in excluded_apps:
                module = import_module(APPS.get(app_name))
                app = getattr(module, app_name)
                app_list.append(app)
        print(app_list)

        # Create a queue from a manager so we can share it through out processes.
        manager = Manager()
        queue = manager.Queue()

        pool = Pool(processes=2)
        pool.apply_async(sleep_process, args=(secs, queue))
        pool.apply(run_apps, args=(app_list, ARGS, KWARGS, queue))


if __name__ == '__main__':
    main()
