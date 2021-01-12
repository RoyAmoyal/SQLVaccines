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

        dataArr = first_line.split(',')
        dataArr = [arg.strip() for arg in dataArr]
        vacNum = dataArr[0]
        supNum = dataArr[1]
        cliNum = dataArr[2]
        logNum = dataArr[3]

        i = 0

        for line in init_lines:

            args = line.split(',')

            if i < vacNum:  # in this case we in the line of Vaccines
                vaccine = Vaccine(*args)
                self._vaccines.insert(vaccine)

            elif vacNum <= i < supNum:  # in this case we in the line of supplier
                supplier = Supplier(*args)
                self._suppliers.insert(supplier)

            elif supNum <= i < cliNum:  # in this case we in the line of clinics
                clinic = Clinic(*args)
                self._clinics.insert(clinic)

            else:  # in this case we in the line of logNum
                logistic = Logistic(*args)
                self._logistics.insert(logistic)

            i = i + 1


repo = _Repository()

atexit.register(repo.close)
