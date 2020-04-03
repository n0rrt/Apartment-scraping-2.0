import datetime
class Apartment():
    """
    class -> table
    attribute -> column
    instance -> row
    """
    def __init__(self, apt_id, status):
        self._apt_id = apt_id
        self._status = status
        self._timestamp = datetime.datetime.utcnow()
    def __str__(self):
        return str(self._apt_id)
    def get_id(self):
        return self._apt_id
    def get_status(self):
        return self._status
    def get_timestamp(self):
        return self._timestamp
    def set_status(self, status):
        self._status = status

class ApartmentProperty():
    """
    Same as Apartment class
    """
    def __init__(self, record_id, apt_id, type, value):
        self._record_id = record_id
        self._apt_id = apt_id
        self._type = type
        self._value = value
    def __str__(self):
        return str(str(self._record_id) + " " + self._apt_id + " " + self._type + " " + self._value)
    def get_record_id(self):
        return self._record_id
    def get_apt_id(self):
        return self._apt_id
    def get_type(self):
        return self._type
    def get_value(self):
        return self._value

class PropertyType():
    def __init__(self, id, name, data):
        self.id = id
        self.name = name
        self.data = data
    def __str__(self):
        return str(self.id) + self.name
    def getID(self):
        return self.id
    def getName(self):
        return self.name
    def getData(self):
        return self.data
