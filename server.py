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
    print("Received data:", json_data)  # pridaj log, aby si videl čo prichádza
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
        <form method="post" style="background:#000;color:#33ff33;padding:1rem;font-family: monospace; max-width:300px; margin:auto; margin-top:5rem;">
            Heslo: <input type="password" name="password" required style="background:#000;color:#33ff33; border: 1px solid #33ff33; padding:0.5rem; font-family: monospace;">
            <input type="submit" value="Prihlásiť sa" style="background:#33ff33;color:#000; border:none; padding:0.5rem 1rem; cursor:pointer; font-weight:bold;">
        </form>
    '''

@app.route('/logout')
def logout():
    return redirect('/admin')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






