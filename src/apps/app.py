"""Class describing an abstract Application for use with okupy."""

import sys
from abc import ABC, abstractmethod

class Application(ABC):
    """ Base class for an application to be used with okupy.
    Contains methods for setting up, running, and stopping the application.
    Note that all methods MUST be implemented, even if they are just pass'ed
    """

    def __init__(self):
        # Forces output to the terminal window. Normally, you wouldn't need to
        # do this because you're in 'interactive mode', but because apps run as
        # parts of subprocesses, we need to specifically bind stdin to the
        # current terminal.
        sys.stdin = open('/dev/tty')


    @abstractmethod
    def setup(self, *args, **kwargs):
        """ Sets up the state of the application to start the task.
        """
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """ Runs the application task.
        """
        pass

    @abstractmethod
    def stop(self, *args, **kwargs):
        """Code to execute when the application is stopped.
        """
        pass
