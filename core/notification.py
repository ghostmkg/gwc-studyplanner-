class NotificationEngine:
    def send_reminder(self, session):
        print(f"Reminder: Study session '{session.title}' for group '{session.group_name}' is scheduled at {session.time}.")
