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
        cursor.execute("""CREATE TABLE Vaccines(id INTEGER PRIMARY KEY,
                                                    date DATE NOT NULL,
                                                    supplier INTEGER REFERENCES Supplier(id),  
                                                    quantity INTEGER REFERENCES Coffee_stands(id))
        """)

        cursor.execute("""CREATE TABLE Suppliers(id INTEGER PRIMARY KEY,
                                                          name STRING NOT NULL,
                                                          logistic INTEGER REFERENCES Logistic(id))
              """)
        cursor.execute("""CREATE TABLE Clinics(id INTEGER PRIMARY KEY,
                                                          location STRING NOT NULL,
                                                          demand INTEGER NOT NULL,
                                                          logistic INTEGER REFERENCES logistic(id))
              """)
        cursor.execute("""CREATE TABLE Logistics(id INTEGER PRIMARY KEY,
                                                              name STRING NOT NULL,
                                                              count_sent INTEGER NOT NULL,
                                                              count_received INTEGER NOT NULL)
              """)

    def fill_tables(self, init_lines, first_line):
        data_arr = first_line.split(',')
        data_arr = [arg.strip() for arg in data_arr]
        vac_num = data_arr[0]  # 3
        sup_num = data_arr[1]  # 2
        cli_num = data_arr[2]  # 1
        log_num = data_arr[3]  # 2
        sumNum = log_num + cli_num + sup_num + vac_num  # 8

        i = sumNum

        for line in reversed(init_lines):
            args = line.split(',')
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

    def order_report(self):
        cursor = self._conn.cursor()
        cursor.execute("""SELECT SUM(quantity),SUM(demand),SUM(total_received),SUM(total_sent)
                        FROM Vaccines,Clinics,Logistics,Logistics""")
        return cursor.fetchall()

    def received_shipment(self, args):
        name = args[0]
        amount = args[1]
        date = args[2]
        cursor = self._conn.cursor()
        cursor.execute("""SELECT id FROM Suppliers
        WHERE name = ?   """, [name])
        sup_id = cursor.fetchone()[0]
        cursor.execute(""" SELECT COUNT(id) FROM Vaccines""")
        vac_id = cursor.fetchone()[0]
        vaccine = Vaccine(vac_id, date, sup_id, amount)
        self._vaccines.insert(vaccine)  # inserting to the Vaccines
        cursor.execute("""SELECT logistic_id FROM Suppliers
                WHERE name = ?   """, [name])
        log_id = cursor.fetchone()[0]
        self._logistics.update_count_received(log_id, amount)  # update count_received

    def send_shipment(self, args):
        amount = args[1]
        cursor = self._conn.cursor()
        cursor.execute("""SELECT id FROM Clinics WHERE name = ?""", [args[0]])
        clinic_id = cursor.fetchone()[0]
        self._clinics.update_demand(clinic_id, amount)  # Updates the demand after the clinic got the vaccines
        cursor.execute("""SELECT logistic_id FROM Clinics WHERE id = ?""", [clinic_id])
        logistic_id = cursor.fetchone()[0]
        self._logistics.update_count_sent(logistic_id, amount)  # Updates the sent count of the logistic id
        cursor.execute("""SELECT * FROM Vaccines""")
        while amount > 0:
            curr_old_vaccines_stock = cursor.fetchone()  # The tupple of the first line on the vaccines table.
            curr_quantity = curr_old_vaccines_stock[4]
            if amount >= curr_quantity:
                amount = amount - curr_quantity
                self._vaccines.delete(curr_old_vaccines_stock[0])
            if amount < curr_quantity:
                self._vaccines.update_quantity(curr_old_vaccines_stock[0], amount)
                amount = 0


repo = _Repository()
atexit.register(repo.close)
