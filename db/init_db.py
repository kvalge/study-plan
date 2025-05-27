from db.config import get_connection

def initialize_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS field_course')
    c.execute('DROP TABLE IF EXISTS course')
    c.execute('DROP TABLE IF EXISTS field')

    c.execute('''
        CREATE TABLE course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE field (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE field_course (
            field_id INTEGER,
            course_id INTEGER,
            weeks INTEGER NOT NULL,
            relevance INTEGER NOT NULL,
            FOREIGN KEY (field_id) REFERENCES field (id),
            FOREIGN KEY (course_id) REFERENCES course (id),
            PRIMARY KEY (field_id, course_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    initialize_db()
