

import sys

from Repository import *


def main(config_file):
    open(DB_FILE_NAME, 'w').close()  # clear the db file

    repo.create_tables()
    with open(config_file, "r") as f:
        first_line = f.readline()
        init_lines = f.readlines()
    repo.fill_tables(init_lines, first_line)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("usage - initiate.py config.txt")
    main(sys.argv[1])