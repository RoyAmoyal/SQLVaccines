import sqlite3
import atexit

from DAO import _Vaccines, _Suppliers, _Clinics, _Logistics
from DTO import *


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect("database.db")
        self._vaccines = _Vaccines(self._conn)
        self._suppliers = _Suppliers(self._conn)
        self._clinics = _Clinics(self._conn)
        self._logistics = _Logistics(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        cursor = self._conn.cursor()
        cursor.execute("""CREATE TABLE vaccines(id INTEGER PRIMARY KEY,
                                                    date DATE NOT NULL,
                                                    supplier INTEGER REFERENCES supplier(id),  
                                                    quantity INTEGER NOT NULL)
        """)

        cursor.execute("""CREATE TABLE suppliers(id INTEGER PRIMARY KEY,
                                                          name STRING NOT NULL,
                                                          logistic INTEGER REFERENCES logistic(id))
              """)
        cursor.execute("""CREATE TABLE clinics(id INTEGER PRIMARY KEY,
                                                          location STRING NOT NULL,
                                                          demand INTEGER NOT NULL,
                                                          logistic INTEGER REFERENCES logistic(id))
              """)
        cursor.execute("""CREATE TABLE logistics(id INTEGER PRIMARY KEY,
                                                              name STRING NOT NULL,
                                                              count_sent INTEGER NOT NULL,
                                                              count_received INTEGER NOT NULL)
              """)

    def fill_tables(self, init_lines, first_line):
        data_arr = first_line.split(',')
        data_arr = [arg.strip() for arg in data_arr]
        vac_num = int(data_arr[0])  # 3
        sup_num = int(data_arr[1])  # 2
        cli_num = int(data_arr[2])  # 1
        log_num = int(data_arr[3])  # 2
        sumNum = log_num + cli_num + sup_num + vac_num  # 8
        currNum = sumNum
        i = sumNum

        for line in init_lines[sumNum - log_num:]:
            args = line.split(',')  #
            logistic = Logistic(*args)
            self._logistics.insert(logistic)

        currNum = currNum-log_num
        for line in init_lines[currNum - cli_num :currNum]:
            args = line.split(',')  #
            clinic = Clinic(*args)
            self._clinics.insert(clinic)

        currNum = currNum-cli_num
        for line in init_lines[currNum - sup_num :currNum]:
            args = line.split(',')  #
            supplier = Supplier(*args)
            self._suppliers.insert(supplier)

        currNum = currNum-sup_num
        for line in init_lines[currNum - vac_num :currNum]:
            args = line.split(',')
            vaccine = Vaccine(*args)
            self._vaccines.insert(vaccine)


    """    for line in reversed(init_lines):
            args = line.split(',')   #
            if i <= vac_num:  # in this case we in the line of Vaccines
                vaccine = Vaccine(*args)
                self._vaccines.insert(vaccine)

            elif vac_num < i <= (sup_num + vac_num):  # in this case we in the line of supplier
                supplier = Supplier(*args)
                self._suppliers.insert(supplier)

            elif (sup_num + vac_num) < i <= (sumNum - log_num):  # in this case we in the line of clinics
                clinic = Clinic(*args)
                self._clinics.insert(clinic)

            else:  # in this case we in the line of logNum
                logistic = Logistic(*args)
                self._logistics.insert(logistic)

            i = i - 1
             """
    def order_report(self):  # ),SUM(demand),SUM(count_received)
        cursor = self._conn.cursor()
        cursor.execute("""SELECT SUM(quantity) FROM vaccines""")
        quantity_tuple = cursor.fetchall()[0]
        quantity_str = "".join(map(str, quantity_tuple))
        cursor.execute("""SELECT SUM(demand) FROM clinics""")
        demand_tuple = cursor.fetchall()[0]
        demand_str = "".join(map(str, demand_tuple))
        cursor.execute("""SELECT SUM(count_received) FROM logistics""")
        count_received_tuple = cursor.fetchall()[0]
        count_received_str = "".join(map(str, count_received_tuple))
        cursor.execute("""SELECT SUM(count_sent) FROM logistics""")
        count_sent_tuple = cursor.fetchall()[0]
        count_sent_str = "".join(map(str, count_sent_tuple))
        str_report = quantity_str + "," + demand_str + "," + count_received_str + "," + count_sent_str
        return str_report

    def received_shipment(self, args):
        name = args[0]
        amount = args[1]
        date = args[2]
        cursor = self._conn.cursor()
        cursor.execute("""SELECT id FROM suppliers
        WHERE name = ?   """, [name])
        sup_id = cursor.fetchone()[0]
        cursor.execute(""" SELECT COUNT(id) FROM vaccines""")
        vac_id = cursor.fetchone()[0]
        vaccine = Vaccine(vac_id, date, sup_id, amount)
        self._vaccines.insert(vaccine)  # inserting to the Vaccines
        cursor.execute("""SELECT logistic FROM suppliers
                WHERE name = ?   """, [name])
        log_id = cursor.fetchone()[0]
        self._logistics.update_count_received(log_id, amount)  # update count_received

    def send_shipment(self, args):
        amount = args[1]
        cursor = self._conn.cursor()
        cursor.execute("""SELECT id FROM clinics WHERE location = ?""", [args[0]])
        clinic_id = cursor.fetchone()[0]
        self._clinics.update_demand(clinic_id, amount)  # Updates the demand after the clinic got the vaccines
        cursor.execute("""SELECT logistic FROM clinics WHERE id = ?""", [clinic_id])
        logistic_id = cursor.fetchone()[0]
        self._logistics.update_count_sent(logistic_id, amount)  # Updates the sent count of the logistic id
        cursor.execute("""SELECT * FROM vaccines""")
        int_amount = int(amount)
        while int_amount > 0:
            curr_old_vaccines_stock = cursor.fetchone()  # The tupple of the first line on the vaccines table.
            curr_quantity = int(curr_old_vaccines_stock[3])
            if int_amount >= curr_quantity:
                int_amount = int_amount - curr_quantity
                self._vaccines.delete(curr_old_vaccines_stock[0])
            elif int_amount < curr_quantity:
                self._vaccines.update_quantity(curr_old_vaccines_stock[0], int_amount)
                int_amount = 0


repo = _Repository()
atexit.register(repo.close)
