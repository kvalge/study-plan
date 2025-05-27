from db.config import get_connection

def clear_tables(cursor):
    cursor.execute("DELETE FROM field_course")
    cursor.execute("DELETE FROM field")
    cursor.execute("DELETE FROM course")

    # Kui tahad auto-increment id’d nullida (SQLite's sqlite_sequence):
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
        "Introduction to Python",
        "Data Visualization",
        "SQL for Data Analysis",
        "Statistics and Probability",
        "Excel for Data Analysis",
        "Data Wrangling",
        "Business Intelligence Tools",
        "Linear Algebra",
        "Machine Learning Basics",
        "Deep Learning Fundamentals",
        "Big Data Tools",
        "Databases",
        "REST API Development",
        "Authentication and Authorization",
        "Version Control",
        "Object-Oriented Programming",
        "Server Deployment Basics",
        "Docker & Containers",
        "HTML & CSS",
        "JavaScript",
        "Responsive Web Design",
        "React Basics",
        "State Management (Redux)",
        "Browser DevTools",
        "UI/UX Principles",
        "Web Accessibility",
        "Model Evaluation and Tuning",
        "Data Pipelines",
        "MLOps Basics",
        "Neural Networks and Architectures",
        "Natural Language Processing",
        "Computer Vision",
        "AI Ethics & Privacy",
        "Cloud Fundamentals",
        "CI/CD Fundamentals",
        "Testing & QA",
        "Reinforcement Learning"
    ]
    course_ids = {}
    for title in courses:
        c.execute("INSERT INTO course (title) VALUES (?)", (title,))
        course_ids[title] = c.lastrowid

    field_course_map = {
        "Data Analyst": [
            ("Introduction to Python",      3, 5),
            ("Excel for Data Analysis",      3, 4),
            ("SQL for Data Analysis",        4, 5),
            ("Data Wrangling",               4, 4),
            ("Statistics and Probability",   5, 4),
            ("Data Visualization",           4, 5),
            ("Business Intelligence Tools",  4, 3),
            ("Data Ethics & Privacy",        2, 3),
        ],
        "Data Scientist": [
            ("Introduction to Python",       3, 5),
            ("Linear Algebra",               5, 4),
            ("Statistics and Probability",   5, 5),
            ("Data Wrangling",               4, 4),
            ("SQL for Data Analysis",        3, 4),
            ("Data Visualization",           4, 4),
            ("Machine Learning Basics",      5, 5),
            ("Deep Learning Fundamentals",   5, 4),
            ("Big Data Tools",               4, 3),
            ("Data Ethics & Privacy",        2, 3),
            ("Cloud Fundamentals",           3, 3),
        ],
        "Backend Developer": [
            ("Introduction to Python",       4, 4),
            ("Databases",                    4, 5),
            ("REST API Development",         4, 5),
            ("Authentication and Authorization", 3, 4),
            ("Version Control",              2, 4),
            ("Object-Oriented Programming",  4, 4),
            ("Server Deployment Basics",     3, 3),
            ("Docker & Containers",          3, 4),
            ("CI/CD Fundamentals",           3, 3),
            ("Testing & QA",                 2, 3),
            ("Cloud Fundamentals",           3, 3),
        ],
        "Frontend Developer": [
            ("HTML & CSS",                   3, 5),
            ("JavaScript",                   5, 5),
            ("Responsive Web Design",        3, 4),
            ("Version Control",              2, 3),
            ("React Basics",                 4, 5),
            ("State Management (Redux)",     3, 4),
            ("Browser DevTools",             2, 3),
            ("UI/UX Principles",             3, 4),
            ("Web Accessibility",            2, 3),
            ("Testing & QA",                 2, 3),
        ],
        "Machine Learning Engineer": [
            ("Introduction to Python",       4, 5),
            ("Linear Algebra",               5, 5),
            ("Statistics and Probability",   5, 5),
            ("Machine Learning Basics",      5, 5),
            ("Deep Learning Fundamentals",   6, 5),
            ("Model Evaluation and Tuning",  4, 4),
            ("Data Pipelines",               4, 4),
            ("MLOps Basics",                 4, 4),
            ("Big Data Tools",               3, 3),
            ("Cloud Fundamentals",           4, 4),
            ("Data Ethics & Privacy",        2, 3),
        ],
        "AI Engineer": [
            ("Introduction to Python",       4, 5),
            ("Linear Algebra",               5, 5),
            ("Deep Learning Fundamentals",   6, 5),
            ("Neural Networks and Architectures", 6, 5),
            ("Natural Language Processing",  4, 4),
            ("Computer Vision",              4, 4),
            ("Reinforcement Learning",       5, 4),
            ("AI Ethics and Safety",         3, 4),
            ("Cloud Fundamentals",           3, 3),
            ("Data Ethics & Privacy",        2, 3),
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

if __name__ == '__main__':
    populate()
