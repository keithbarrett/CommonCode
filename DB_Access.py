#! /usr/bin/env python

"""
DB_Access.py

Maintainer: Keith Barrett

Function for connecting to the database.
"""

import cx_Oracle


#
# Constants and Globals
#

#
# Functions and Methods
#


def connect_to_our_db(**kwargs):
    """Connect to the database. Every argument to this call is named and optional,
    as they will default to the R/O backup database or what's in a local config file.

    Comnon calls:
        x = connect_to_our_db(config='myconfig.ini')  # load from a configuation file.

        x = connect_to_our_db(user_id='xxx', user_pw='yyy')  # Use defaults and this user id/pw

    Parameters/Arguments:
        config='path/xxxx.zzz'
            First load parameter values from this configuation file before applying any of
            these other arguments. Defaults to "db.ini".

        db_server = 'xxx'
            Name or IP address of the database server.

        db_port = nnnnn
            The port number on the server to connect to.

        ora_sid = 'xxxx'
            The Oracle SID of the database.

        db_user_id = 'xxxx'
            The user ID to use when logging into the database.

        db_user_pw = 'xxxx'
            The password for this user ID.

    :return: cx_Oracle.connect() handle

    There are several ways to provide the information needed to connect to the database,
    and if you use multiple methods one will override the other. For every parameter except
    user ID and password, the function starts out with program defaults that will connect
    to the backup R/O database. If you use a configuration file (recommended), any
    values in it will override its default. Lastly, any values passed directly to this function
    call will override both. User ID and password are required to sucessfully connect, but
    the only way to pass them to this function is either in a configuration file or as an
    argument here. For security there are no hardcoded defaults for those two parameters.
    """

    DFLT_DB_SERVER = "my-database.com"
    DFLT_DB_PORT = 9999
    DFLT_DB_SID = "PRDDB"
    DFLT_CONFIG_FILE = 'db.ini'

    def load_keypair_file(config_file, force_lower=None):
        """Load data from a key pair configuration file. Blank lines, most whitespace and
        anything to the right of a '# ' are ignored):

        :param config_file: [Optional; can be ""] Config file to load. If none then the function just
        returns an empty dictionary.
        :type config_file: str
        :param force_lower: [Optional] Force keys to be lower case?
        :type force_lower: bool
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
                            if force_lower:
                                key = key.lower()
                            keypairs[key.strip()] = value.strip()
            except Exception:
                pass

        return keypairs

    def load_db_config(config_file=None):
        """Load data from a key pair configuration file, using defaults for anything not
        specified. File Format (Note: keynames are not case sensitive, anything to the
        right of a ' # ' is ignored):

        DB_SERVER = xxxx    # Name or IP address of the Oracle database server
        DB_PORT = nnnn      # IP port number to connect to
        DB_ORA_SID = xxxx   # Oracle dtabase SID
        DB_USER_ID = xxxx   # User ID for connection
        DB_USER_PW = xxxx   # Password for connection

        :param config_file: [Optional] File to load key pair values from.
        """

        my_param_list = {'db_server': DFLT_DB_SERVER, 'db_port': DFLT_DB_PORT, 'db_ora_sid': DFLT_DB_SID,
                         'db_user_id': '', 'db_user_pw': ''}
        # Start with default values

        my_config_file = DFLT_CONFIG_FILE

        if config_file:
            if config_file.strip() != "":
                my_config_file = config_file

        file_values = load_keypair_file(my_config_file, True)
        # load config file

        for key in my_param_list.keys():
            if key in file_values.keys():
                if file_values[key] != '':
                    my_param_list[key] = file_values[key]

            if key in kwargs.keys():
                if kwargs[key] != '':
                    my_param_list[key] = kwargs[key]

        return my_param_list

    #
    # Main connect_to_our_db() logic

    if 'config' in kwargs.keys():
        param_list = load_db_config(kwargs['config'])
    else:
        param_list = load_db_config()

    # Connect to Oracle Server
    oracle_dsn = cx_Oracle.makedsn(param_list['db_server'], int(param_list['db_port']), param_list['db_ora_sid'])

    # Connect to database
    return cx_Oracle.connect(param_list['db_user_id'], param_list['db_user_pw'], oracle_dsn)
    # TODO Needs try blocks

# END OF LINE
