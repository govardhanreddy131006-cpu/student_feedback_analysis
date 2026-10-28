import io
import matplotlib.pyplot as plt
from flask import Flask, Response, jsonify, render_template_string, request
from config import connect

app = Flask(__name__)


def get_section_averages(course_id=None, trainer_id=None):
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT s.section_name, ROUND(AVG(f.rating), 2) AS average_score
        FROM feedback f
        JOIN feedback_questions q ON f.question_id = q.question_id
        JOIN sections s ON q.section_id = s.section_id
        WHERE 1=1
    """
    params = []

    if course_id and str(course_id).strip() != "":
        sql += " AND f.course_id = %s"
        params.append(course_id)

    if trainer_id and str(trainer_id).strip() != "":
        sql += " AND f.trainer_id = %s"
        params.append(trainer_id)

    sql += " GROUP BY s.section_id, s.section_name"

    cursor.execute(sql, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in results:
        row["average_score"] = float(row["average_score"])

    return results


def get_all_courses():
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return courses


def get_all_trainers():
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT trainer_id, trainer_name, course_id, gender FROM trainers")
    trainers = cursor.fetchall()
    cursor.close()
    conn.close()
    return trainers


def get_trainers_grouped_by_course():
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT c.course_id,
               c.course_name,
               c.course_code,
               t.trainer_id,
               t.trainer_name,
               t.gender
        FROM courses c
        LEFT JOIN trainers t ON c.course_id = t.course_id
        ORDER BY c.course_id, t.trainer_id
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    courses_dict = {}
    for row in rows:
        c_id = row["course_id"]
        if c_id not in courses_dict:
            courses_dict[c_id] = {
                "course_id": c_id,
                "course_name": row["course_name"],
                "course_code": row["course_code"],
                "trainers_count": 0,
                "trainers": []
            }

        if row["trainer_id"]:
            courses_dict[c_id]["trainers"].append({
                "trainer_id": row["trainer_id"],
                "trainer_name": row["trainer_name"],
                "gender": row["gender"]
            })
            courses_dict[c_id]["trainers_count"] += 1

    return list(courses_dict.values())


def get_questions():
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT question_id, question_text FROM feedback_questions")
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    return questions


def insert_student_feedback(course_id, trainer_id, roll_number, responses, comment):
    conn = connect()
    cursor = conn.cursor()
    sql = """
        INSERT INTO feedback (course_id, trainer_id, roll_number, question_id, rating, comment_optional)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = [(course_id, trainer_id, roll_number, q_id, rating, comment) for q_id, rating in responses.items()]
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()
    conn.close()


def get_filtered_student_reviews_json(course_id=None, trainer_id=None):
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT MAX(f.feedback_id) AS feedback_id,
               f.roll_number,
               c.course_name,
               c.course_code,
               t.trainer_name,
               ROUND(AVG(f.rating), 2) AS average_rating,
               f.comment_optional,
               f.submitted_at
        FROM feedback f
        JOIN courses c ON f.course_id = c.course_id
        LEFT JOIN trainers t ON f.trainer_id = t.trainer_id
        WHERE 1 = 1
    """
    params = []
    if course_id and str(course_id).strip() != "":
        sql += " AND f.course_id = %s"
        params.append(course_id)
    if trainer_id and str(trainer_id).strip() != "":
        sql += " AND f.trainer_id = %s"
        params.append(trainer_id)

    sql += """
        GROUP BY 
            f.roll_number, 
            f.course_id, 
            c.course_name, 
            c.course_code, 
            t.trainer_name, 
            f.trainer_id, 
            f.comment_optional, 
            f.submitted_at
        ORDER BY f.submitted_at DESC
    """
    cursor.execute(sql, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    for r in results:
        r["average_rating"] = float(r["average_rating"])
        if r["submitted_at"]:
            r["submitted_at"] = str(r["submitted_at"])

    return results


@app.route("/")
def index():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Feedback Portal</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 50px; background-color: #f4f6f9; }
            .card { max-width: 450px; margin: auto; background: white; padding: 35px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            h1 { color: #007bff; margin-bottom: 25px; }
            .btn { display: block; width: 90%; margin: 15px auto; padding: 14px; background-color: #007bff; color: white; text-decoration: none; border-radius: 6px; font-size: 16px; font-weight: bold; }
            .btn-green { background-color: #28a745; }
            .btn-info { background-color: #17a2b8; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Student Feedback System</h1>
            <a href="/analysis" class="btn">View Admin Dashboard</a>
            <a href="/feedback-form" class="btn btn-green">Fill Student Feedback Form</a>
            <a href="/admin/trainers-by-course-json" class="btn btn-info" target="_blank">View Courses & Trainers (JSON)</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_code)


@app.route("/admin/trainers-by-course-json")
def trainers_by_course_json():
    grouped_data = get_trainers_grouped_by_course()
    return jsonify({
        "status": "success",
        "total_courses": len(grouped_data),
        "courses_and_trainers": grouped_data
    })


@app.route("/analysis")
def analysis():
    course_id = request.args.get("course_id", "")
    trainer_id = request.args.get("trainer_id", "")

    courses = get_all_courses()
    trainers = get_all_trainers()
    results = get_section_averages(course_id=course_id, trainer_id=trainer_id)

    if not results:
        table_html = "<p style='color: red; font-weight: bold;'>No feedback ratings submitted for this specific trainer or subject yet.</p>"
    else:
        table_rows = "".join(
            [f"<tr><td>{r['section_name']}</td><td><strong>{r['average_score']} / 5.0</strong></td></tr>" for r in results]
        )
        table_html = f"""
        <table class="table">
            <thead>
                <tr><th>Section Name</th><th>Average Rating</th></tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """

    json_reviews_url = f"/admin/student-details-json?course_id={course_id}&trainer_id={trainer_id}"
    chart_url = f"/chart.png?course_id={course_id}&trainer_id={trainer_id}"

    course_options = "".join([
        f'<option value="{c["course_id"]}" {"selected" if str(c["course_id"]) == str(course_id) else ""}>{c["course_code"]} - {c["course_name"]}</option>'
        for c in courses
    ])

    trainer_options = "".join([
        f'<option value="{t["trainer_id"]}" data-course="{t["course_id"]}" {"selected" if str(t["trainer_id"]) == str(trainer_id) else ""}>{t["trainer_name"]}</option>'
        for t in trainers
    ])

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Feedback Analysis Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; margin: 30px; background-color: #f8f9fa; }}
            .filter-card {{ max-width: 600px; margin: 0 auto 20px auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            table {{ margin: 20px auto; border-collapse: collapse; width: 60%; background: white; }}
            th, td {{ border: 1px solid #dddddd; padding: 10px; text-align: center; }}
            th {{ background-color: #007bff; color: white; }}
            .btn {{ display: inline-block; padding: 10px 15px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 5px; cursor: pointer; border: none; }}
            .btn-secondary {{ background-color: #6c757d; }}
            .btn-info {{ background-color: #17a2b8; }}
            select {{ padding: 8px; margin: 5px; border-radius: 4px; border: 1px solid #ccc; }}
        </style>
    </head>
    <body>
        <h1>Admin Feedback Analysis Dashboard</h1>

        <div class="filter-card">
            <form action="/analysis" method="GET">
                <label><strong>Filter Subject:</strong></label>
                <select name="course_id" id="courseSelect" onchange="filterTrainers()">
                    <option value="">-- All Subjects --</option>
                    {course_options}
                </select>

                <label><strong>Filter Trainer:</strong></label>
                <select name="trainer_id" id="trainerSelect">
                    <option value="">-- All Trainers --</option>
                    {trainer_options}
                </select>

                <button type="submit" class="btn">Apply Filter</button>
            </form>
        </div>

        <a href="/" class="btn btn-secondary">Back to Home</a>
        <a href="{json_reviews_url}" class="btn btn-info" target="_blank">View Student Reviews (JSON)</a>

        <h3>Section Average Ratings</h3>
        {table_html}

        <h3>Performance Bar Graph</h3>
        <img src="{chart_url}" alt="Feedback Chart" width="600">

        <script>
        function filterTrainers() {{
            var selectedCourse = document.getElementById("courseSelect").value;
            var trainerSelect = document.getElementById("trainerSelect");
            var options = trainerSelect.querySelectorAll("option");

            trainerSelect.value = "";

            options.forEach(function(option) {{
                var cId = option.getAttribute("data-course");
                if (!cId) return;

                if (!selectedCourse || cId === selectedCourse) {{
                    option.style.display = "block";
                    option.disabled = false;
                }} else {{
                    option.style.display = "none";
                    option.disabled = true;
                }}
            }});
        }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html_code)


@app.route("/feedback-form")
def feedback_form():
    courses = get_all_courses()
    trainers = get_all_trainers()
    questions = get_questions()

    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Feedback Entry Form</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f8f9fa; }
            .container { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h2 { text-align: center; color: #007bff; }
            .form-group { margin-bottom: 15px; text-align: left; }
            label { font-weight: bold; display: block; margin-bottom: 5px; }
            input[type="text"], select, textarea { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
            .question-box { background: #e9ecef; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: left; }
            .rating-options label { font-weight: normal; margin-right: 15px; }
            button { width: 100%; background-color: #28a745; color: white; padding: 10px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Student Feedback Form</h2>
            <form action="/submit-feedback" method="POST">
                <div class="form-group">
                    <label>Student Roll Number:</label>
                    <input type="text" name="roll_number" placeholder="e.g. 21121A0501" required>
                </div>
                <div class="form-group">
                    <label>Select Course:</label>
                    <select name="course_id" required>
                        <option value="" disabled selected>-- Choose Course --</option>
                        {% for c in courses %}
                            <option value="{{ c.course_id }}">{{ c.course_code }} - {{ c.course_name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label>Select Trainer:</label>
                    <select name="trainer_id" required>
                        <option value="" disabled selected>-- Choose Faculty --</option>
                        {% for t in trainers %}
                            <option value="{{ t.trainer_id }}">{{ t.trainer_name }} ({{ t.gender }})</option>
                        {% endfor %}
                    </select>
                </div>
                <h3>Evaluation Questions</h3>
                {% for q in questions %}
                    <div class="question-box">
                        <label>{{ q.question_text }}</label>
                        <div class="rating-options">
                            {% for r in range(1, 6) %}
                                <label><input type="radio" name="question_{{ q.question_id }}" value="{{ r }}" required> {{ r }}</label>
                            {% endfor %}
                        </div>
                    </div>
                {% endfor %}
                <div class="form-group">
                    <label>Optional Remarks:</label>
                    <textarea name="comment" rows="3" placeholder="Enter remarks..."></textarea>
                </div>
                <button type="submit">Submit Feedback</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_code, courses=courses, trainers=trainers, questions=questions)


@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    course_id = request.form.get("course_id")
    trainer_id = request.form.get("trainer_id")
    roll_number = request.form.get("roll_number", "").strip()
    comment = request.form.get("comment", "")

    responses = {}
    for key, value in request.form.items():
        if key.startswith("question_"):
            q_id = key.split("_")[1]
            responses[q_id] = int(value)

    if course_id and trainer_id and roll_number and responses:
        insert_student_feedback(course_id, trainer_id, roll_number, responses, comment)
        return "<h1>Feedback Submitted Successfully!</h1><a href='/'>Back to Home</a>"

    return "Invalid Submission", 400


@app.route("/admin/student-details-json")
def student_reviews_json():
    course_id = request.args.get("course_id", "")
    trainer_id = request.args.get("trainer_id", "")

    reviews = get_filtered_student_reviews_json(course_id=course_id, trainer_id=trainer_id)
    return jsonify({
        "status": "success",
        "filter_course_id": course_id or "All",
        "filter_trainer_id": trainer_id or "All",
        "total_filtered_reviews": len(reviews),
        "student_reviews": reviews
    })


@app.route("/chart.png")
def chart():
    course_id = request.args.get("course_id", "")
    trainer_id = request.args.get("trainer_id", "")

    results = get_section_averages(course_id=course_id, trainer_id=trainer_id)

    fig, ax = plt.subplots(figsize=(7, 4))

    if not results:
        ax.text(0.5, 0.5, "No Data Available for Selection", ha="center", va="center", fontsize=14, color="gray")
        ax.axis("off")
    else:
        sections = [r["section_name"] for r in results]
        scores = [r["average_score"] for r in results]

        colors = ['#28a745' if s >= 4.0 else '#ffc107' if s >= 3.0 else '#dc3545' for s in scores]

        bars = ax.bar(sections, scores, color=colors, width=0.4)
        ax.set_title("Section-Wise Feedback Scores", fontsize=12, fontweight="bold")
        ax.set_xlabel("Evaluation Sections", fontweight="bold")
        ax.set_ylabel("Average Score (Out of 5)", fontweight="bold")
        ax.set_ylim(0, 5.5)

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=120)
    plt.close(fig)
    buffer.seek(0)

    return Response(buffer.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)