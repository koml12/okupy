"""
Application that allows the user to read Hacker News headlines and save any
links they want to check out later.
"""

import requests
import sys

from src.apps.app import Application


class HackerNews(Application):
    """Get top stories from Hacker News, and offer users the choice to save
    links to a file for later viewing.
    """

    # URL to get JSON data for a story. Append 'story_id.json' to the end.
    STORY_BASE = 'https://hacker-news.firebaseio.com/v0/item/'

    # Want to get JSON data for stories.
    JSON_ADD = '.json'

    # URL to get ID's of the top stories on HN.
    TOP_STORIES = 'https://hacker-news.firebaseio.com/v0/topstories.json'

    # When we have an Ask HN post, there is no URL in the JSON data, so instead
    # redirect users to the comment page for the question.
    ASK_HN = 'https://news.ycombinator.com/item?id='

    def __init__(self):
        """Initializes object. Sets fields to impossible values, because the
        user should call setup() upon instantiating the class.
        """
        super(HackerNews, self).__init__()
        self.url = ''
        self.max = -1
        self.file = ''

    def setup(self, *args, **kwargs):
        """Sets up URL base for getting stories from HN, as well as an optional
        maximum number of stories to get (defaults to 25).

        Arguments:
            kwargs {dict} -- specify properties of application.
                             url  -- url to query for stories.
                                     defaults to url for top stories
                             max  -- max number of stories to look through.
                                     defaults to 25
                             file -- file to write saved stories to.
                                     defaults to './hackernews.txt'
        """

        if 'url' in kwargs:
            self.url = kwargs.get('url')
        else:
            self.url = HackerNews.TOP_STORIES

        if 'max' in kwargs:
            if kwargs.get('max') <= 0:
                raise ValueError('Max stories must be greater than 0')
            self.max = kwargs.get('max')
        else:
            self.max = 25

        if 'file' in kwargs:
            self.file = kwargs.get('file')
        else:
            self.file = './hackernews.txt'

        with open(self.file, 'w') as out_file:
            out_file.truncate()
            out_file.close()

    def run(self, *args, **kwargs):
        """Runs the HackerNews application.
        Gets the top stories, and then goes through them one by one, asking the
        user if they want to save the link to the story for later.
        """

        top_stories = requests.get(url=self.url).json()

        for item in top_stories[0:self.max]:
            item_url = HackerNews.STORY_BASE + str(item) + HackerNews.JSON_ADD
            story = requests.get(url=item_url).json()
            print('Title: {}'.format(story.get('title')))
            print('URL: {}'.format(story.get('url')))
            sys.stdout.flush()

            flag = True      # Determines input validity.
            while flag:
                command = input('(s)ave for later, (q)uit, or (n)ext story?  ')
                if command == 's':
                    # Save story for later in a text file.
                    if 'url' in story:
                        self.save_link(story.get('title'), story.get('url'))
                    else:
                        # Only Ask HN posts have no URL in their JSON data.
                        self.save_link(story.get('title'), HackerNews.ASK_HN +
                                       str(item))
                    print('\n')
                    flag = False
                elif command == 'n':
                    # Move to the next story.
                    print('\n')
                    flag = False
                elif command == 'q':
                    # Quit application.
                    return
                else:
                    # Invalid input.
                    print('Invalid input. Please try again.')
                    continue

    def stop(self, *args, **kwargs):
        """Clean up any extraneous data we have.
        For this particular application, we don't have any loose ends to tie up,
        so the application can just terminate.
        """

        pass

    def is_setup(self):
        """Checks if the setup() method has been run yet.

        Returns:
            {bool} -- true if setup() has been run, false otherwise.
        """

        return (self.url != '') and (self.max != -1) and (self.file != '')

    def save_link(self, title, link):
        """Writes the title and the link to the object's 'file' field.

        Arguments:
            title {str} -- title of the story.
            link {str} -- link to the story.
        """

        if self.is_setup():
            with open(self.file, 'a+') as out_file:
                write_str = title + '\t' + link + '\n'
                out_file.write(write_str)
        else:
            raise ValueError('Run setup() before calling other functions.')


def main():
    """Integration test for the HackerNews application.
    Modify options in setup to see how the application responds.
    """

    hacker_news = HackerNews()
    hacker_news.setup(max=30)
    hacker_news.run()
    hacker_news.stop()

if __name__ == '__main__':
    main()
