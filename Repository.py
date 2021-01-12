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


