from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('studyplan.db')
    conn.row_factory = sqlite3.Row  # lubab kasutada dict-stiilis viitamist
    return conn

@app.route('/', methods=['GET'])
def index():
    month = request.args.get('month')
    week = request.args.get('week')

    query = 'SELECT * FROM study_plan WHERE 1=1'
    params = []

    if month:
        query += ' AND month = ?'
        params.append(month)

    if week:
        query += ' AND week = ?'
        params.append(int(week))

    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('index.html', results=rows)

if __name__ == '__main__':
    app.run(debug=True)
