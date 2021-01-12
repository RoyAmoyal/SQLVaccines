class _Vaccines:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, vaccine):
        self._cursor.execute("""
                    INSERT INTO Vaccines (id, date, supplier_id, quantity) VALUES (?, ?, ?, ?)
                """, [vaccine.id, vaccine.date, vaccine.supplier_id, vaccine.quantity])

    def update(self, vaccine_id, quantity):
        self._cursor.execute("""UPDATE Vaccines SET quantity = quantity + ?
                WHERE id = ?""", [quantity, vaccine_id])

    def get_quantity(self, product_id):
        self._cursor.execute("""SELECT quantity FROM Vaccines
                       WHERE id = ?""", [product_id])
        return int(self._cursor.fetchone()[0])

    def fetch_table(self):
        self._cursor.execute("SELECT * FROM Vaccines ORDER BY Vaccines.id")
        all_data = self._cursor.fetchall()
        return all_data


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, supplier):
        self._cursor.execute("""
                INSERT INTO Suppliers (id, name, logistic) VALUES (?, ?, ?)
            """, [supplier.id, supplier.name, supplier.logistic])

    def fetch_table(self):
        self._cursor.execute("SELECT * FROM Suppliers ORDER BY Suppliers.id")
        all_data = self._cursor.fetchall()
        return all_data


class _Clinics:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, clinic):
        self._cursor.execute("""
                INSERT INTO Clinics (id, location, demand, logistic_id) VALUES (?, ?, ?, ?)
            """, [clinic.id, clinic.location, clinic.demand, clinic.logistic_id])

    def fetch_table(self):
        self._cursor.execute("SELECT * FROM Clinics ORDER BY Suppliers.id")
        all_data = self._cursor.fetchall()
        return all_data


class _Logistics:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, logistic):
        self._cursor.execute("""
                INSERT INTO Logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
            """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def fetch_table(self):
        self._cursor.execute("SELECT * FROM Logistics ORDER BY Suppliers.id")
        all_data = self._cursor.fetchall()
        return all_data

