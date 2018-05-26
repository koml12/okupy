"""Unit tests for app.py
"""

import unittest

# pylint: disable=E0401
from app import Application

class ApplicationTestCases(unittest.TestCase):
    """Test cases for the Application class in app.py"""

    def test_abstract_class(self):
        """Checks if the Application class is actually abstract.
        That is, the Application class can be instantiated without throwing a
        TypeError due to unimplemented abstract methods.
        """

        self.assertRaises(TypeError, Application)
