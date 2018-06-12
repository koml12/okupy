"""Global and application specific settings for okupy."""

"""Stores apps in app_name: app_path format.
Where app_name extends the abstract base class App and app_path is a path to
the location of the app_name class.
"""
APPS = {
    'HackerNews': 'src.apps.hackernews',
    'Twitter': 'src.apps.twitter',
}

"""A str-to-tuple mapping of application names (as defined in the APPS dict
above) to a variable length tuple of arguments that will be passed in as *args
when calling the setup() function of the application.
"""
ARGS = {
}

"""A str-to-dict mapping of application names (as defined in the APPS dict
above) to a variable length dict consisting of keyword arguments that will be
passed in as **kwargs when calling the setup() function of the application.
"""
KWARGS = {
    'HackerNews': {
        'max': 10,
        'file': './hackernews2.txt',
    },
}
