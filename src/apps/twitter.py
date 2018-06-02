"""
Application that allows the user to view tweets from their timeline.
"""

from src.apps.app import Application

class Twitter(Application):
    def setup(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        print('Running Twitter app')
    
    def stop(self, *args, **kwargs):
        pass

def main():
    Twitter()

if __name__ == '__main__':
    main()
    
