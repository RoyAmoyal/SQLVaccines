class _Vaccines:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, vaccine):
        self._cursor.execute("""
                    INSERT INTO Vaccines (id, date, supplier_id, quantity) VALUES (?, ?, ?, ?)
                """, [vaccine.id, vaccine.date, vaccine.supplier_id, vaccine.quantity])

    """If an order request has been set, 
    we update the quantity and then check with get quantity if quantity==0. if we do we remove him from the table"""

    def update_quantity(self, vaccine_id, amount):
        self._cursor.execute("""UPDATE Vaccines SET quantity = quantity - ?
                WHERE id = ?""", [amount, vaccine_id])

    def get_quantity(self, vaccine_id):
        self._cursor.execute("""SELECT quantity FROM Vaccines
                       WHERE id = ?""", [vaccine_id])
        return int(self._cursor.fetchone()[0])

    def delete(self, vaccine_id):
        self._cursor.execute("""
                    DELETE FROM Vaccines WHERE id = ?""", [vaccine_id])

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

    def update_demand(self, clinic_id, amount):
        self._cursor.execute("""UPDATE Vaccines SET demand = demand - ?
                                WHERE id = ?""", [amount, clinic_id])

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

    def update_count_sent(self, logistic_id, amount):
        self._cursor.execute("""UPDATE Logistics SET count_sent = count_sent + ?
                                WHERE id = ?""", [amount, logistic_id])

    def update_count_received(self, logistic_id, amount):
        self._cursor.execute("""UPDATE Logistics SET count_received = count_received + ?
                                WHERE id = ?""", [amount, logistic_id])

    def fetch_table(self):
        self._cursor.execute("SELECT * FROM Logistics ORDER BY Suppliers.id")
        all_data = self._cursor.fetchall()
        return all_data
