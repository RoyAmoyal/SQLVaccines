# DTOs
class Vaccine:
    def __init__(self, vaccine_id, date, supplier_id, quantity):
        self.id = vaccine_id
        self.date = date
        self.supplier_id = supplier_id  # we need to check if we need cast to int the id (int)supplier_id
        self.quantity = quantity


class Supplier:
    def __init__(self, supplier_id, name, logistic_id):
        self.id = supplier_id
        self.name = name
        self.logistic_id = int(logistic_id)


class Clinic:
    def __init__(self, clinic_id, location, demand, logistic_id):
        self.id = clinic_id
        self.location = location
        self.demand = demand
        self.logistic_id = int(logistic_id)


class Logistic:
    def __init__(self, logistic_id, name):
        self.id = logistic_id
        self.name = name
        self.count_sent = 0  # default value
        self.count_received = 0  # default value

