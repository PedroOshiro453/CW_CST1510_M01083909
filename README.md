Student: M01083909
GitHub: https://github.com/PedroOshiro453/CW_CST1510_M01083909
Module: CST1510 – Programming for Data Communication and Networks
Assessment: Coursework 2 (CW2)

Multi-Domain Intelligence Platform (CW2)
Overview

This project is a Multi-Domain Intelligence Platform developed as part of the CST1510 – Programming for Data Communication and Networks (Coursework 2).

The application is built using Python and Streamlit and provides an interactive dashboard to analyse cybersecurity incidents stored in CSV files. The platform demonstrates key concepts taught throughout Weeks 7–11, including authentication, data handling, visualisation, and structured application design.

Features
1. User Authentication (File-Based)
    Login and registration system using DATA/user.txt
    Passwords are securely stored using bcrypt hashing
    Session-based authentication with st.session_state
    Protected pages using a guard pattern (login required)

2. Cyber Incidents Dashboard
    Data source: DATA/cyber_incidents.csv
    Interactive dashboard with:
    Severity filter (sidebar)
    Bar chart: number of incidents by category
    Line chart: incident progression over time
    Data table with full incident details
    Responsive layout using Streamlit columns

3. Robust Data Handling
    Automatic validation of CSV structure
    Safe handling of time-only timestamps (e.g. 00:00.0)
    Synthetic timeline generation when real timestamps lack variation
    Consistent rendering even with incomplete or imperfect datasets

Project Structure
CW_CST1510_M01083909/
│
├── Apps.py                # Main Streamlit application (navigation + routing)
├── Home.py                # Login / Register page
├── Dashboard.py           # Cyber Incidents Dashboard
├── log_hash.py            # Password hashing and verification (bcrypt)
├── main.py                # Console-based auth demo (Week 7)
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
│
├── DATA/
│   ├── cyber_incidents.csv
│   ├── datasets_metadata.csv
│   ├── it_tickets.csv
│   └── user.txt
│
└── .venv/                 # Virtual environment (not committed)

Data Sources
cyber_incidents.csv

Expected columns:
    incident_id,timestamp,severity,category,status,description

Note:
The dataset contains time-only values (e.g. 00:00.0). Since this limits true temporal analysis, the dashboard dynamically generates a synthetic timeline to ensure the line chart remains meaningful and visually informative.

How to Run the Application
1. Create and activate a virtual environment
    python -m venv .venv
    source .venv/bin/activate   # Linux / macOS
    .venv\Scripts\activate      # Windows

2. Install dependencies
    pip install -r requirements.txt

3. Run the Streamlit app
    streamlit run Apps.py

The application will be available at:
    http://localhost:8501

Dashboard Explanation

-Sidebar
    Navigation between pages
    Severity filter for cyber incidents

-Visualisations
    Bar Chart: Displays the number of incidents per category for the selected severity
    Line Chart: Shows the progression of incidents using a plot-friendly timeline
    Table: Displays detailed records of filtered incidents
This design follows the layout patterns demonstrated in the workshop materials (layout_demo.py, mini_dashboard.py).

-Security Considerations
    Passwords are never stored in plain text
    bcrypt hashing with salt is used
    User sessions are handled securely using Streamlit session state
    Protected routes prevent unauthorised access

-Learning Outcomes Demonstrated
    Python modular programming
    Streamlit UI development
    File-based authentication
    Data cleaning and validation
    Interactive data visualisation
    Application architecture and separation of concerns

-Future Improvements
    Migration from CSV to SQLite database
    Full CRUD operations from the UI
    AI-powered insights using OpenAI API
    Additional dashboards for:
        Data Science metadata
        IT service desk tickets