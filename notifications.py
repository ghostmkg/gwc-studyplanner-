from utils import format_datetime, schedule_reminder
from datetime import datetime
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()  # loads variables from .env file

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# ---------------------------
# Email Sending Function
# ---------------------------
def send_email_reminder(user_email: str, topic: str, session_time: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = user_email
        msg["Subject"] = f"StudySync Reminder: {topic}"

        body = (
            f"Hello!\n\nThis is a reminder for your upcoming study session:\n\n"
            f"Topic: {topic}\nTime: {session_time}\n\nHappy Studying!\n\n- StudySync"
        )
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, user_email, msg.as_string())
        server.quit()
        print(f"[EMAIL SENT] Reminder sent to {user_email} for '{topic}' at {session_time}")
    except Exception as e:
        print(f"[EMAIL ERROR] Could not send to {user_email}. Error: {e}")

# ---------------------------
# Schedule Reminder
# ---------------------------
def schedule_session_reminder(user_email: str, topic: str, session_time: datetime, reminder_minutes: int = 30):
    reminder_time = schedule_reminder(session_time, reminder_minutes)
    delay = (reminder_time - datetime.now()).total_seconds()

    if delay <= 0:
        # Send immediately if within reminder window
        send_email_reminder(user_email, topic, format_datetime(session_time))
        return

    threading.Timer(delay, send_email_reminder, args=[user_email, topic, format_datetime(session_time)]).start()
