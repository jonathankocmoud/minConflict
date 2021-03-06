"""This file includes basic utility functions and files"""
import inspect
import sys
from itertools import cycle

class bcolors:
    """
    Produce colorful outputs
    usage:
            print bcolors.BOLD + 'BOLD' + 'bcolors.ENDC
    Works ONLY on *nix systems
    """
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def raiseNotDefined():
    """A helper function which helpts to exits gracefully if method is undefined."""

    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print "*** Method not implemented: %s at line %s of %s" % (method, line, fileName)
    sys.exit(0)
