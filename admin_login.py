from flask import Blueprint, render_template, request, redirect, url_for, session
import requests

admin_bp = Blueprint('admin', __name__)

# ---------------- JSONBIN CONFIG ----------------
JSONBIN_API_KEY = "$2a$10$R74G8pPzaRy0kLrcmfIYO.jvMl0T8JA3XQVaRHQNqYWsyO8ltxLr."
BIN_ID = "68fef25a43b1c97be983b22f"

HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": JSONBIN_API_KEY
}

# ---------------- JSONBIN FUNCTION ----------------
def load_admin():
    """Fetch admin credentials from JSONBin"""
    try:
        res = requests.get(f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest", headers=HEADERS)
        if res.status_code == 200:
            data = res.json().get("record", {})
            return data.get("admin", {})
        else:
            print("Error loading admin:", res.status_code, res.text)
    except Exception as e:
        print("JSONBin Error:", e)
    return {}

# ---------------- ROUTES ----------------
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("logged_in"):
        return redirect(url_for("home"))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin_data = load_admin()
        admin_username = admin_data.get("username")
        admin_password = admin_data.get("password")

        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('admin.login'))
