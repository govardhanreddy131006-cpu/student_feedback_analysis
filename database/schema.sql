-- 1. Create and select database
CREATE DATABASE IF NOT EXISTS college_db;
USE college_db;

-- 2. Drop existing tables to start fresh (in reverse dependency order)
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS feedback_questions;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS courses;

-- 3. Create Courses Table
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) NOT NULL UNIQUE
);

-- 4. Create Trainers Table (4 trainers per course)
CREATE TABLE trainers (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY,
    trainer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

-- 5. Create Sections Table (Evaluation Categories)
CREATE TABLE sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    section_name VARCHAR(100) NOT NULL
);

-- 6. Create Questions Table
CREATE TABLE feedback_questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    question_text VARCHAR(255) NOT NULL,
    FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE
);

-- 7. Create Student Feedback Responses Table
CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    trainer_id INT NOT NULL,
    roll_number VARCHAR(20) NOT NULL,
    question_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment_optional TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES feedback_questions(question_id) ON DELETE CASCADE
);

-- ==========================================
-- INSERT SEEDED DATA
-- ==========================================

-- Insert Courses
INSERT INTO courses (course_id, course_name, course_code) VALUES
(1, 'Python Programming', 'CS101'),
(2, 'Java Programming', 'CS102'),
(3, 'Web Development', 'CS103');

-- Insert Trainers (4 Trainers per Course)
INSERT INTO trainers (trainer_id, trainer_name, gender, course_id) VALUES
-- Python Programming Trainers
(1, 'Raghu', 'Male', 1),
(2, 'Ananya Rao', 'Female', 1),
(3, 'Suresh Reddy', 'Male', 1),
(4, 'Priya Sharma', 'Female', 1),

-- Java Programming Trainers
(5, 'Kiran Varma', 'Male', 2),
(6, 'Lakshmi Devi', 'Female', 2),
(7, 'Venkat Ram', 'Male', 2),
(8, 'Sneha Patel', 'Female', 2),

-- Web Development Trainers
(9, 'Rajesh Kumar', 'Male', 3),
(10, 'Divya Nair', 'Female', 3),
(11, 'Pradeep Joshi', 'Male', 3),
(12, 'Kavitha Swamy', 'Female', 3);

-- Insert Evaluation Sections
INSERT INTO sections (section_id, section_name) VALUES
(1, 'TEACHING'),
(2, 'CONTENT'),
(3, 'PRACTICAL');

-- Insert Evaluation Questions
INSERT INTO feedback_questions (question_id, section_id, question_text) VALUES
(1, 1, 'How clear are the explanation methods used by the faculty?'),
(2, 1, 'Does the trainer address and resolve student doubts effectively?'),
(3, 2, 'Is the course content well-structured and relevant?'),
(4, 2, 'Are the lecture materials and slides helpful for learning?'),
(5, 3, 'Does the trainer provide useful hands-on coding practice?'),
(6, 3, 'Are lab exercises aligned with real-world applications?');

-- Insert Seeded Feedback Data (Ensures every trainer has test scores)
INSERT INTO feedback (course_id, trainer_id, roll_number, question_id, rating, comment_optional) VALUES
-- Reviews for Raghu (Python)
(1, 1, '21121A0501', 1, 5, 'Raghu sir explains Python concepts with great clarity.'),
(1, 1, '21121A0501', 2, 5, 'Very responsive to doubts.'),
(1, 1, '21121A0501', 3, 4, 'Good course material.'),
(1, 1, '21121A0501', 4, 4, 'Slides are easy to follow.'),
(1, 1, '21121A0501', 5, 5, 'Practical coding sessions are excellent.'),
(1, 1, '21121A0501', 6, 4, 'Labs are very helpful.'),

(1, 1, '21121A0502', 1, 4, 'Great teaching methodology.'),
(1, 1, '21121A0502', 2, 4, 'Clears doubts quickly.'),
(1, 1, '21121A0502', 3, 5, 'Content structure is awesome.'),
(1, 1, '21121A0502', 4, 4, 'Good notes.'),
(1, 1, '21121A0502', 5, 4, 'Need a bit more lab time.'),
(1, 1, '21121A0502', 6, 4, 'Overall good practice.'),

-- Reviews for Ananya Rao (Python)
(1, 2, '21121A0503', 1, 4, 'Detailed explanations.'),
(1, 2, '21121A0503', 2, 3, 'Pacing can be slightly fast.'),
(1, 2, '21121A0503', 3, 4, 'Content is good.'),
(1, 2, '21121A0503', 4, 4, 'Useful resources.'),
(1, 2, '21121A0503', 5, 3, 'Decent practical guidance.'),
(1, 2, '21121A0503', 6, 4, 'Good examples.'),

-- Reviews for Kiran Varma (Java)
(2, 5, '21121A0504', 1, 5, 'Master of OOPs concepts.'),
(2, 5, '21121A0504', 2, 5, 'Excellent doubt clearance.'),
(2, 5, '21121A0504', 3, 4, 'Java syllabus covered thoroughly.'),
(2, 5, '21121A0504', 4, 5, 'Great code samples.'),
(2, 5, '21121A0504', 5, 4, 'Practical sessions were solid.'),
(2, 5, '21121A0504', 6, 5, 'Strong lab practice.');