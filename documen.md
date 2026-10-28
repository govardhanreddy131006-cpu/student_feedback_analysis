# Student Feedback Analysis System

## 1. About the Project
The **Student Feedback Analysis System** is a Python-based web application designed to collect, manage, and analyze student feedback for college courses and faculty members. It connects to a MySQL database and uses Flask to provide an interactive web interface for:
* Filtering feedback analysis by subject or trainer.
* Generating dynamic Matplotlib bar charts server-side without external web assets.
* Serving structured JSON student review reports for administrative auditing.

This project is developed as a college team project.

---

## 2. Key Features
* **Home Selection Portal (`/`)**: Interactively select courses and faculty trainers with automatic client-side dropdown filtering via JavaScript.
* **Student Feedback Entry Form (`/feedback-form`)**: Allow students to submit roll numbers, course selections, trainer choices, ratings across evaluation sections, and optional remarks.
* **Filtered Analysis Dashboard (`/analysis`)**: Compute and display section-wise average ratings (*Teaching*, *Content*, *Practical*) out of 5.0.
* **Data Visualization (`/chart.png`)**: Generate and display dynamic Matplotlib bar charts color-coded by performance thresholds.
* **Filtered Student Reviews API (`/admin/student-details-json`)**: Export and view structured student review logs in JSON format filtered by course or trainer.

---

## 3. Technologies Used
* **Python** — Core application logic and data processing
* **Flask** — Web application backend framework
* **MySQL** — Relational database management system (`mysql-connector-python`)
* **Matplotlib** — Server-side graph generation and data visualization
* **HTML5 / CSS3 / JavaScript (ES6)** — Web page structuring, styling, and dynamic element filtering
* **Git & GitHub** — Version control and collaborative code sharing

---

## 4. Project Structure

```text
student_feedback_app/
├── .venv/                     # Virtual environment folder
├── database/
│   └── schema.sql             # SQL schema definitions and database setup script
├── app.py                     # Main Flask application and server routes
├── config.py                  # MySQL database connection configuration
└── seed_responses.py          # Script to populate sample feedback responses
```

---

## 5. System Requirements
* **Python 3.x**
* **MySQL Server**
* **PyCharm** (or any Python IDE)
* **Git**

---

## 6. Setup and Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/govardhanreddy131006-cpu/student_feedback_analysis.git
```
Open the downloaded project folder in PyCharm.

### Step 2: Install Required Python Packages
Open the PyCharm terminal in your project directory, activate your virtual environment, and install all required packages:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install Flask mysql-connector-python matplotlib
```

### Step 3: Configure MySQL Database
1. Start your local MySQL Server.
2. Open **MySQL Workbench** or MySQL CLI and create the database:
   ```sql
   CREATE DATABASE college_db;
   USE college_db;
   ```
3. Execute the SQL statements inside `database/schema.sql` to create `courses`, `trainers`, `sections`, `feedback_questions`, and `feedback` tables.
4. Set up your local `config.py` with your MySQL credentials:
   ```python
   import mysql.connector

   def connect():
       return mysql.connector.connect(
           host="localhost",
           user="root",
           password="YOUR_MYSQL_PASSWORD",
           database="college_db"
       )
   ```
   > **Note:** Do not commit your actual database password to GitHub. Ensure `config.py` is added to your `.gitignore`.

5. *(Optional)* Run the seed script to populate sample test data:
   ```bash
   python seed_responses.py
   ```

### Step 4: Run the Application
In the PyCharm terminal, execute:
```bash
python app.py
```
Open the local server address displayed in the terminal:
```text
http://127.0.0.1:5000/
```

---

## 7. Application Endpoints & Routes

| Route | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Home Selection page (Select course & trainer) |
| `/analysis` | `GET` | View calculated section averages and performance graph |
| `/feedback-form` | `GET` | Student feedback submission portal |
| `/submit-feedback` | `POST` | Endpoint to insert submitted student reviews into MySQL |
| `/chart.png` | `GET` | Dynamic Matplotlib PNG image stream endpoint |
| `/admin/student-details-json` | `GET` | Filtered student feedback review logs in JSON format |

---

## 8. Team Collaboration
This repository serves as the centralized source code repository for team collaboration.

Team members should clone the repository, run `database/schema.sql` in their local MySQL server, set up their personal `config.py` credentials, install the required packages, and run `python app.py` locally.

---

## 9. Project Status
The project is under active development. Further analytical capabilities and user interface enhancements will be integrated continuously.