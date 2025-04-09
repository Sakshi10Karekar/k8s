from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Database credentials from environment variables (default values provided)
HOST_NAME = os.getenv('DB_HOST', 'localhost')
DATABASE_NAME = os.getenv('DB_NAME', 'postgres')
PORT = os.getenv('DB_PORT', '5432')
PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DATABASE_USER = os.getenv('DB_USER', 'postgres')


def get_connection():
    """Establish connection with PostgreSQL database."""
    return psycopg2.connect(
        host=HOST_NAME,
        dbname=DATABASE_NAME,
        port=PORT,
        password=PASSWORD,
        user=DATABASE_USER
    )


def create_table():
    """Create student_info table if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student_info (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            qualification TEXT,
            board TEXT,
            passing_year TEXT,
            percentage TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def insert_student(name, email, phone, qualification, board, passing_year, percentage):
    """Insert a new student record."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO student_info (
            name, email, phone, qualification, board, passing_year, percentage
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, email, phone, qualification, board, passing_year, percentage))
    conn.commit()
    cur.close()
    conn.close()


def fetch_all_students():
    """Fetch all student records."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM student_info")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


@app.route('/')
def personal():
    return render_template('personal.html')


@app.route('/educational', methods=['POST'])
def educational():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    return render_template('educational.html', name=name, email=email, phone=phone)


@app.route('/submited_data', methods=['POST'])
def mydata():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    qualification = request.form['qualification']
    board = request.form['board']
    passing_year = request.form['year']
    percentage = request.form['score']

    insert_student(name, email, phone, qualification, board, passing_year, percentage)

    return render_template(
        'submited_data.html',
        name=name,
        email=email,
        phone=phone,
        qualification=qualification,
        board=board,
        p_year=passing_year,
        percentage=percentage
    )


@app.route('/show_data', methods=['POST'])
def database_data():
    student_data = fetch_all_students()
    return render_template('show_data.html', student=student_data)


@app.route('/thankyou', methods=['POST'])
def last():
    return render_template('thankyou.html')


if __name__ == "__main__":
    create_table()
    app.run(debug=True, host='0.0.0.0', port=5000)
