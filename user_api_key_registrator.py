#!/usr/bin/env python3
import argparse
import sqlite3
import sys

from db_services import re_initialize_db, register_new_api_key, get_user_api_keys

from config import USERS_API_KEYS_DB_FILE


def main(args):
    with sqlite3.connect(USERS_API_KEYS_DB_FILE) as db_connection:
        if not (args.list or args.register):
            parser.print_usage(sys.stderr)
            print("error: You must provide at least one argument", file=sys.stderr)
            sys.exit(1)

        re_initialize_db(db_connection)

        if args.list:
            # List user keys
            for key in get_user_api_keys(db_connection):
                print(key)

        if args.register:
            # Register new user and generate a 32-character key
            key = register_new_api_key(db_connection)
            print('New user registered with key:', key)


if __name__ == "__main__":
    # Define the argparse parser object
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('--list', action='store_true', help='List user keys')
    parser.add_argument('--register', action='store_true', help='Register new user')

    # Parse the command line arguments
    args = parser.parse_args()

    main(args)

# Note. In the future, some functionality might be added, in order to
# show messages history by provided user key, or whatever. But for now that's not the case.
