""" times.py
"""

import threading
import time

def str_to_secs(timestr):
    """Converts a time string (i.e. 30s) to a number of seconds (i.e. 30)

    Arguments:
        timestr {str} -- string representation of the time. Allows suffixes of 's',                  'm', or 'h'
    Returns:
        {int} -- number of seconds given by the time string input.
    """
    l = len(timestr)

    if not timestr[0:l-1].isdigit() and l > 1:
        # Check if there are any letters before the last char in the input.
        # If length is 1, then we're checking the empty string, so we have to
        # skip that case.
        return -1    

    if not timestr[l - 1].isalpha():
        # Default with no suffix is seconds.
        return int(timestr)
    elif timestr[l - 1] == 's':
        # Suffix of 's' means seconds
        return int(timestr[0:l-1])
    elif timestr[l - 1] == 'm':
        # Suffix of 'm' means minutes, so multiply by 60.
        return int(timestr[0:l-1]) * 60
    elif timestr[l - 1] == 'h':
        # Suffix of 'h' means hour, so multiply by 60*60
        return int(timestr[0:l-1]) * 360
    else:
        return -1
    

class TimeThread(threading.Thread):
    """ Class that maintains a threaded timer over a set number of seconds.
    """

    def __init__(self, secs):
        """ Initializes the thread with a specified duration in seconds.
        
        Arguments:
            secs {int} -- number of seconds the thread should run for.
        """
        threading.Thread.__init__(self)
        if secs < 0:
            raise ValueError('Input time cannot be negative.')

        self.secs = secs

    def run(self):
        """ Runs the thread for the passed in number of seconds.
        """
        t_now = int(time.time())

        while True:
            t_then = int(time.time())
            if t_then - t_now == self.secs:
                break


def main():
    timestr = '0'
    t = str_to_secs(timestr)
    print(t)
    thread = TimeThread(t)
    t_start = time.time()
    thread.start()
    thread.join()
    t_end = time.time()
    print('done')
    print(t_end - t_start)
    

if __name__ == '__main__':
    main()
    