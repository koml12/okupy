"""Processes to run the applications and keep track of time."""

import random
from importlib import import_module
from multiprocessing import Manager, Pool
from queue import Empty as EmptyException
from time import sleep

from settings import APPS, ARGS, KWARGS


def run_apps(apps, global_args, global_kwargs, queue):
    """Runs apps at random from a list of class objects.

    Arguments:
        apps {list<class>} -- list of class objects that can be instantiated
                              individually to run the apps.
        global_args {dict<str:tuple>} -- mapping of application names to a
                                         tuple that contains the ordered list
                                         of arguments that can be passed in for
                                         *args to the app's setup() method.
        global_kwargs {dict:<str:dict>} -- mapping of application names to
                                           a dict object that contains the
                                           keyword arguments that can be passed
                                           in for **kwargs to the app's
                                           setup() method.
        queue {Queue} -- shared queue used for interprocess communication
                         with sleep_process.
    """


    time_up = False

    # Going to remove apps from the list after we use them, but we don't
    # want to lose access to the list of apps, so make a copy of the list.
    local_apps = apps[:]

    while local_apps and not time_up:
        app = random.sample(local_apps, 1)[0]    # Get random app from list.
        print(app)

        # Get *args and **kwargs for the setup() method.
        # Defaults to empty if there are no args or kwargs for an app.
        args = global_args.get(app.__name__, ())
        kwargs = global_kwargs.get(app.__name__, {})

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
        except EmptyException:
            pass        # Resume normal execution.

def sleep_process(secs, queue):
    """Sleep for a certain amount of time, and update state when finished.

    Arguments:
        secs {int} -- number of seconds to sleep for.
        queue {Queue} -- shared Queue used for interprocess communication
                         with run_apps.
    """

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
