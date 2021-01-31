from classes.Question import Question


class Event:
    def __init__(self, _id, _eventname, _host):
        self.id = _id
        self.eventName = _eventname
        self.host = _host
        self.queue = []
        self.user_frequency = {}

    def __str__(self):
        return f'{self.eventName} hosted by: {self.host.display_name}. ID: {self.id}'

    def check_user_frequency(self, user):
        return user in self.user_frequency and self.user_frequency[user] == 5

    def enter_queue(self, user, topic):
        if self.check_user_frequency(user):
            return False
        self.queue.append(Question(user, topic))
        self.increase_user_frequency(user)
        return True

    def leave_queue(self, user, question_id):
        for users in self.queue:
            if user.display_name == users.author.display_name and question_id != -1:
                self.queue.pop(question_id)

    def resolve(self, question_index):
        self.decrease_user_frequency(self.queue[question_index].author)
        return self.queue.pop(question_index - 1)

    def currently_served(self):
        return self.queue[0].author

    def clear_queue(self):
        self.queue = []

    def move_user(self, old_pos, new_pos):
        topic = self.queue[old_pos]
        del self.queue[old_pos]
        self.queue.insert(new_pos, topic)

    def increase_user_frequency(self, user):
        if user not in self.user_frequency:
            self.user_frequency[user] = 0
        self.user_frequency[user] += 1

    def decrease_user_frequency(self, user):
        self.user_frequency[user] -= 1

    def get_question_at(self, index):
        return self.queue[index]
