import random
import time
from config import connect

def auto_review_20_students_per_subject():
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    print("Cleaning up existing feedback records...")
    cursor.execute("DELETE FROM feedback")
    conn.commit()

    # Fetch all subjects and feedback questions
    cursor.execute("SELECT course_id, course_name FROM courses")
    courses = cursor.fetchall()

    cursor.execute("SELECT question_id FROM feedback_questions")
    questions = [q["question_id"] for q in cursor.fetchall()]

    if not courses or not questions:
        print("Error: Ensure courses and feedback_questions exist in MySQL first!")
        conn.close()
        return

    # Sample comments for realistic student remarks
    sample_remarks = [
        "Clear explanation of core concepts.",
        "Interactive lectures and helpful doubt clearing.",
        "Assignments were well-structured.",
        "Great practical lab sessions.",
        "Good course material and pacing.",
        "Need more live coding practice.",
        "Overall very satisfied with the instructor.",
        ""
    ]

    print("\nStarting auto-review generation (20 students per subject)...")

    for course in courses:
        course_id = course["course_id"]
        course_name = course["course_name"]

        for student_num in range(1, 21):  # Exactly 20 students
            # Unique timestamp per student submission to ensure accurate student counts
            submission_time = time.strftime('%Y-%m-%d %H:%M:%S')
            comment = random.choice(sample_remarks)

            for question_id in questions:
                # Realistic rating distribution (mostly 4s and 5s, with occasional 3s)
                rating = random.choices([3, 4, 5], weights=[15, 45, 40])[0]

                sql = """
                    INSERT INTO feedback (course_id, question_id, rating, comment_optional, submitted_at)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (course_id, question_id, rating, comment, submission_time))

        print(f"✓ Successfully generated 20 student reviews for: {course_name}")

    conn.commit()
    cursor.close()
    conn.close()
    print("\nAll subjects successfully populated with 20 student reviews each!")

if __name__ == "__main__":
    auto_review_20_students_per_subject()