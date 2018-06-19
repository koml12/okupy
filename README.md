# okupy
A terminal only application hub that helps you control your procrastination.

# Installing
+ Clone the repository with `git clone https://github.com/koml12/okupy`
+ `cd okupy` into the outer directory, and run `./okupy.py` with any of the command line flags specified below.

# Usage
+ The program is meant to be run as a python script with various command line options.
+ `-t <val>` or `--time <val>` --- specify the amount of time the program should be running for. 
    + The time value should be an integer with an optional one letter suffix at the end.
    + The default unit for a plain integer is seconds, but there are suffixes included for convenience. There are suffixes of (s)econds, (m)inutes, and (h)ours available.
    + When the timer is up, no more applications will be started, and the program will terminate after the current application is finished. 
    + Specifying a time value will start up the program. Any other flags passed in will not start the program.
    
+ `-e <app> <app> ...` or `--exclude <app> <app> ...` --- exclude certain applications for running in this instance of the program.
    + Can take any number of app names.
    + Misspelled or nonexistent app names will be ignored (with a small message for the user's information).
    + Note: this flag does nothing if the `--time` flag is not specified, because it only affects the program at runtime. 
    
+ `-i <app> <app> ...` or `--info <app> <app> ...` --- get info about apps.
     + Can take any number of app names.
     + Misspelled or nonexistent app names will be ignored (with a small message for the user's information).
     + Displays the documentation for the app's class, and lists its *args* and *kwargs* that will be used to set up the app.
     + Note: while this flag can work with the `--time` flag, it really isn't the best idea to use with it in practice. Most applications will use stdout to communicate with the user, and since the `--info` flag prints to stdout before apps get executed, it is likely that the information the user wants will get lost during the running of the applications.
    
+ `-o` or `--override` --- override *args* and *kwargs* values for apps for the current instance of the program.
    + Not implemented yet, more details to come!
    
    
# Creating New Applications
+ While the goal of the program is to provide as many quality applications as possible for the user, some users might want specific applications that aren't included out-of-the-box. It is simple to create your own application and integrate it into use of the program.
+ To create an application, change into the `src/apps` directory, and create a new `.py` file. For this example, we'll say that we create `foo.py`.
+ Inside `foo.py`, create a class extending the base `Application` class in the directory, for example, if the class was named Bar, `class Bar(Application):`.
+ Extending the *Application* class requires for 3 methods to be overriden, `setup(*, **)`, `run(*, **)`, and `stop(*, **)`. The methods will be called in that order when running the app, so write any code as if the methods were to be called in that order.
+ Once the class has been written, change into the outer project directory and edit `settings.py`.
+ In the `APPS` dictionary, add a line with the class name mapped to a path to the file the class is in (both strings). For our example above, the line would look like `'Bar': 'src.apps.foo'`.
+ In the `ARGS` and `KWARGS` dictionaries, you can add an entry that contains the app name mapped to either a tuple (of args) or a dictionary (of kwargs), that will be passed into the `setup()` function for the application.
+ In total, our sample application might look something like this:
```python
# In file src/apps/foo.py
from src.apps.app import Application

class Bar(Application):
    def setup(*args, **kwargs):
        # Set up environment to run the app here.
        pass
        
    def run(*args, **kwargs):
        # The "main method" of the app that does the bulk of the execution.
        pass
        
    def stop(*args, **kwargs):
        # Clean up environment if necessary.
        pass
```

```python
# In file settings.py
APPS = {
    ...,
    'Bar', 'src.apps.foo',
}

ARGS = {
   ...,
   'Bar': (list, of, args),
}

KWARGS = {
   ...,
   'Bar': {
       dict: of,
       any: kwargs,
    },
}
```
