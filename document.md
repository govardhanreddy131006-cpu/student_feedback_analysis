# Student Feedback Analysis System

## 1. About the Project

The **Student Feedback Analysis System** is a Python-based web application designed to collect, manage, and analyze student feedback about college courses and faculty members.

The application uses **Flask** for the web interface and **MySQL** to store feedback data. It provides features for:

- Filtering feedback analysis by subject or trainer.
- Calculating average ratings for different teaching and learning sections.
- Generating dynamic Matplotlib bar charts on the server.
- Providing structured JSON reports for administrative review.
- Displaying courses and their assigned trainers in a nested JSON format.

This project is developed as a college team project.

## 2. Key Features

### 2.1 Home Portal (`/`)

Provides a simple landing page with navigation links to the Admin Dashboard, Student Feedback Form, and JSON API feeds.

### 2.2 Filtered Analysis Dashboard (`/analysis`)

Calculates and displays average ratings out of 5.0 for these sections:

- Teaching
- Content
- Practical

Users can filter the analysis by subject or trainer.

### 2.3 Student Feedback Form (`/feedback-form`)

Allows students to submit:

- Roll number
- Course selection
- Trainer selection
- Ratings for evaluation sections
- Optional remarks

### 2.4 Data Visualization (`/chart.png`)

Generates a dynamic bar chart using Matplotlib. The chart uses different colors to represent performance thresholds.

### 2.5 Courses and Trainers JSON API (`/admin/trainers-by-course-json`)

Returns a structured, nested JSON feed containing subjects and their assigned faculty trainers.

### 2.6 Filtered Student Reviews API (`/admin/student-details-json`)

Returns structured student feedback records that can be filtered by course or trainer for administrative auditing.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic and data processing |
| Flask | Web application backend framework |
| MySQL | Relational database management |
| `mysql-connector-python` | Connects Python to MySQL |
| Matplotlib | Server-side charts and data visualization |
| HTML5 | Web page structure |
| CSS3 | Page styling and layout |
| JavaScript (ES6) | Dynamic page interactions and filtering |
| Git and GitHub | Version control and team collaboration |

## 4. Project Structure

```text
student_feedback_app/
├── .venv/                     # Python virtual environment
├── database/
│   └── schema.sql             # Database schema and setup script
├── app.py                     # Main Flask application and routes
├── config.py                  # MySQL connection configuration
└── seed_responses.py          # Script to insert sample feedback
```

## 5. System Requirements

Before running the project, make sure the following software is installed:

- Python 3.x
- MySQL Server
- MySQL Workbench or MySQL command-line client
- PyCharm or another Python IDE
- Git (for cloning the repository)

## 6. Setup and Installation

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/govardhanreddy131006-cpu/student_feedback_analysis.git
```

Open the downloaded `student_feedback_analysis` folder in PyCharm.

### Step 2: Create a Virtual Environment and Install Packages

Open the PyCharm terminal in the project directory and run these commands on Windows:

```bash
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install Flask mysql-connector-python matplotlib
```

### Step 3: Configure the MySQL Database

1. Start your local MySQL Server.
2. Open MySQL Workbench or the MySQL command-line client.
3. Create the database by running:

```sql
CREATE DATABASE college_db;
USE college_db;
```

4. Execute the SQL statements in `database/schema.sql` to create the required tables, including `courses`, `trainers`, `sections`, `feedback_questions`, and `feedback`.

### Step 4: Configure the Database Connection

Create or update `config.py` with your local MySQL credentials:

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

**Security note:** Replace `YOUR_MYSQL_PASSWORD` with your local MySQL password. Do not commit real passwords or other secrets to GitHub. Add `config.py` to `.gitignore` if it contains credentials.

### Step 5: (Optional) Insert Sample Feedback Data

To populate the database with sample responses for testing, run:

```bash
python seed_responses.py
```

### Step 6: Run the Application

In the PyCharm terminal, execute:

```bash
python app.py
```

Open the local URL shown in the terminal. It is commonly:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

The application will be available while the Flask server is running.

## 7. Application Endpoints and Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home portal with links to the dashboard, feedback form, and JSON feeds |
| `/analysis` | GET | Displays section-wise average ratings, filter controls, and performance graph |
| `/feedback-form` | GET | Displays the student feedback submission form |
| `/submit-feedback` | POST | Receives submitted feedback and inserts it into MySQL |
| `/chart.png` | GET | Generates a dynamic Matplotlib chart as a PNG image |
| `/admin/trainers-by-course-json` | GET | Returns courses and their assigned trainers as nested JSON |
| `/admin/student-details-json` | GET | Returns filtered student feedback review records |

## 8. Team Collaboration

GitHub acts as the centralized repository for the project.

Each team member should:

1. Clone the repository.
2. Open the project in their preferred Python IDE.
3. Create and activate a virtual environment.
4. Install the required Python packages.
5. Create the local MySQL database.
6. Execute `database/schema.sql`.
7. Configure their own database credentials in `config.py`.
8. Run `python app.py` and test the application locally.

Team members should avoid committing virtual environment folders, database passwords, and other sensitive configuration details.

## 9. Project Status and Future Enhancements

The project is currently under active development. Future improvements may include:

- More detailed feedback analytics and comparisons.
- Improved dashboard design and usability.
- Additional filtering and reporting options.
- Better validation and error handling.
- Secure administrator authentication and access control.
- Exporting reports for administrative use.

These are proposed enhancements and may not yet be implemented.

## 10. Conclusion

The **Student Feedback Analysis System** provides a centralized way to collect and analyze student feedback about courses and faculty members. By combining Flask, MySQL, and Matplotlib, the system supports feedback management, rating analysis, graphical reports, and structured JSON data for administrative review.

The project also gives the team practical experience with Python web development, database integration, data visualization, API routes, and collaborative software development.
