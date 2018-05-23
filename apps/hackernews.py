""" 
Application that allows the user to read Hacker News headlines and save any links they want to check out later.
"""

from app import Application

class HackerNews(Application):
    def setup(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

    def stop(self, *args, **kwargs):
        pass

def main():
    hn = HackerNews()
    hn.setup()
    hn.run()
    hn.stop()

if __name__ == '__main__':
    main()
    