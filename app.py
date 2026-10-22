# app.py
import os
import sqlite3
from datetime import datetime, timezone
from flask import (
    Flask, request, g, render_template, redirect, url_for,
    session, jsonify, send_from_directory, flash
)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

load_dotenv()  # optional .env for configs

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'reports.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret')

# ---------- DB helpers ----------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_conn(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    return cur.lastrowid

# ---------- Authentication ----------
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login', next=request.path))
        return f(*args, **kwargs)
    return wrapper

# ---------- Public Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

# API: return approved reports as JSON (filters supported)
@app.route('/api/reports')
def api_reports():
    # filters: category, search, start_date, end_date
    params = []
    q = "SELECT * FROM reports WHERE status = 'approved'"
    category = request.args.get('category')
    search = request.args.get('search')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if category:
        q += " AND LOWER(category) = LOWER(?)"
        params.append(category)
    if search:
        q += " AND (LOWER(title) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?))"
        s = f"%{search}%"
        params.extend([s, s])
    if start_date:
        q += " AND date_reported >= ?"
        params.append(start_date + "T00:00:00")
    if end_date:
        q += " AND date_reported <= ?"
        params.append(end_date + "T23:59:59")

    q += " ORDER BY date_reported DESC"
    rows = query_db(q, params)
    results = [dict(r) for r in rows]
    return jsonify(results)

# API: submit report (accepts multipart/form-data so file upload works)
@app.route('/api/report', methods=['POST'])
def api_report():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    latitude = request.form.get('latitude') or None
    longitude = request.form.get('longitude') or None
    category = request.form.get('category') or None
    image = request.files.get('image')

    image_path = None
    if image and image.filename:
        filename = secure_filename(image.filename)
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        if ext in ALLOWED_EXT:
            unique = f"{int(datetime.now().timestamp())}_{filename}"
            dest = os.path.join(app.config['UPLOAD_FOLDER'], unique)
            image.save(dest)
            image_path = unique

    date_reported = datetime.now(timezone.utc).isoformat()
    execute_db(
        "INSERT INTO reports (title, description, latitude, longitude, category, date_reported, status, image_path) "
        "VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)",
        (title, description, latitude, longitude, category, date_reported, image_path)
    )
    return jsonify({"status":"ok","message":"Report submitted and pending approval"}), 201

# serve uploaded images
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ---------- Admin UI ----------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        row = query_db("SELECT * FROM admins WHERE username = ?", (username,), one=True)
        if row and check_password_hash(row['password_hash'], password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # show all reports (pending + approved)
    rows = query_db("SELECT * FROM reports ORDER BY date_reported DESC")
    reports = [dict(r) for r in rows]
    return render_template('admin_dashboard.html', reports=reports, admin=session.get('admin_username'))

# Admin actions: approve and delete (AJAX endpoints)
@app.route('/admin/approve/<int:report_id>', methods=['POST'])
@admin_required
def admin_approve(report_id):
    r = query_db("SELECT * FROM reports WHERE id = ?", (report_id,), one=True)
    if not r:
        return jsonify({"status":"error","message":"not found"}), 404
    execute_db("UPDATE reports SET status = 'approved' WHERE id = ?", (report_id,))
    return jsonify({"status":"ok"})

@app.route('/admin/delete/<int:report_id>', methods=['POST'])
@admin_required
def admin_delete(report_id):
    r = query_db("SELECT * FROM reports WHERE id = ?", (report_id,), one=True)
    if not r:
        return jsonify({"status":"error","message":"not found"}), 404
    # delete image file if exists
    image = r['image_path']
    if image:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image))
        except Exception:
            pass
    execute_db("DELETE FROM reports WHERE id = ?", (report_id,))
    return jsonify({"status":"ok"})

# small API for admin to list pending reports (optional)
@app.route('/admin/api/pending')
@admin_required
def admin_api_pending():
    rows = query_db("SELECT * FROM reports WHERE status = 'pending' ORDER BY date_reported DESC")
    return jsonify([dict(r) for r in rows])

# ---------- Run ----------
if __name__ == '__main__':
    # Ensure DB exists
    if not os.path.exists(DB_PATH):
        print("Please run init_db.py first to create the database and admin user.")
    app.run(debug=True, port=5000)
