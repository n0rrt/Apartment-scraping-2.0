class City():
    def __init__(self, name, id):
        self._name = name
        self._id = id
    def __str__(self):
        return self._name.split('%')[0]
    def get_id(self):
        return self._id
    def get_name(self):
        return self._name
 