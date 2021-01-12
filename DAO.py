class _Vaccines:
    def __init__(self,conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, vaccine):
