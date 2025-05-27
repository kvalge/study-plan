from flask import Flask, render_template, request, redirect, url_for, session
from db.config import get_connection

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # vajalik sessioni kasutamiseks


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, title FROM field")
    fields = c.fetchall()

    results = []

    if request.method == 'POST':
        selected_field_ids = request.form.getlist('fields')

        if selected_field_ids:
            session['selected_field_ids'] = selected_field_ids  # salvesta sessiooni
            return redirect(url_for('index'))  # PRG – redirect GET-ile

    selected_field_ids = session.get('selected_field_ids')

    if selected_field_ids:
        placeholders = ','.join('?' for _ in selected_field_ids)

        query = f'''
            SELECT course.title, 
                   MAX(field_course.weeks) as max_weeks,
                   MAX(field_course.relevance) as max_relevance
            FROM field_course
            JOIN course ON course.id = field_course.course_id
            WHERE field_course.field_id IN ({placeholders})
            GROUP BY course.title
            ORDER BY max_relevance DESC
        '''
        c.execute(query, selected_field_ids)
        results = c.fetchall()

    conn.close()
    return render_template('index.html', fields=fields, results=results)


@app.route('/clear', methods=['POST'])
def clear():
    session.pop('selected_field_ids', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
