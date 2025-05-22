import sqlite3

conn = sqlite3.connect("studyplan.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE study_plan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,
        week INTEGER NOT NULL,
        topic TEXT NOT NULL,
        details TEXT,
        is_completed BOOLEAN NOT NULL
    )
''')

c.execute("INSERT INTO study_plan (month, week, topic, details, is_completed) VALUES (?, ?, ?, ?, ?)",
          ('June', 23, 'Statistics and Pandas', None, False))

c.execute("INSERT INTO study_plan (month, week, topic, details, is_completed) VALUES (?, ?, ?, ?, ?)",
          ('June', 24, 'Linear Regression', None, False))

conn.commit()
conn.close()