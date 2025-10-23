from datetime import datetime

class StudySession:
    def __init__(self, title, group_name, time):
        self.title = title
        self.group_name = group_name
        self.time = time
        self.attendees = []

    def add_attendee(self, name):
        if name not in self.attendees:
            self.attendees.append(name)

    def remove_attendee(self, name):
        if name in self.attendees:
            self.attendees.remove(name)

    def get_summary(self):
        return {
            "title": self.title,
            "group": self.group_name,
            "time": self.time,
            "attendees": self.attendees
        }
