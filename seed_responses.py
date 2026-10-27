import random
import time
from config import connect

def seed_responses_with_roll_numbers():
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    print("Clearing existing feedback records...")
    cursor.execute("DELETE FROM feedback")
    conn.commit()

    cursor.execute("SELECT course_id, course_name FROM courses")
    courses = cursor.fetchall()

    cursor.execute("SELECT question_id FROM feedback_questions")
    questions = [q["question_id"] for q in cursor.fetchall()]

    for course in courses:
        course_id = course["course_id"]
        cursor.execute("SELECT trainer_id, trainer_name FROM trainers WHERE course_id = %s", (course_id,))
        trainers = cursor.fetchall()

        for trainer_idx, trainer in enumerate(trainers):
            trainer_id = trainer["trainer_id"]

            for student_num in range(1, 21):
                # Format roll numbers like 21121A0501, 21121A0502...
                roll_number = f"21121A05{student_num:02d}"
                submission_time = time.strftime('%Y-%m-%d %H:%M:%S')

                for question_id in questions:
                    rating = random.choices([3, 4, 5], weights=[20, 50, 30])[0]
                    sql = """
                        INSERT INTO feedback (course_id, roll_number, trainer_id, question_id, rating, submitted_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (course_id, roll_number, trainer_id, question_id, rating, submission_time))

    conn.commit()
    cursor.close()
    conn.close()
    print("Successfully seeded responses with student roll numbers!")

if __name__ == "__main__":
    seed_responses_with_roll_numbers()