from flask import Flask, jsonify, request, send_from_directory
import csv, os
from collections import Counter
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'reports.csv')

# -----------------------------
# Simple keyword-based classifier (AI component)
# -----------------------------
CATEGORY_KEYWORDS = {
    "Health": ["fever", "sick", "clinic", "hospital", "disease", "outbreak", "virus"],
    "Sanitation": ["garbage", "trash", "waste", "sewage", "drain", "dumping"],
    "Safety": ["accident", "robbery", "unsafe", "danger", "injury"],
    "Environment": ["pollution", "smoke", "air", "water", "noise", "tree"],
}


def classify_text(text):
    text_lower = text.lower()
    scores = Counter()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[cat] += 1
    if scores:
        return scores.most_common(1)[0][0]
    return "Other"


# -----------------------------
# Load Reports
# -----------------------------
def load_reports(limit=None):
    reports = []
    if not os.path.exists(DATA_PATH):
        return reports
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit and i >= limit:
                break
            reports.append(row)
    return reports


# -----------------------------
# API Endpoints
# -----------------------------
@app.route('/api/reports')
def api_reports():
    reports = load_reports()
    # Add classification to each report (AI)
    for r in reports:
        if not r.get('category'):
            r['category'] = classify_text(r.get('description', ''))
    return jsonify(reports)


@app.route('/api/summary')
def api_summary():
    reports = load_reports()
    categories = Counter()
    for r in reports:
        cat = r.get('category') or classify_text(r.get('description', ''))
        categories[cat] += 1
    summary = {"total": len(reports), "by_category": dict(categories)}
    return jsonify(summary)


# -----------------------------
# Endpoint to accept new report (POST)
# -----------------------------
@app.route('/api/report', methods=['POST'])
def api_report():
    data = request.json or {}
    fields = ['id', 'title', 'description', 'latitude', 'longitude', 'category']
    file_exists = os.path.exists(DATA_PATH)

    # Determine new ID
    new_id = 1
    if file_exists:
        with open(DATA_PATH, newline='', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            ids = [int(r['id']) for r in reader if r.get('id') and str(r['id']).isdigit()]
            if ids:
                new_id = max(ids) + 1

    # Prepare new row
    row = {k: data.get(k, '') for k in fields}
    row['id'] = str(new_id)

    # Auto-classify if category not provided
    if not row.get('category'):
        row['category'] = classify_text(row.get('description', ''))

    # Ensure directory exists
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    # 🔥 NEW CODE (Added section starts here)
    # Ensure previous entry ends with newline before appending
    if file_exists:
        with open(DATA_PATH, 'rb+') as f:
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:  # if file not empty
                f.seek(-1, os.SEEK_END)
                last_char = f.read(1)
                if last_char != b'\n':
                    f.write(b'\n')
    # 🔥 NEW CODE (Added section ends here)

    # Append new row
    write_header = not os.path.exists(DATA_PATH)
    with open(DATA_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    return jsonify({"status": "ok", "row": row}), 201



# -----------------------------
# Serve Frontend (index.html)
# -----------------------------
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')


# -----------------------------
# Main
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
