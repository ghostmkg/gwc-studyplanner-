from flask import Flask, request, jsonify
from core.session import StudySession
from core.storage import load_sessions, save_sessions

app = Flask(__name__)
sessions = load_sessions()

@app.route("/create_session", methods=["POST"])
def create_session():
    data = request.json
    session = StudySession(data["title"], data["group_name"], data["time"])
    sessions.append(session.get_summary())
    save_sessions(sessions)
    return jsonify({"message": "Session created successfully!", "session": session.get_summary()})

@app.route("/list_sessions", methods=["GET"])
def list_sessions():
    return jsonify(sessions)

if __name__ == "__main__":
    app.run(debug=True)
