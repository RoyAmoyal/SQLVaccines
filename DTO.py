# DTOs
class Vaccine:
    def __init__(self, vaccine_id, date, supplier_id, quantity):
        self.id = int(vaccine_id)
        self.date = date
        self.supplier_id = int(supplier_id)  # we need to check if we need cast to int the id (int)supplier_id
        self.quantity = int(quantity)


class Supplier:
    def __init__(self, supplier_id, name, logistic_id):
        self.id = int(supplier_id)
        self.name = name
        self.logistic_id = int(logistic_id)


class Clinic:
    def __init__(self, clinic_id, location, demand, logistic_id):
        self.id = int(clinic_id)
        self.location = location
        self.demand = int(demand)
        self.logistic_id = int(logistic_id)


class Logistic:
    def __init__(self, logistic_id, name, count_sent, count_received):
        self.id = int(logistic_id)
        self.name = name
        self.count_sent = int(count_sent)
        self.count_received = int(count_received)


