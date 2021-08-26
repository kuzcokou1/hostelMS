from flask import Flask, render_template, url_for, request, redirect, session, get_flashed_messages, flash
from passlib.hash import sha256_crypt
from datetime import datetime
from functools import wraps
import mysql.connector
import json


app = Flask(__name__)


config = json.loads("""
        {
            "database": {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "hostel"
            },

            "app_secret": "SFDAHhkdshfueuir54W5Q6jilidfidfBSWEQW"
        }
    """)


# App configurations
app.config['SECRET_KEY'] = 'SFDAHhkdshfueuir54W5Q6jilidfidfBSWEQW'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


host = config['database']['host']
user = config['database']['user']
passwd = config['database']['password']
dbName = config['database']['database']


conn = mysql.connector.connect(host = host, user = user, passwd = passwd, database = dbName)
cur = conn.cursor(dictionary = True)


# Limit direct page access
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return render_template('403.html')
    return wrap


@app.route('/', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')

        cur.execute("SELECT * FROM "+dbName+".users WHERE users.username = '%s'" % (username))
        data = cur.fetchall()

        for row in data:
            if sha256_crypt.verify(passwd, row['password']) == False:
                flash('Passwords Not Matching', 'danger')
                return redirect(url_for('signin'))
            else:
                session['logged_in'] = True
                session['username'] = username
                flash('Logged In', 'success')
                return redirect(url_for('index'))
        flash('Login mismatch', 'warning')
    return render_template('signin.html', title="Log In")


@app.route('/signup', methods = ['GET', 'POST'])
@login_required
def signup():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        passwd = sha256_crypt.hash(request.form.get('password'))
        confirm = sha256_crypt.hash(request.form.get('confirm'))

        try:
            cur.execute("INSERT INTO "+dbName+".users(`fname`, `lname`, `username`, `email`, `type`, `password`) VALUES(%s, %s, %s, %s, %s, %s)", (fname, lname, username, email, role, passwd))
            conn.commit()
            flash('Created account for %s' %fname+lname, 'success')
            return redirect(url_for('users'))
        except:
            flash('An error occured', 'warning')
            return redirect(url_for('signup'))
    return render_template('signup.html', title="Sign Up")


@app.route('/dashboard')
@login_required
def index():
    cur.execute("SELECT COUNT(*) as hostels FROM "+dbName+".hostels")
    hostels = cur.fetchall()

    cur.execute("SELECT * FROM "+dbName+".hostels ORDER BY id DESC LIMIT 3")
    recent_hostels = cur.fetchall()

    cur.execute("SELECT COUNT(*) as students FROM "+dbName+".students")
    students = cur.fetchall()

    cur.execute("SELECT * FROM "+dbName+".students ORDER BY id DESC LIMIT 3")
    recent_students = cur.fetchall()

    cur.execute("SELECT COUNT(*) as wardens FROM "+dbName+".wardens")
    wardens = cur.fetchall()

    cur.execute("SELECT * FROM "+dbName+".wardens ORDER BY id DESC LIMIT 3")
    recent_wardens = cur.fetchall()

    cur.execute("SELECT COUNT(*) as users FROM "+dbName+".users")
    users = cur.fetchall()

    cur.execute("SELECT * FROM "+dbName+".users ORDER BY id DESC LIMIT 3")
    recent_users = cur.fetchall()

    return render_template('index.html', title = "Home", hostels = hostels, students = students, wardens = wardens, users = users, recent_students = recent_students, recent_wardens = recent_wardens, recent_users = recent_users, recent_hostels = recent_hostels)


@app.route('/users')
@login_required
def users():
    cur.execute("SELECT * FROM "+dbName+".users")
    users = cur.fetchall()
    return render_template('users.html', title = 'Manage Users', users = users)



@app.route('/user/<int:id>/remove', methods = ['GET', 'POST'])
@login_required
def remove_user(id):
    try:
        cur.execute("DELETE FROM "+dbName+".users WHERE id = %s" %id)
        conn.commit()

        flash("User removed successfully", 'success')
        return redirect(url_for('users'))
    except:
        flash("An error occured!", 'warning')
    return redirect(url_for('users'))


@app.route('/hostels')
@login_required
def hostels():
    cur.execute("SELECT * FROM "+dbName+".hostels")
    hostels = cur.fetchall()
    return render_template('hostels.html', title = "Hostels", hostels = hostels)


@app.route('/hostel/<int:id>/remove', methods = ['GET', 'POST'])
@login_required
def remove_hostel(id):
    try:
        cur.execute("DELETE FROM "+dbName+".hostels WHERE id = %s" %id)
        conn.commit()

        flash("Hostel removed successfully", 'success')
        return redirect(url_for('hostels'))
    except:
        flash("An error occured!", 'warning')
    return redirect(url_for('hostels'))



@app.route('/add_hostel', methods = ['GET', 'POST'])
@login_required
def addHostel():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        capacity = request.form.get('capacity')

        try:
            cur.execute("INSERT INTO "+dbName+".hostels(name, location, capacity) VALUES(%s, %s, %s)", (name, location, capacity))
            conn.commit()
            flash("Hostel added", 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash("An error occured", 'warning')
            return redirect(url_for('addHostel'))
    return render_template('addHostel.html', title = "Add Hostel")



@app.route('/add_warden', methods = ['GET', 'POST'])
@login_required
def addWarden():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        address = request.form.get('address')
        phone = request.form.get('phone')

        try:
            cur.execute("INSERT INTO "+dbName+".`wardens`(`fname`, `lname`, `address`, `phone`) VALUES(%s, %s, %s, %s)", (fname, lname, address, phone))
            conn.commit()
            flash('Warden added', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('An error occured', 'warning')
            return redirect(url_for('addWarden'))
    return render_template('addWarden.html', title = "Add Warden")



@app.route('/students')
@login_required
def students():
    cur.execute("SELECT * FROM "+dbName+".students")
    students = cur.fetchall()
    return render_template('students.html', title = "Students", students = students)



@app.route('/student/<int:id>', methods = ['GET', 'POST'])
@login_required
def student(id):
    cur.execute("SELECT * FROM "+dbName+".students WHERE id = '%s'" % (id))
    student = cur.fetchone()

    if request.method == 'POST':
        uid = request.form.get('id')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        email = request.form.get('email')
        hostel = request.form.get('hostel')

        try:
            cur.execute("UPDATE "+dbName+".`students` SET `fname` = %s, `lname` = %s, `email` = %s, `address` = %s, `city` = %s, `country` = %s, `hostel` = %s WHERE `id` = %s", (fname, lname, email, address, city, country, hostel, uid))
            conn.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for('students'))
        except:
            flash('An error occured', 'warning')
            return redirect(url_for('students'))

    return render_template('student.html', title = "Student", student = student)



@app.route('/student/<int:id>/remove', methods = ['GET', 'POST'])
@login_required
def remove_student(id):
    try:
        cur.execute("DELETE FROM "+dbName+".students WHERE id = %s" %id)
        conn.commit()

        flash("Student removed successfully", 'success')
        return redirect(url_for('index'))
    except:
        flash("An error occured!", 'warning')
    return redirect(url_for('students'))



@app.route('/register', methods = ['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        regNo = request.form.get('regNo')
        course = request.form.get('course')
        hostel = request.form.get('hostel')

        try:
            cur.execute("INSERT INTO "+dbName+".`students`(`fname`, `lname`, `username`, `email`, `address`, `city`, `country`, `regNo`, `course`, `hostel`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, username, email, address, city, country, regNo, course, hostel))
            conn.commit()
            flash('Student Registered', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('An error occured', 'warning')
            return redirect(url_for('register'))
    return render_template('register.html', title = "Register")



@app.route('/profile/<string:username>', methods = ['GET', 'POST'])
@login_required
def profile(username):
    cur.execute("SELECT * FROM "+dbName+".users WHERE users.username = '%s'" %(username))
    user = cur.fetchone()

    if request.method == 'POST':
        uid          = request.form.get('id')
        fname        = request.form.get('fname')
        lname        = request.form.get('lname')
        email        = request.form.get('email')
        new          = request.form.get('new')
        new_hash     = sha256_crypt.hash(new)
        confirm      = request.form.get('confirm')
        confirm_hash = sha256_crypt.hash(confirm)

        try:
            cur.execute("UPDATE "+dbName+".`users` SET `fname` = %s, `lname`= %s, `email`= %s, `passwd`= %s WHERE `id` = %s", (fname, lname, email, confirm_hash, uid))
            conn.commit()
            flash('Updated profile', 'success')
            return redirect(url_for('index'))
        except:
            flash('An error occured', 'warning')
            return render_template('profile.html', title = 'Profile', user = user)
    return render_template('profile.html', title = "Profile", user = user)


# Logout Section
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logged out', 'success')
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)
