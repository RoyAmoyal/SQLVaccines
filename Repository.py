import sqlite3
import atexit

from DAO import _Vaccines, _Suppliers, _Clinics, _Logistics
from DTO import *

DB_FILE_NAME = "database.db"


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect(DB_FILE_NAME)
        self._vaccines = _Vaccines(self._conn)
        self._suppliers = _Suppliers(self._conn)
        self._clinics = _Clinics(self._conn)
        self._logistics = _Logistics(self._conn)

    def _close(self):
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
        vac_num = data_arr[0]
        sup_num = data_arr[1]
        cli_num = data_arr[2]
        log_num = data_arr[3]

        i = 0  # do you mean i=1 because we want to avoid the first line?

        for line in init_lines:

            args = line.split(',')

            if i < vac_num:  # in this case we in the line of Vaccines
                vaccine = Vaccine(*args)
                self._vaccines.insert(vaccine)

            elif vac_num <= i < sup_num:  # in this case we in the line of supplier
                supplier = Supplier(*args)
                self._suppliers.insert(supplier)

            elif sup_num <= i < cli_num:  # in this case we in the line of clinics
                clinic = Clinic(*args)
                self._clinics.insert(clinic)

            else:  # in this case we in the line of logNum
                logistic = Logistic(*args)
                self._logistics.insert(logistic)

            i = i + 1

    def order_report(self):
        cursor = self._conn.cursor()
        cursor.execute("""SELECT sum
                            """)


repo = _Repository()

atexit.register(repo.close)
