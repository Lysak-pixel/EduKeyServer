import sqlite3
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session

# Inicializácia Flask aplikácie
app = Flask(__name__)
# Nastav tajný kľúč pre session, v reálnom projekte by mal byť komplexný a utajený
app.secret_key = 'super_tajny_kluc_vzdelavacie_projekt' 

# Heslo na prístup k stránke s dátami
DATA_PAGE_PASSWORD = 'mojetajneheslo123'

def get_db_connection():
    """Vytvorí pripojenie k SQLite databáze."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializuje databázu a vytvorí tabuľku, ak ešte neexistuje."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE
        );
    ''')
    conn.commit()
    conn.close()

def generate_code(length=6):
    """Vy
