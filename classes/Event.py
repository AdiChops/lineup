from classes.Question import Question


class Event:
    def __init__(self, _id, _eventname, _host):
        self.id = _id
        self.eventName = _eventname
        self.host = _host
        self.queue = []

    def __str__(self):
        return f'{self.eventName} hosted by: {self.host.display_name}. ID: {self.id}'

    def enter_queue(self, user, topic):
        self.queue.append(Question(user, topic))

    def resolve(self):
        return self.queue.pop(0)

    def clear_queue(self):
        self.queue = []

    def move_user(self, old_pos, new_pos):
        user = queue[old_pos]
        queue.insert(new_pos, user)
        del queue[old_pos+1]