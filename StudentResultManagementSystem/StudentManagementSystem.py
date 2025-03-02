from flask import Flask, render_template, request,  redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret_key"  # Required for session management

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password='Your MySql server password', 
    database="student_db"
)
cursor = db.cursor(dictionary=True)

# ----------------------------------------------
# 1️ Home Page
# ----------------------------------------------
@app.route('/')
def home():
    return render_template("home.html")

# ----------------------------------------------
# 2️ Student Login
# ----------------------------------------------
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form['student_id']
        password = request.form['password']

        cursor.execute("SELECT * FROM students WHERE student_id=%s AND password=%s", (student_id, password))
        student = cursor.fetchone()

        if student:
            session['student_id'] = student_id
            return redirect('/view_results')
        else:
            return "Invalid Student Credentials"

    return render_template("student_login.html")

# ----------------------------------------------
# 3️ Teacher Login
# ----------------------------------------------
@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form['teacher_id']
        password = request.form['password']

        cursor.execute("SELECT * FROM teachers WHERE teacher_id=%s AND password=%s", (username, password))
        teacher = cursor.fetchone()

        if teacher:
            session['teacher_id'] = username
            return redirect(url_for('marks_entry'))
        else:
            return render_template('teacher_login.html', error="Invalid ID or Password")

    return render_template("teacher_login.html")

# ----------------------------------------------
# 4️ Admin Login
# ----------------------------------------------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        admin = cursor.fetchone()

        if admin:
            session['admin_id'] = username
            return redirect('/admin_dashboard')
        else:
            return "Invalid Admin Credentials"

    return render_template("admin_login.html")

# ----------------------------------------------
# 5️ Teacher Marks Entry Page
# ----------------------------------------------
@app.route('/marks_entry', methods=['GET', 'POST'])
def marks_entry():
    if 'teacher_id' not in session:
        return redirect('/teacher_login')  # Redirect if not logged in

    # Fetch students from the database
    cursor.execute("SELECT student_id, name FROM students")
    students = cursor.fetchall()
    return render_template('marks_entry.html', students=students)

    if request.method == 'POST':
        student_id = request.form['student_id']
        english = int(request.form['english'])
        maths = int(request.form['maths'])
        physics = int(request.form['physics'])
        chemistry = int(request.form['chemistry'])
        computer = int(request.form['computer'])

        total_marks = english + maths + physics + chemistry + computer
        percentage = (total_marks / 500) * 100

        cursor.execute("INSERT INTO results (student_id, english, maths, physics, chemistry, computer, total, percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       (student_id, english, maths, physics, chemistry, computer, total_marks, percentage))
        db.commit()

        return "Marks submitted successfully"

    return redirect(url_for('teacher_login'))

# ----------------------------------------------
#  6 Sumbit marks
# ----------------------------------------------

@app.route('/submit_marks', methods=['POST'])
def submit_marks():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))  # Redirect if not logged in

    student_ids = request.form.getlist('student_id[]')
    english_marks = request.form.getlist('english[]')
    maths_marks = request.form.getlist('maths[]')
    physics_marks = request.form.getlist('physics[]')
    chemistry_marks = request.form.getlist('chemistry[]')
    computer_marks = request.form.getlist('computer[]')
    total_marks = request.form.getlist('total[]')
    percentages = request.form.getlist('percentage[]')

    for i in range(len(student_ids)):
        student_id = student_ids[i]
        english = int(english_marks[i])
        maths = int(maths_marks[i])
        physics = int(physics_marks[i])
        chemistry = int(chemistry_marks[i])
        computer = int(computer_marks[i])
        total = int(total_marks[i])
        percentage = percentages[i].replace('%', '')  # Remove the percentage symbol
        percentage = float(percentage)  # Convert the cleaned value to float


        cursor.execute("""
            INSERT INTO results (student_id, english, maths, physics, chemistry, computer, total, percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            english = VALUES(english), maths = VALUES(maths), physics = VALUES(physics),
            chemistry = VALUES(chemistry), computer = VALUES(computer), total = VALUES(total),
            percentage = VALUES(percentage)
        """, (student_id, english, maths, physics, chemistry, computer, total, percentage))

    db.commit()
    return "Marks successfully submitted!"


# ----------------------------------------------
# 7 View Student Results
# ----------------------------------------------
@app.route('/results')
def view_results():
    if 'student_id' not in session:
        return redirect('/student_login')  # Redirect if not logged in

    student_id = session['student_id']
    cursor.execute("SELECT * FROM results WHERE student_id=%s", (student_id,))
    results = cursor.fetchall()

    return render_template("results.html", results=results)

# ----------------------------------------------
# 8 Admin Dashboard
# ----------------------------------------------
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect('/admin_login')

    cursor.execute("SELECT * FROM results")
    all_results = cursor.fetchall()

    return render_template("admin_dashboard.html", all_results=all_results)

# ----------------------------------------------
# 9 Logout Function
# ----------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ----------------------------------------------
# Run Flask App
# ----------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
