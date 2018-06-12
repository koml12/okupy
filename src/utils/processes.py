"""Processes to run the applications and keep track of time."""

import random
from importlib import import_module
from multiprocessing import Pool, Manager
from queue import Empty
from time import sleep

from settings import APPS, ARGS, KWARGS


def run_apps(apps, g_args, g_kwargs, queue):

    time_up = False

    # Going to remove apps from the list after we use them, but we don't
    # want to lose access to the list of apps, so make a copy of the list.
    local_apps = apps[:]

    while local_apps and not time_up:
        app = random.sample(local_apps, 1)[0]    # Get random app from list.
        print(app)
        
        # Get *args and **kwargs for the setup() method.
        # Defaults to empty if there are no args or kwargs for an app.
        args = g_args.get(app.__name__, ())
        kwargs = g_kwargs.get(app.__name__, {})

        # Instantiate, setup, and run the app.
        # pylint: disable=E1102
        runnable_app = app()
        runnable_app.setup(*args, **kwargs)
        runnable_app.run()
        runnable_app.stop()

        local_apps.remove(app)

        # Check if the time limit has expired.
        try:
            queue.get(timeout=0.001)    # Very low timeout to prevent blocking.
            time_up = True
        except Empty:
            pass        # Resume normal execution.

def sleep_process(secs, queue):
    sleep(secs)
    queue.put(True, timeout=0.001)      # Low timeout to prevent blocking.    

if __name__ == '__main__':
    app_list = []
    for app_name in APPS:
        module = import_module(APPS.get(app_name))
        app = getattr(module, app_name)
        app_list.append(app)
    print(app_list)


    manager = Manager()
    queue = manager.Queue()

    pool = Pool(processes=2)
    pool.apply(run_apps, args=(app_list, ARGS, KWARGS, queue))
    pool.apply_async(sleep_process, args=(5, queue))
