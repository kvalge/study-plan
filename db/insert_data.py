from db.config import get_connection


def clear_tables(cursor):
    cursor.execute("DELETE FROM field_course")
    cursor.execute("DELETE FROM field")
    cursor.execute("DELETE FROM course")

    cursor.execute("DELETE FROM sqlite_sequence WHERE name='field'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='course'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='field_course'")


def populate():
    conn = get_connection()
    c = conn.cursor()

    clear_tables(c)

    fields = [
        "Data Analyst",
        "Data Scientist",
        "Backend Developer",
        "Frontend Developer",
        "Machine Learning Engineer",
        "AI Engineer"
    ]
    field_ids = {}
    for title in fields:
        c.execute("INSERT INTO field (title) VALUES (?)", (title,))
        field_ids[title] = c.lastrowid

    courses = [
        ("Introduction to Python", "Beginner"),
        ("Advanced Python", "Advanced"),
        ("Pandas Library", "Intermediate"),
        ("NumPy Library", "Intermediate"),
        ("Data Visualization", "Intermediate"),
        ("SQL for Data Analysis", "Intermediate"),
        ("Statistics and Probability", "Intermediate"),
        ("Excel for Data Analysis", "Beginner"),
        ("Data Wrangling", "Intermediate"),
        ("Business Intelligence Tools", "Intermediate"),
        ("Linear Algebra", "Intermediate"),
        ("Machine Learning Basics", "Intermediate"),
        ("Deep Learning Fundamentals", "Advanced"),
        ("Big Data Tools", "Intermediate"),
        ("Databases", "Intermediate"),
        ("REST API Development", "Intermediate"),
        ("Authentication and Authorization", "Intermediate"),
        ("Version Control", "Beginner"),
        ("Object-Oriented Programming", "Intermediate"),
        ("Server Deployment Basics", "Beginner"),
        ("Docker & Containers", "Intermediate"),
        ("HTML & CSS", "Beginner"),
        ("JavaScript", "Intermediate"),
        ("Responsive Web Design", "Beginner"),
        ("React Basics", "Intermediate"),
        ("State Management (Redux)", "Advanced"),
        ("Browser DevTools", "Beginner"),
        ("UI/UX Principles", "Beginner"),
        ("Web Accessibility", "Beginner"),
        ("Model Evaluation and Tuning", "Advanced"),
        ("Data Pipelines", "Advanced"),
        ("MLOps Basics", "Advanced"),
        ("Neural Networks and Architectures", "Advanced"),
        ("Natural Language Processing", "Advanced"),
        ("Computer Vision", "Advanced"),
        ("AI Ethics & Privacy", "Beginner"),
        ("AI Ethics and Safety", "Intermediate"),
        ("Cloud Fundamentals", "Intermediate"),
        ("CI/CD Fundamentals", "Intermediate"),
        ("Testing & QA", "Beginner"),
        ("Reinforcement Learning", "Advanced"),
        ("Flask Web Development", "Intermediate"),
        ("Django Web Framework", "Advanced"),
        ("TypeScript", "Intermediate"),
        ("C++ for Data Science", "Advanced"),
        ("Java for Backend", "Intermediate"),
    ]
    course_ids = {}
    for title, level in courses:
        c.execute("INSERT INTO course (title, level) VALUES (?, ?)", (title, level))
        course_ids[title] = c.lastrowid

    field_course_map = {
        "Data Analyst": [
            ("Introduction to Python", 3, 5),
            ("Pandas Library", 3, 5),
            ("Excel for Data Analysis", 3, 4),
            ("SQL for Data Analysis", 4, 5),
            ("Data Wrangling", 4, 4),
            ("Data Visualization", 4, 5),
            ("Business Intelligence Tools", 4, 3),
            ("Statistics and Probability", 5, 4),
            ("AI Ethics & Privacy", 2, 3),
        ],
        "Data Scientist": [
            ("Introduction to Python", 3, 5),
            ("Advanced Python", 4, 4),
            ("Pandas Library", 3, 5),
            ("NumPy Library", 3, 5),
            ("Statistics and Probability", 5, 5),
            ("Data Wrangling", 4, 4),
            ("Machine Learning Basics", 5, 5),
            ("Deep Learning Fundamentals", 5, 4),
            ("Natural Language Processing", 4, 4),
            ("Big Data Tools", 4, 3),
            ("AI Ethics & Privacy", 2, 3),
        ],
        "Backend Developer": [
            ("Java for Backend", 5, 4),
            ("Introduction to Python", 4, 4),
            ("Flask Web Development", 4, 4),
            ("Django Web Framework", 5, 5),
            ("REST API Development", 4, 5),
            ("Databases", 4, 5),
            ("Authentication and Authorization", 3, 4),
            ("Docker & Containers", 3, 4),
            ("CI/CD Fundamentals", 3, 3),
            ("Cloud Fundamentals", 3, 3),
        ],
        "Frontend Developer": [
            ("HTML & CSS", 3, 5),
            ("JavaScript", 5, 5),
            ("Responsive Web Design", 3, 4),
            ("React Basics", 4, 5),
            ("State Management (Redux)", 3, 4),
            ("TypeScript", 3, 4),
            ("UI/UX Principles", 3, 4),
            ("Web Accessibility", 2, 3),
            ("Browser DevTools", 2, 3),
            ("Testing & QA", 2, 3),
        ],
        "Machine Learning Engineer": [
            ("Introduction to Python", 4, 5),
            ("Advanced Python", 4, 4),
            ("Linear Algebra", 5, 5),
            ("Statistics and Probability", 5, 5),
            ("Machine Learning Basics", 5, 5),
            ("Model Evaluation and Tuning", 4, 4),
            ("Data Pipelines", 4, 4),
            ("MLOps Basics", 4, 4),
            ("Deep Learning Fundamentals", 6, 5),
            ("Neural Networks and Architectures", 6, 5),
            ("Big Data Tools", 3, 3),
            ("Cloud Fundamentals", 4, 4),
        ],
        "AI Engineer": [
            ("Introduction to Python", 4, 5),
            ("Advanced Python", 4, 4),
            ("Deep Learning Fundamentals", 6, 5),
            ("Neural Networks and Architectures", 6, 5),
            ("Natural Language Processing", 4, 4),
            ("Computer Vision", 4, 4),
            ("Reinforcement Learning", 5, 4),
            ("AI Ethics and Safety", 3, 4),
            ("Cloud Fundamentals", 3, 3),
            ("AI Ethics & Privacy", 2, 3),
        ],
    }

    for field, course_list in field_course_map.items():
        field_id = field_ids[field]
        for course_title, weeks, relevance in course_list:
            course_id = course_ids[course_title]
            c.execute(
                "INSERT INTO field_course (field_id, course_id, weeks, relevance) VALUES (?, ?, ?, ?)",
                (field_id, course_id, weeks, relevance)
            )

    conn.commit()
    conn.close()
    print("Data populated successfully.")


if __name__ == '__main__':
    populate()
