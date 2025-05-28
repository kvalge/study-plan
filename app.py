from flask import Flask, render_template, request, redirect, url_for, session
from db.config import get_connection

app = Flask(__name__)
app.secret_key = 'your-secret-key'


@app.route('/', methods=['GET', 'POST'])
def index():
    fields = get_fields()

    results = []
    total_weeks = 0

    if request.method == 'POST':
        selected_field_ids = request.form.getlist('fields')
        selected_levels = request.form.getlist('levels')

        session['selected_field_ids'] = selected_field_ids
        session['selected_levels'] = selected_levels

        return redirect(url_for('index'))

    selected_field_ids = session.get('selected_field_ids', [])
    selected_levels = session.get('selected_levels', [])

    if selected_field_ids or selected_levels:
        results = get_courses(selected_field_ids, selected_levels)
        total_weeks = sum(row[2] for row in results)

    return render_template(
        'index.html',
        fields=fields,
        results=results,
        total_weeks=total_weeks,
        selected_field_ids=selected_field_ids,
        selected_levels=selected_levels
    )


@app.route('/clear', methods=['POST'])
def clear():
    session.pop('selected_field_ids', None)
    session.pop('selected_levels', None)

    return redirect(url_for('index'))


def get_fields():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title FROM field")
    fields = c.fetchall()
    conn.close()
    return fields


def get_courses(selected_field_ids, selected_levels):
    conn = get_connection()
    c = conn.cursor()

    query_params = []
    conditions = []

    if selected_field_ids:
        placeholders_fields = ','.join('?' for _ in selected_field_ids)
        conditions.append(f"field_course.field_id IN ({placeholders_fields})")
        query_params.extend(selected_field_ids)

    if selected_levels:
        placeholders_levels = ','.join('?' for _ in selected_levels)
        conditions.append(f"course.level IN ({placeholders_levels})")
        query_params.extend(selected_levels)

    where_clause = ' AND '.join(conditions) if conditions else ''

    query = f'''
        SELECT course.title, course.level,
               MAX(field_course.weeks) AS max_weeks,
               MAX(field_course.relevance) AS max_relevance
        FROM field_course
        JOIN course ON course.id = field_course.course_id
        {'WHERE ' + where_clause if where_clause else ''}
        GROUP BY course.title, course.level
        ORDER BY
            max_relevance DESC,
            CASE course.level
                WHEN 'Beginner' THEN 1
                WHEN 'Intermediate' THEN 2
                WHEN 'Advanced' THEN 3
                ELSE 4
            END
    '''

    c.execute(query, query_params)
    results = c.fetchall()
    conn.close()
    return results


if __name__ == '__main__':
    app.run(debug=True)
