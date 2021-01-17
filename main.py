import sys

from Repository import *


def main(config_file, order_file, output_file):
    open("database.db", 'w').close()  # clear the db file
    open('output.txt', 'w').close() # clear the output file
    repo.create_tables()
    with open(config_file, "r") as f:
        all_lines = f.read().splitlines()
        first_line = all_lines[0]
        init_lines = all_lines[1:]
    repo.fill_tables(init_lines, first_line)

    with open(order_file, "r") as o:
        order_lines = o.read().splitlines()
        with open(output_file, "a") as q:
            for line in order_lines:
                args = line.split(',')  # we need to make sure that the split not ruin the line
                args = [arg.strip() for arg in args]
                if len(args) == 3:
                    repo.received_shipment(args)
                    curr_report = repo.order_report()
                else:
                    repo.send_shipment(args)
                    curr_report = repo.order_report()
                if line is not order_lines[-1]:
                    q.write(curr_report + "\n")
                else:
                    q.write(curr_report)
            q.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise ValueError("usage - main.py config.txt orders.txt output.txt")
    main(sys.argv[1], sys.argv[2], sys.argv[3])
