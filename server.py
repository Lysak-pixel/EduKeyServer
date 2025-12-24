import sqlite3
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session

# =========================
# Inicializácia Flask appky
# =========================
app = Flask(
    __name__,
    template_folder="templates/templates/template/templates"
)

# Tajný kľúč pre session
app.secret_key = '120202810428Jm!'

# Heslo na prístup k stránke s dátami
DATA_PAGE_PASSWORD = '120202810428Jm!'


# =========================
# Databáza
# =========================
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE
        );
    """)
    conn.commit()
    conn.close()


# =========================
# Pomocné funkcie
# =========================
def generate_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# =========================
# Routes
# =========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return redirect(url_for("index"))

    code = generate_code()

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO logins (username, password, code) VALUES (?, ?, ?)",
            (username, password, code)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "Chyba: kód už existuje"
    conn.close()

    return render_template("code.html", code=code)


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        password = request.form.get("password")
        if password == DATA_PAGE_PASSWORD:
            session["authorized"] = True
        else:
            return "Zlé heslo"

    if not session.get("authorized"):
        return redirect(url_for("index"))

    conn = get_db_connection()
    logins = conn.execute("SELECT * FROM logins").fetchall()
    conn.close()

    return render_template("data.html", logins=logins)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# =========================
# Spustenie aplikácie
# =========================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
