class _Vaccines:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, vaccine):
        self._cursor.execute("""
                    INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
                """, [vaccine.id, vaccine.date, vaccine.supplier_id, vaccine.quantity])

    """If an order request has been set, 
    we update the quantity and then check with get quantity if quantity==0. if we do we remove him from the table"""

    def update_quantity(self, vaccine_id, amount):
        self._cursor.execute("""UPDATE vaccines SET quantity = quantity - ?
                WHERE id = ?""", [amount, vaccine_id])

    def get_quantity(self, vaccine_id):
        self._cursor.execute("""SELECT quantity FROM vaccines
                       WHERE id = ?""", [vaccine_id])
        return int(self._cursor.fetchone()[0])

    def delete(self, vaccine_id):
        self._cursor.execute("""
                    DELETE FROM vaccines WHERE id = ?""", [vaccine_id])

    def fetch_table(self):
        self._cursor.execute("SELECT * FROM vaccines ORDER BY vaccines.id")
        all_data = self._cursor.fetchall()
        return all_data


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, supplier):
        self._cursor.execute("""
                INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
            """, [supplier.id, supplier.name, supplier.logistic_id])

    def fetch_table(self):
        self._cursor.execute("SELECT * FROM suppliers ORDER BY suppliers.id")
        all_data = self._cursor.fetchall()
        return all_data


class _Clinics:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, clinic):
        self._cursor.execute("""
                INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
            """, [clinic.id, clinic.location, clinic.demand, clinic.logistic_id])

    def update_demand(self, clinic_id, amount):
        self._cursor.execute("""UPDATE clinics SET demand = demand - ?
                                WHERE id = ?""", [amount, clinic_id])

    def fetch_table(self):
        self._cursor.execute("SELECT * FROM clinics ORDER BY suppliers.id")
        all_data = self._cursor.fetchall()
        return all_data


class _Logistics:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def insert(self, logistic):
        self._cursor.execute("""
                INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
            """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def update_count_sent(self, logistic_id, amount):
        self._cursor.execute("""UPDATE logistics SET count_sent = count_sent + ?
                                WHERE id = ?""", [amount, logistic_id])

    def update_count_received(self, logistic_id, amount):
        self._cursor.execute("""UPDATE logistics SET count_received = count_received + ?
                                WHERE id = ?""", [amount, logistic_id])

    def fetch_table(self):
        self._cursor.execute("SELECT * FROM logistics ORDER BY suppliers.id")
        all_data = self._cursor.fetchall()
        return all_data
