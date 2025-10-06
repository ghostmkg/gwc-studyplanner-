import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load .env for email credentials
load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

# ---------------------------
# 1️⃣ Create a Group with unique name
# ---------------------------
unique_name = datetime.now().strftime("%Y%m%d%H%M%S")
group_data = {"name": f"Math Study Group {unique_name}"}
resp = requests.post(f"{BASE_URL}/groups/", json=group_data)
group = resp.json()
print("Created Group:", group)

# ---------------------------
# 2️⃣ Add Users
# ---------------------------
users = [
    {"name": "Krushnali", "email": "mungekarkrushnali7@gmail.com", "group_id": group["id"]},
    {"name": "Rupali", "email": "mungekarkrushnali@gmail.com", "group_id": group["id"]}
]


created_users = []
for user in users:
    resp = requests.post(f"{BASE_URL}/users/", json=user)
    created_user = resp.json()
    created_users.append(created_user)
    print("Created User:", created_user)

# ---------------------------
# 3️⃣ Create a Study Session (2 minutes in the future for testing)
# ---------------------------
session_time = datetime.now() + timedelta(minutes=2)
session_data = {
    "topic": "Calculus Exam Prep",
    "scheduled_time": session_time.isoformat(),
    "group_id": group["id"]
}
resp = requests.post(f"{BASE_URL}/sessions/", json=session_data)
session = resp.json()
print("Created Session:", session)

# ---------------------------
# 4️⃣ Mark Attendance for Krushnali
# ---------------------------
attendance_data = {
    "user_id": created_users[0]["id"],
    "session_id": session["id"],
    "present": True
}
resp = requests.put(f"{BASE_URL}/attendance/", json=attendance_data)
print("Updated Attendance:", resp.json())

print("\n✅ Test complete. Emails will be sent shortly. Check your inboxes!")
