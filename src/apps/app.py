from abc import ABC, abstractmethod

class Application(ABC):
    """ Base class for an application to be used with okupy.
    Contains methods for setting up, running, and stopping the application.
    Note that all methods MUST be implemented, even if they are just pass'ed
    """

    @abstractmethod
    def setup(self, *args, **kwargs):
        """ Sets up the state of the application to start the task.
        """
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """ Runs the application task
        """
        pass

    @abstractmethod
    def stop(self, *args, **kwargs):
        """Code to execute when the application is stopped
        """
        pass