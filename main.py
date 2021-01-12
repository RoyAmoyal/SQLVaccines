

import sys

from Repository import *


def main(config_file, order_file, output_file):
    open(DB_FILE_NAME, 'w').close()  # clear the db file

    repo.create_tables()
    with open(config_file, "r") as f:
        first_line = f.readline()
        init_lines = f.readlines()
    repo.fill_tables(init_lines, first_line)

    with open(order_file, "r") as o:
        order_lines = o.readlines()
    repo.order_active(order_lines)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise ValueError("usage - main.py config.txt order.txt output.txt")
    main(sys.argv[1], sys.argv[2], sys.argv[3])


    # this method will be in repository
    def order_active(self, order_lines):
        for line in order_lines:
            args = line.split(',')    # we need to make sure that the split not ruin the line
            args = [arg.strip() for arg in args]
            if len(args) == 3 :
                recive_shipment(line)
            else:
                send_shipment(line)




