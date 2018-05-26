"""
Application that allows the user to read Hacker News headlines and save any
links they want to check out later.
"""

# TODO: add a base url for getting data for an item.
# TODO: implement the run() method.

# pylint: disable=redefined-builtin
from os import O_APPEND, O_CREAT, close, open, write
from stat import S_IRWXU

import requests

# pylint: disable=E0401
from app import Application


class HackerNews(Application):
    """Get top stories from Hacker News, and offer users the choice to save
    links to a file for later viewing.
    """
    def __init__(self):
        """Initializes object. Sets fields to impossible values, because the
        user should call setup() upon instantiating the class.
        """

        super(HackerNews, self).__init__()
        self.url = ''
        self.max = -1
        self.file_descr = -1

    def setup(self, *args, **kwargs):
        """Sets up URL base for getting stories from HN, as well as an optional
        maximum number of stories to get (defaults to 25).

        Arguments:
            kwargs {dict} -- specify properties of application.
                             url  -- url to query for stories.
                             max  -- max number of stories to look through.
                                     defaults to 25
                             file -- file to write saved stories to.
                                     defaults to './hackernews.txt'

        Raises:
            ValueError -- if no url is specified.
        """

        if 'url' not in kwargs:
            raise ValueError('Must specify a url path to start up the app.')

        self.url = kwargs.get('url')

        if 'max' in kwargs:
            if kwargs.get('max') <= 0:
                raise ValueError('Max stories must be greater than 0')
            self.max = kwargs.get('max')
        else:
            self.max = 25

        if 'file' in kwargs:
            self.file_descr = open(kwargs.get('file'), O_APPEND | O_CREAT, 
                                   S_IRWXU)
        else:
            self.file_descr = open('./hackernews.txt', O_APPEND | O_CREAT, 
                                   S_IRWXU)
        
        if self.file_descr < 0:
            raise ValueError('Failed to open file.')

    def run(self, *args, **kwargs):
        pass

    def stop(self, *args, **kwargs):
        """Closes file descriptors and cleans up after application finishes.
        """

        close(self.file_descr)

    def is_setup(self):
        """Checks if the setup() method has been run yet.

        Returns:
            {bool} -- true if setup() has been run, false otherwise.
        """

        return (self.url != '') and (self.max != -1) and (self.file_descr != -1)

    def save_link(self, title, link):
        """Writes the title and the link to the object's 'file' field.

        Arguments:
            title {str} -- title of the story.
            link {str} -- link to the story.
        """

        if self.is_setup():
            write(self.file_descr, '{}\t{}\n'.format(title, link))
        else:
            raise ValueError('Run setup() before calling other functions.')


def main():
    hacker_news = HackerNews()
    hacker_news.setup(url='yo')
    hacker_news.run()
    hacker_news.stop()

if __name__ == '__main__':
    main()
