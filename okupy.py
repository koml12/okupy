#!/usr/bin/env python

import sys
from utils.times import str_to_secs, TimeThread

def main():
    if len(sys.argv) != 2:
        # Invalid invocation.
        print('Error: Usage is ./okupy <time>')
        sys.exit(1)

    secs = str_to_secs(sys.argv[1])
    
    if (secs == -1):
        # Invalid time input.
        print('Invalid time input. Suffixes of \'s\', \'m\', or \'h\' are allowed.')
        sys.exit(1)
    
    time_thread = TimeThread(secs)
    time_thread.run()

if __name__ == '__main__':
    main()