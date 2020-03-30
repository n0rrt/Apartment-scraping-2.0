import datetime
class Apartment():
    """
    class -> table
    attribute -> column
    instance -> row
    """
    def __init__(self, aptID, status):
        self.aptID = aptID
        self.status = status
        self.timestamp = datetime.datetime.utcnow()
    def __str__(self):
        return str(self.aptID)
    def getID(self):
        return self.aptID
    def getStatus(self):
        return self.status
    def getTimestamp(self):
        return self.timestamp
    def setStatus(self, status):
        self.status = status

class ApartmentProperty():
    """
    Same as Apartment class
    """
    def __init__(self, recordID, aptID, type, value):
        self.recordID = recordID
        self.aptID = aptID
        self.type = type
        self.value = value
    def __str__(self):
        return str(str(self.recordID) + " " + self.aptID + " " + self.type + " " + self.value)
    def getRecordID(self):
        return self.recordID
    def getAptID(self):
        return self.aptID
    def getType(self):
        return self.type
    def getValue(self):
        return self.value

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
