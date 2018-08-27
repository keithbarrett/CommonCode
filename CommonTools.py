#! /usr/bin/env python

"""
CommonTools.py

Maintainer: keibarre@cisco.com (Keith Barrett)

Collection of useful generic functions, constants and classes.

"""

import unicodedata
import os
import platform
import sys


#
# Constants and Globals
#

DEBUG_MODE = False


#
# Classes and Objects
#

class TextColor:
    """Escapes to display text in special formats and colors"""

    ON = ''
    VIOLET = '\033[95m'
    CYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[31m'   # Was 91

    UNDERLINE = '\033[4m'
#   BOLD = '\033[1m'       # Doesm't work in Windows PyCharm
#   ITALIC = '\033[3m'     # Doesn't work in Windows PyCharm
#   STRIKE = '\033[9m'     # Doesn't work in Windows PyCHarm

    WARN = YELLOW
    FAIL = RED
    INFO = GREEN
    OK = GREEN
    NOTE = CYAN
    ALERT = WARN
    ERROR = FAIL

    OFF = '\033[0m'


#
# Functions and Methods
#

def load_keypair_file(config_file):
    """Load data from a key pair configuration file. Keynames are treated as not case
    sensitive, blank lines, most whitespace and anything to the right of a '# ' are ignored):

    :param config_file: [Optional] Config file to load. If none then the function just
    returns an empty dictionary.
    :type config_file: str
    :return: dictionary of key and value
    """

    keypairs = {}

    if config_file and config_file.strip() != '':
        # noinspection PyBroadException
        try:
            with open(config_file) as myfile:
                for line in myfile:
                    curline = line.split('# ')[0].strip()
                    if (curline != '') and (curline != '#'):
                        key, value = curline.partition("=")[::2]
                        keypairs[key.strip()] = value.strip()

        except Exception:
            pass

    return keypairs


def input_is_redirected():
    """Is our input redirected from a file or pipe?"""

    def are_we_pycharm():
        """Are we running under PyCharm?"""
        return_status = False
        # noinspection PyBroadException
        try:
            if os.environ['PYCHARM_HOSTED'] == '1':
                return_status = True
        except Exception:
            pass
        return return_status

    if not sys.stdin.isatty() and not are_we_pycharm():
        # PyCharm fails sys.stdin.isatty() check, so we to check that also.
        return True
    else:
        return False


def DEBUG_LOG(log_line):
    """Simple function to display debug text depending on a debug mode setting.

    :param log_line: If True/False (bool) value, turns on/off debug mode. If (int) value,
        sets logging level to that value. All else gets logged as a string.
    :type log_line: String, Bool or Int
    :return: Always returns success
    """

    global DEBUG_MODE

    # If we don't get a string, then set our log level to the value
    if type(log_line).__name__ == 'bool':
        if log_line:
            DEBUG_MODE = 1
        else:
            DEBUG_MODE = 0
        return 0

    if type(log_line).__name__ == 'int':
        # TODO Add Support For logging levels
        if log_line > 0:
            DEBUG_MODE = True
        else:
            DEBUG_MODE = False
        return 0

    if type(log_line).__name__ != 'str':
        my_log_line = str(log_line)
    else:
        my_log_line = log_line + " "

    if (DEBUG_MODE > 0) and (len(my_log_line.strip()) > 0):
        if my_log_line[0] == '\n':
            print("\nDEBUG: " + my_log_line[1:])
        else:
            print("DEBUG: " + my_log_line)

    return 0


def user_id():
    """ Get your user id from the os, whether you are on windows or unix."""

    if platform.system() != 'Windows':
        # noinspection PyUnresolvedReferences
        return pwd.getpwuid(os.getuid()).pw_name
    else:
        # noinspection PyUnresolvedReferences
        return os.getenv('USERNAME')


def nocase_compare(item1, item2):
    """Case insensitive compare that tolerates foreign characters, unicode, non-strings and nulls"""

    if (item1 is not None) and (item2 is not None):
        if item1 == item2:  # This should work for any data types that are equal in content
            return True
        else:
            if type(item1).__name__ == 'str' and type(item2).__name__ == 'str':
                return unicodedata.normalize("NFKD", item1.casefold()) \
                       == unicodedata.normalize("NFKD", item2.casefold())
    return False


def clean_value(data_item, def_value):
    """Return a data item, or a default value if the data item is null or bad data

    :param data_item: Data item to check and return if OK
    :param def_value: Data to return if data_item is missing, invalid or null
    """

    if data_item is None:
        return def_value
    else:
        if data_item == 'No Match Row Id' or nocase_compare(data_item, 'null'):
            return def_value
        else:
            return data_item

#
# Rest of this file are clever items I've come across but haven't adopted (yet)
#

# def convert_tupple_to_str(data_item):
#     """ Clever trick to turn tupples into strings"""
#
#     if data_item is None:
#         return ''
#     else:
#         return ''.join(data_item)


# def find_values(id, obj):
#     results = []
#
#     def _find_values(id, obj):
#         try:
#             for key, value in obj.iteritems():
#                 if key == id:
#                     results.append(value)
#                 elif not isinstance(value, basestring):
#                     _find_values(id, value)
#         except AttributeError:
#             pass
#
#         try:
#             for item in obj:
#                 if not isinstance(item, basestring):
#                     _find_values(id, item)
#         except TypeError:
#             pass
#
#     if not isinstance(obj, basestring):
#         _find_values(id, obj)
#     return results


# # Cool function to flatten JSON by concatinating key fields in nested blocks
# def flattenjson( b, delim ):
#     val = {}
#     for i in b.keys():
#         if isinstance( b[i], dict ):
#             get = flattenjson( b[i], delim )
#             for j in get.keys():
#                 val[ i + delim + j ] = get[j]
#         else:
#             val[i] = b[i]
#
#     return val
