"""Thread that runs the applications given by the program."""

import threading
import random
from settings import APPS, ARGS, KWARGS
from importlib import import_module

class WorkThread(threading.Thread):
    """Runs applications in a separate thread from the user."""

    def __init__(self, apps, args, kwargs):
        """Sets up thread and checks validity of passed in data.
        
        Arguments:
            apps {list<class>} -- a list of class objects, one for each 
                                  application, that can be instantiated 
                                  and run by the thread.
            args {dict<str:tuple>} -- a mapping of app names to the tuple that
                                      will be passed in as *args when calling 
                                      the application's setup() function.
            kwargs {dict<str:dict>} -- a mapping of app names to the dict that
                                       will be passed in as **kwargs when 
                                       calling the application's setup()
                                       function.
        """
        threading.Thread.__init__(self, daemon=True)
        self.apps = apps
        self.args = args
        self.kwargs = kwargs

    def run(self):
        # Going to remove apps from the list after we use them, but we don't 
        # want to lose access to the list of apps, so make a copy of the list.
        local_apps = self.apps[:]

        while len(local_apps) > 0:
            app = random.sample(local_apps, 1)[0]    # Get random app from list.
            print(app)
            
            # Get *args and **kwargs for the setup() method.
            # Defaults to empty if there are no args or kwargs for an app.
            args = self.args.get(app.__name__, ())
            kwargs = self.kwargs.get(app.__name__, {})

            # Instantiate, setup, and run the app.
            runnable_app = app()
            runnable_app.setup(*args, **kwargs)
            runnable_app.run()
            runnable_app.stop()

            local_apps.remove(app)
            

    
def main():
    """Testing code for the worker thread, by simulating its regular usage
    without a time limit.
    """
    app_list = []
    for app_name in APPS:
        module = import_module(APPS.get(app_name))
        app = getattr(module, app_name)
        app_list.append(app)
    print(app_list)

    work_thread = WorkThread(app_list, ARGS, KWARGS)
    work_thread.run()

if __name__ == '__main__':
    main()
    


