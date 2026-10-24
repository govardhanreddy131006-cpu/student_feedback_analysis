from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import connect


def get_all_courses():
    """Fetch all courses for drop-down menus."""
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return courses


def get_questions_by_section():
    """Fetch unique questions grouped by section."""
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    sql = """
          SELECT DISTINCT q.question_id, \
                          q.question_text, \
                          s.section_id, \
                          s.section_name
          FROM feedback_questions q
                   JOIN sections s ON q.section_id = s.section_id
          ORDER BY s.section_id, q.question_id \
          """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    sections = {}
    for row in rows:
        sec_name = row["section_name"]
        if sec_name not in sections:
            sections[sec_name] = []
        if not any(q["question_text"] == row["question_text"] for q in sections[sec_name]):
            sections[sec_name].append(row)

    return sections


def insert_feedback(course_id, responses, comment=""):
    """CREATE Operation: Insert student rating responses."""
    conn = connect()
    cursor = conn.cursor()
    for question_id, rating in responses.items():
        sql = "INSERT INTO feedback (course_id, question_id, rating, comment_optional) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (course_id, question_id, rating, comment))
    conn.commit()
    cursor.close()
    conn.close()


def get_section_averages(course_id=None):
    """READ Operation: Calculate section-wise average ratings and actual student count."""
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    # We group by question count to get the exact number of student submissions per section
    sql = """
          SELECT s.section_name, \
                 ROUND(AVG(f.rating), 2)                              AS average_score, \
                 COUNT(f.feedback_id) / COUNT(DISTINCT f.question_id) AS response_count
          FROM feedback f
                   JOIN feedback_questions q ON f.question_id = q.question_id
                   JOIN sections s ON q.section_id = s.section_id \
          """
    params = []
    if course_id:
        sql += " WHERE f.course_id = %s"
        params.append(course_id)

    sql += " GROUP BY s.section_id, s.section_name"
    cursor.execute(sql, params)
    results = cursor.fetchall()

    # Round response_count to an integer
    for row in results:
        row["response_count"] = int(row["response_count"])

    cursor.close()
    conn.close()
    return results

def get_course_details(course_id=None):
    """Fetch specific course details for heading display."""
    if not course_id:
        return {"course_name": "All Subjects Combined", "course_code": "ALL"}

    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT course_name, course_code FROM courses WHERE course_id = %s", (course_id,))
    course = cursor.fetchone()
    cursor.close()
    conn.close()
    return course or {"course_name": "All Subjects Combined", "course_code": "ALL"}

def get_feedback_comments(course_id=None, limit=5):
    """Fetch recent optional comments provided by students."""
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    sql = """
          SELECT DISTINCT f.comment_optional, \
                          c.course_name, \
                          f.submitted_at
          FROM feedback f
                   JOIN courses c ON f.course_id = c.course_id
          WHERE f.comment_optional IS NOT NULL
            AND f.comment_optional != '' \
          """
    params = []
    if course_id:
        sql += " AND f.course_id = %s"
        params.append(course_id)

    sql += " ORDER BY f.submitted_at DESC LIMIT %s"
    params.append(limit)

    cursor.execute(sql, params)
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return comments

app = Flask(__name__)


@app.route("/")
def index():
    courses = get_all_courses()
    sections = get_questions_by_section()
    return render_template("index.html", courses=courses, sections=sections)


@app.route("/submit", methods=["POST"])
def submit():
    course_id = request.form.get("course_id")
    comment = request.form.get("comment", "")

    responses = {}
    for key, value in request.form.items():
        if key.startswith("question_"):
            q_id = key.split("_")[1]
            responses[q_id] = int(value)

    if course_id and responses:
        insert_feedback(course_id, responses, comment)
        return redirect(url_for("success"))
    return "Invalid submission", 400


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/admin/dashboard")
def dashboard():
    courses = get_all_courses()
    selected_course = request.args.get("course_id")

    # Fetch course header info
    current_course = get_course_details(course_id=selected_course)

    # Calculate 3-section average ratings
    averages = get_section_averages(course_id=selected_course)

    # Fetch student comments summary
    comments = get_feedback_comments(course_id=selected_course, limit=5)

    return render_template(
        "admin/dashboard.html",
        averages=averages,
        courses=courses,
        selected_course=selected_course,
        current_course=current_course,
        comments=comments
    )


@app.route("/api/chart-data")
def chart_data():
    course_id = request.args.get("course_id")
    data = get_section_averages(course_id=course_id)

    labels = [row["section_name"] for row in data]
    scores = [float(row["average_score"]) for row in data]

    return jsonify({"labels": labels, "scores": scores})


if __name__ == "__main__":
    app.run(debug=True)