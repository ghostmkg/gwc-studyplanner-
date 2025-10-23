from core.session import StudySession
from core.notification import NotificationEngine
from core.storage import load_sessions, save_sessions

def main():
    sessions = load_sessions()
    notification = NotificationEngine()

    print("Welcome to StudySync CLI!")
    print("1. Create Session\n2. List Sessions\n3. Send Reminders")
    choice = input("Choose an option: ")

    if choice == "1":
        title = input("Session Title: ")
        group = input("Group Name: ")
        time = input("Time (YYYY-MM-DD HH:MM): ")
        session = StudySession(title, group, time)
        sessions.append(session.get_summary())
        save_sessions(sessions)
        print("Session created successfully!")

    elif choice == "2":
        if not sessions:
            print("No sessions available.")
        for s in sessions:
            print(s)

    elif choice == "3":
        for s in sessions:
            notification.send_reminder(StudySession(s["title"], s["group"], s["time"]))

if __name__ == "__main__":
    main()
