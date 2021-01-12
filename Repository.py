import sqlite3

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
                                                    coffee_stand INTEGER REFERENCES Coffee_stands(id))
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

