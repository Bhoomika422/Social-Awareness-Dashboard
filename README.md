# 🌐 Social Awareness Analytics Portal

An end-to-end full-stack analytics platform built to monitor, analyze, and visualize social issue data and community awareness trends using Python Flask, AI-driven text classification, and interactive visualization dashboards.

---

## 📌 Executive Summary & Business Impact
* **Business Problem:** Community grievances and civic issue reports are often unstructured, making manual categorization slow and hindering timely intervention by local authorities or NGOs.
* **Solution:** Developed an automated end-to-end web portal that ingests citizen reports, utilizes an AI-based text classification pipeline to categorize issues automatically, and generates real-time analytics dashboards for decision-makers.

---

## 📋 Table of Contents
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Directory Structure](#-project-directory-structure)
- [Installation & Setup](#-installation--setup)
- [How It Works](#-how-it-works)
- [Testing & Validation](#-testing--validation)
- [Future Roadmap & Next-Gen AI Integration](#-future-roadmap--next-gen-ai-integration)
- [Author](#-author)

---

## ✨ Key Features
* **Full-Stack Architecture:** Modular design separating backend application logic (Flask), frontend client interfaces (HTML/CSS/JS), and persistent data models.
* **AI & NLP Keyword Classification:** Integrates an intelligent text classification module to automatically parse, flag, and categorize raw citizen report text into predefined issue domains.
* **Data Processing & ETL Pipeline:** Clean, normalize, and manipulate structured report data utilizing **Pandas** and **NumPy**.
* **Interactive Analytics Visualizations:** Real-time dashboards rendering key metrics and trend plots using **Chart.js**, **Matplotlib**, and **Seaborn**.
* **Database & Export Support:** Automated SQLite database initialization with support for exporting analytical records directly to Excel.

---

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Chart.js |
| **Backend & APIs** | Python, Flask, REST APIs, JSON |
| **Data Analysis & AI** | Pandas, NumPy, Intelligent Keyword Classification Engine |
| **Data Visualization** | Matplotlib, Seaborn, Chart.js |
| **Database & Files** | SQLite (`reports.db`), MS Excel (`reports.xlsx`) |

---

## 📁 Project Directory Structure

'''text
Social_Awareness_Project_MainDb/
│
├── backend/          # Backend controllers & business logic
├── frontend/         # Client-side UI components
├── data/             # Datasets & analytical inputs
├── static/           # CSS stylesheets, JavaScript files & assets
├── templates/        # HTML templates rendered by Flask
├── uploads/          # File upload directory for user reports
├── app.py            # Main Flask application entry point
├── init_db.py        # Database setup & schema initialization script
├── reports.db        # SQLite database file
├── reports.xlsx      # Exported analytical spreadsheet
└── requirements.txt  # Python project dependencies '''

## 🚀 Installation & Setup
Follow these steps to set up and run the project locally:

1. Clone the Repository
Bash
git clone [https://github.com/Bhoomikasahu1/Social_Awareness_Project_MainDb.git](https://github.com/Bhoomikasahu1/Social_Awareness_Project_MainDb.git)
cd Social_Awareness_Project_MainDb
2. Create & Activate Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Initialize Database & Launch Application
Bash
python init_db.py
python app.py
Open your browser and visit: http://127.0.0.1:5000

## 🤖 How It Works
Data Ingestion: Community reports and text data are received via web form submissions or batch-uploaded files (uploads/).

AI Classification: The text processing engine analyzes incoming report content against contextual keyword patterns to assign specific issue categories.

ETL & Transformation: Pandas and NumPy aggregate structured metrics, calculate statistical summaries, and handle missing data points.

Dashboard Rendering: Processed payloads are passed from Flask backend controllers to templates, rendering dynamic Chart.js plots and visual summary cards.

##🧪 Testing & Validation
API & Data Payload Validation: Performed functional testing on backend endpoints using structured test payloads to ensure accuracy of JSON responses.

Data Integrity Checks: Verified database transactions and statistical outputs against raw data inputs to prevent data loss or duplicate entry errors.

##🔮 Future Roadmap & Next-Gen AI Integration
The future scope of this portal focuses on expanding from rule-based text analysis to advanced Generative AI & Multimodal Workflows:

Multimodal Citizen Reporting via Gemini API: Integrating Google Gemini Vision capabilities allowing citizens to upload photos or voice notes of civic issues (e.g., potholes, garbage accumulation). The multimodal LLM will auto-extract geographic context, assess severity, and draft an issue summary.

Agentic AI & Autonomous Triage: Implementing LangChain/LangGraph AI agents to autonomously analyze incoming complaints, categorize urgency levels, and route dispatches directly to relevant municipal department APIs.

Predictive Civic Analytics: Developing predictive ML models to forecast recurring urban issues (such as waterlogging risk prior to monsoons) using historical complaint trends and spatial data.

Conversational Citizen Assistants: Building RAG-powered natural language chatbots for real-time status tracking and policy inquiry handling in regional languages.

👤 Author
**Bhoomika Sahu**
📧 Email: bhoomikasahu422@gmail.com
💼 LinkedIn: Bhoomika Sahu
💻 GitHub: https://github.com/Bhoomika422
