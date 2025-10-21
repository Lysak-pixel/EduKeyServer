from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from functools import wraps
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supertajnykluc123")

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    # Pridáme čas prijatia
    data['received_at'] = datetime.utcnow().isoformat() + "Z"
    
    # Uložíme dáta
    current_data = load_data()
    current_data.append(data)
    save_data(current_data)
    
    return jsonify({"status": "ok"}), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Prihlasovacie údaje zmenené podľa požiadavky
        if username == 'u-Admin' and password == '120202810428Jm!':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = "Nesprávne meno alebo heslo"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    data = load_data()
    # Najnovšie dáta hore
    data = sorted(data, key=lambda x: x.get('received_at', ''), reverse=True)
    return render_template('dashboard.html', data=data)
    # Ak chceš alternatívny dashboard, zmeň na:
    # return render_template('dashboard_alt.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)



