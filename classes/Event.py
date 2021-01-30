class Event:
    def __init__(self, _id, _eventname, _host):
        self.id = _id
        self.eventName = _eventname
        self.host = _host
        self.queue = []

    def __str__(self):
        return f'{self.eventName} hosted by: {self.host}. ID: {self.id}'