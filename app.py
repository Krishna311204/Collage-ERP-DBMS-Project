from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college_attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, faculty, student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    enrollment_date = db.Column(db.Date, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), default='active')  # active, dropped, completed
    grade = db.Column(db.String(2))  # A, B, C, D, F, etc.
    
    # Relationships
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # present, absent, late
    marked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'faculty':
            return redirect(url_for('faculty_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    total_students = Student.query.count()
    total_courses = Course.query.count()
    total_faculty = User.query.filter_by(role='faculty').count()
    total_enrollments = Enrollment.query.count()
    
    return render_template('admin_dashboard.html', 
                         total_students=total_students,
                         total_courses=total_courses,
                         total_faculty=total_faculty,
                         total_enrollments=total_enrollments)

@app.route('/faculty/dashboard')
@login_required
def faculty_dashboard():
    if current_user.role != 'faculty':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    courses = Course.query.filter_by(faculty_id=current_user.id).all()
    return render_template('faculty_dashboard.html', courses=courses)

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    student = Student.query.filter_by(user_id=current_user.id).first()
    if student:
        attendance_records = Attendance.query.filter_by(student_id=student.id).all()
        return render_template('student_dashboard.html', 
                             student=student, 
                             attendance_records=attendance_records)
    
    return redirect(url_for('index'))

@app.route('/admin/students')
@login_required
def admin_students():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    students = Student.query.all()
    return render_template('admin_students.html', students=students)

@app.route('/admin/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Create user account first
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('add_student.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('add_student.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role='student'
        )
        db.session.add(user)
        db.session.flush()  # Get the user ID
        
        # Create student record
        student = Student(
            student_id=request.form['student_id'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=email,
            phone=request.form['phone'],
            department=request.form['department'],
            year=int(request.form['year']),
            semester=int(request.form['semester']),
            user_id=user.id
        )
        db.session.add(student)
        db.session.commit()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('admin_students'))
    
    return render_template('add_student.html')

@app.route('/admin/courses')
@login_required
def admin_courses():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    courses = Course.query.all()
    return render_template('admin_courses.html', courses=courses)

@app.template_filter('get_faculty_name')
def get_faculty_name(faculty_id):
    if faculty_id:
        faculty = User.query.get(faculty_id)
        return faculty.username if faculty else 'Unknown'
    return 'Unassigned'

@app.template_filter('get_course_count')
def get_course_count(faculty_id):
    if faculty_id:
        return Course.query.filter_by(faculty_id=faculty_id).count()
    return 0

@app.template_filter('get_student_name')
def get_student_name(student_id):
    if student_id:
        student = Student.query.get(student_id)
        return f"{student.first_name} {student.last_name}" if student else 'Unknown'
    return 'Unknown'

@app.template_filter('get_course_name')
def get_course_name(course_id):
    if course_id:
        course = Course.query.get(course_id)
        return course.course_name if course else 'Unknown'
    return 'Unknown'

@app.template_filter('get_course_code')
def get_course_code(course_id):
    if course_id:
        course = Course.query.get(course_id)
        return course.course_code if course else 'Unknown'
    return 'Unknown'

@app.route('/admin/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        faculty_id = request.form['faculty_id']
        course = Course(
            course_code=request.form['course_code'],
            course_name=request.form['course_name'],
            credits=int(request.form['credits']),
            department=request.form['department'],
            faculty_id=int(faculty_id)
        )
        db.session.add(course)
        db.session.commit()
        
        flash('Course added successfully!', 'success')
        return redirect(url_for('admin_courses'))
    
    faculty = User.query.filter_by(role='faculty').all()
    return render_template('add_course.html', faculty=faculty)

@app.route('/faculty/attendance/<int:course_id>')
@login_required
def faculty_attendance(course_id):
    if current_user.role != 'faculty':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    course = Course.query.get_or_404(course_id)
    if course.faculty_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('faculty_dashboard'))
    
    # Get all students (in a real system, you'd have course enrollments)
    students = Student.query.all()
    today = date.today()
    
    # Get today's attendance
    today_attendance = {}
    for student in students:
        record = Attendance.query.filter_by(
            student_id=student.id,
            course_id=course_id,
            date=today
        ).first()
        today_attendance[student.id] = record.status if record else None
    
    return render_template('faculty_attendance.html', 
                         course=course, 
                         students=students,
                         today_attendance=today_attendance)

@app.route('/faculty/mark_attendance', methods=['POST'])
@login_required
def mark_attendance():
    if current_user.role != 'faculty':
        return jsonify({'success': False, 'message': 'Access denied'})
    
    data = request.get_json()
    student_id = data['student_id']
    course_id = data['course_id']
    status = data['status']
    date_str = data['date']
    
    # Check if attendance already exists for today
    existing = Attendance.query.filter_by(
        student_id=student_id,
        course_id=course_id,
        date=datetime.strptime(date_str, '%Y-%m-%d').date()
    ).first()
    
    if existing:
        existing.status = status
    else:
        attendance = Attendance(
            student_id=student_id,
            course_id=course_id,
            status=status,
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            marked_by=current_user.id
        )
        db.session.add(attendance)
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/faculty')
@login_required
def admin_faculty():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    faculty = User.query.filter_by(role='faculty').all()
    return render_template('admin_faculty.html', faculty=faculty)

@app.route('/admin/add_faculty', methods=['GET', 'POST'])
@login_required
def add_faculty():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        department = request.form['department']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('add_faculty.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('add_faculty.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role='faculty'
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Faculty member added successfully!', 'success')
        return redirect(url_for('admin_faculty'))
    
    return render_template('add_faculty.html')

@app.route('/admin/reports')
@login_required
def admin_reports():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Get attendance statistics
    total_attendance = Attendance.query.count()
    present_count = Attendance.query.filter_by(status='present').count()
    absent_count = Attendance.query.filter_by(status='absent').count()
    late_count = Attendance.query.filter_by(status='late').count()
    
    attendance_rate = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    return render_template('admin_reports.html',
                         total_attendance=total_attendance,
                         present_count=present_count,
                         absent_count=absent_count,
                         late_count=late_count,
                         attendance_rate=round(attendance_rate, 2))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if not check_password_hash(current_user.password_hash, current_password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('profile'))
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('profile'))
        
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long', 'error')
            return redirect(url_for('profile'))
        
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html')

@app.route('/admin/enrollments')
@login_required
def admin_enrollments():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    enrollments = Enrollment.query.all()
    return render_template('admin_enrollments.html', enrollments=enrollments)

@app.route('/admin/add_enrollment', methods=['GET', 'POST'])
@login_required
def add_enrollment():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        
        # Check if enrollment already exists
        existing = Enrollment.query.filter_by(
            student_id=student_id, 
            course_id=course_id,
            status='active'
        ).first()
        
        if existing:
            flash('Student is already enrolled in this course', 'error')
            return render_template('add_enrollment.html')
        
        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id
        )
        db.session.add(enrollment)
        db.session.commit()
        
        flash('Enrollment added successfully!', 'success')
        return redirect(url_for('admin_enrollments'))
    
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('add_enrollment.html', students=students, courses=courses)

@app.route('/student/enrolled_courses')
@login_required
def student_enrolled_courses():
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Get student record
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Student record not found', 'error')
        return redirect(url_for('student_dashboard'))
    
    enrollments = Enrollment.query.filter_by(student_id=student.id, status='active').all()
    return render_template('student_enrolled_courses.html', enrollments=enrollments)

@app.route('/student/attendance_history')
@login_required
def student_attendance_history():
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Get student record
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Student record not found', 'error')
        return redirect(url_for('student_dashboard'))
    
    # Get attendance records for enrolled courses
    enrollments = Enrollment.query.filter_by(student_id=student.id, status='active').all()
    course_ids = [e.course_id for e in enrollments]
    
    attendance_records = Attendance.query.filter(
        Attendance.student_id == student.id,
        Attendance.course_id.in_(course_ids)
    ).order_by(Attendance.date.desc()).all()
    
    return render_template('student_attendance_history.html', attendance_records=attendance_records)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@college.edu',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username=admin, password=admin123")
    
    app.run(debug=True)
