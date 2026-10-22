# 🌐 Social Awareness Analytics Portal

An end-to-end full-stack analytics platform built to monitor, analyze, and visualize social issue data and community awareness trends using Python Flask, AI-driven keyword classification, and interactive data visualization libraries.

---

## 📋 Table of Contents
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Directory Structure](#-project-directory-structure)
- [Installation & Setup](#-installation--setup)
- [How It Works](#-how-it-works)
- [Author](#-author)

---

## ✨ Key Features
* **Full-Stack Architecture**: Modular design separating backend logic (`Flask`), frontend interfaces (`HTML/CSS/JS`), and database models.
* **AI Keyword Classification**: Integrates an intelligent classification component to automatically flag and categorize text inputs based on social context keywords.
* **Data Processing Pipeline**: Clean and manipulate structured report data utilizing **Pandas** and **NumPy**.
* **Interactive Visualizations**: Real-time analytical dashboards created using **Chart.js**, **Matplotlib**, and **Seaborn**.
* **Database Management**: Automated database initialization (`init_db.py`) and persistent record tracking.

---

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Chart.js |
| **Backend** | Python, Flask |
| **Data Analysis & AI** | Pandas, NumPy, AI Keyword Classifier |
| **Data Visualization** | Matplotlib, Seaborn, Chart.js |
| **Database & Files** | SQLite (`reports.db`), Excel (`reports.xlsx`) |

---

## 📁 Project Directory Structure

```text
Social_Awareness_Project_MainDb/
│
├── backend/          # Backend controllers & business logic
├── frontend/         # Client-side components
├── data/             # Datasets & analytical inputs
├── static/           # CSS stylesheets, JavaScript files & images
├── templates/        # HTML templates rendered by Flask
├── uploads/          # File upload directory for reports
├── app.py            # Main Flask application entry point
├── init_db.py        # Database setup & initialization script
├── reports.db        # SQLite database file
├── reports.xlsx      # Exported report analytical sheet
└── requirements.txt  # Python project dependencies


🚀 Installation & Setup
Follow these steps to run the project locally on your machine:

1. Clone the Repository
Bash
git clone [https://github.com/Bhoomikasahu1/Social_Awareness_Project_MainDb.git](https://github.com/Bhoomikasahu1/Social_Awareness_Project_MainDb.git)
cd Social_Awareness_Project_MainDb
2. Create & Activate Virtual Environment
Bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Initialize Database & Run Application
Bash
python init_db.py
python app.py
Open your web browser and navigate to: http://127.0.0.1:5000

🤖 How It Works
Data Ingestion: Community reports and social data are received via web forms or uploaded files (uploads/).

AI Classification: The AI engine scans incoming text data against defined keyword patterns to assign issue categories.

Data Transformation: Pandas and NumPy process the categorized data to generate aggregated statistical summaries.

Dashboard Rendering: The backend serves processed data to Flask templates, generating dynamic charts via Chart.js and Matplotlib plots.

👤 Author
Bhoomika Sahu

Email: bhoomikasahu422@gmail.com
