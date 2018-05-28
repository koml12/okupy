"""Test cases for the HackerNews class in hackernews.py"""

import unittest
from os import remove

# pylint: disable=E0401
from hackernews import HackerNews

class HackerNewsTest(unittest.TestCase):
    """Test Cases for the HackerNews class."""

    def setUp(self):
        """Sets up top stories url."""

        self.url = 'https://hacker-news.firebaseio.com/v0/topstories.json'

    def tearDown(self):
        """Cleans up files created during tests."""

        try:
            remove('./hackernews.txt')
        except OSError:
            pass

        try:
            remove('./hackernews2.txt')
        except OSError:
            pass

        try:
            remove('./hackernews3.txt')
        except OSError:
            pass

        try:
            remove('./testfile.txt')
        except OSError:
            pass

    def test_can_create_hackernews(self):
        """Checks if the HackerNews class can be instantiated."""

        hackernews = HackerNews()
        self.assertIsInstance(hackernews, HackerNews)

    def test_setup_no_url(self):
        """Test if a HackerNews instance with no URL gets the default."""

        hackernews = HackerNews()
        hackernews.setup()
        self.assertEqual(hackernews.url, hackernews.TOP_STORIES)

    def test_can_setup_with_defaults(self):
        """Test if a HackerNews instance with a custom URL gets default max and
        file name fields."""

        hackernews = HackerNews()
        hackernews.setup(url=self.url)
        self.assertEqual(hackernews.url, self.url)
        self.assertEqual(hackernews.max, 25)
        self.assertEqual(hackernews.file, './hackernews.txt')

    def test_can_setup_with_max(self):
        """Test if a HackerNews instance can be created with custom max."""

        hackernews = HackerNews()
        hackernews.setup(url=self.url, max=50)
        self.assertEqual(hackernews.url, self.url)
        self.assertEqual(hackernews.max, 50)
        self.assertEqual(hackernews.file, './hackernews.txt')

    def test_setup_fails_negative_max(self):
        """Test if a HackerNews instance fails setup with max <= 0."""

        hackernews = HackerNews()
        self.assertRaises(ValueError, hackernews.setup, url=self.url, max=-1)

    def test_setup_hackernews_with_file(self):
        """Test if a HackerNews instance can be created with a custom output
        file name.
        """

        hackernews = HackerNews()
        hackernews.setup(url=self.url, file='hackernews2.txt')
        self.assertEqual(hackernews.url, self.url)
        self.assertEqual(hackernews.max, 25)
        self.assertEqual(hackernews.file, 'hackernews2.txt')

    def test_setup_hackernews_max_file(self):
        """Test if a HackerNews instance can be created with custom URL, max,
        and filename fields.
        """

        hackernews = HackerNews()
        hackernews.setup(url=self.url, max=50, file='hackernews3.txt')
        self.assertEqual(hackernews.url, self.url)
        self.assertEqual(hackernews.max, 50)
        self.assertEqual(hackernews.file, 'hackernews3.txt')

    def test_can_write_to_file(self):
        """ Test the save_link method on a file.
        Writes to the file (within save_link()) and reads from the file to
        verify that it was in fact written to with the expected data.
        """

        write_str = 'hello\tworld\n'
        filename = 'testfile.txt'
        hackernews = HackerNews()
        hackernews.setup(file=filename)
        hackernews.save_link('hello', 'world')
        with open('testfile.txt', 'r+') as out_file:
            buf = out_file.read(256)
            self.assertEqual(buf, write_str)
