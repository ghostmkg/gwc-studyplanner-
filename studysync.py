import datetime
import time

# -------------------------------
# 📌 StudySync - Group Study Scheduler
# -------------------------------

class StudySession:
    def __init__(self, topic, date_time, duration):
        self.topic = topic
        self.date_time = date_time
        self.duration = duration
        self.attendees = []

    def add_attendee(self, name):
        self.attendees.append(name)

    def __str__(self):
        return f"{self.topic} | {self.date_time.strftime('%Y-%m-%d %H:%M')} | Duration: {self.duration} hrs | Attendees: {len(self.attendees)}"


class StudyGroup:
    def __init__(self, group_name):
        self.group_name = group_name
        self.sessions = []

    def create_session(self, topic, date_time, duration):
        session = StudySession(topic, date_time, duration)
        self.sessions.append(session)
        print(f"✅ Session '{topic}' scheduled on {date_time.strftime('%Y-%m-%d %H:%M')}")
        return session

    def list_sessions(self):
        print(f"\n📚 Study Sessions for Group: {self.group_name}")
        for i, session in enumerate(self.sessions, start=1):
            print(f"{i}. {session}")

    def send_reminders(self):
        now = datetime.datetime.now()
        print("\n🔔 Checking for upcoming sessions...")
        for session in self.sessions:
            if 0 <= (session.date_time - now).total_seconds() <= 3600:
                print(f"⏰ Reminder: '{session.topic}' starts at {session.date_time.strftime('%H:%M')}!")


# -------------------------------
# 🧭 Main Program
# -------------------------------
def main():
    print("🎓 Welcome to StudySync - Group Study Scheduler")

    group_name = input("Enter group name: ")
    group = StudyGroup(group_name)

    while True:
        print("\n--- MENU ---")
        print("1. Create Study Session")
        print("2. Add Attendee")
        print("3. View Sessions")
        print("4. Send Reminders")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            topic = input("Enter session topic: ")
            date_str = input("Enter date and time (YYYY-MM-DD HH:MM): ")
            duration = float(input("Enter duration (in hours): "))
            date_time = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            group.create_session(topic, date_time, duration)

        elif choice == "2":
            group.list_sessions()
            try:
                index = int(input("Select session number: ")) - 1
                attendee = input("Enter attendee name: ")
                group.sessions[index].add_attendee(attendee)
                print(f"👥 {attendee} added to '{group.sessions[index].topic}'")
            except (IndexError, ValueError):
                print("❌ Invalid selection!")

        elif choice == "3":
            group.list_sessions()

        elif choice == "4":
            group.send_reminders()

        elif choice == "5":
            print("👋 Exiting StudySync. Happy Studying!")
            break

        else:
            print("❌ Invalid choice! Try again.")

        time.sleep(1)


if __name__ == "__main__":
    main()
