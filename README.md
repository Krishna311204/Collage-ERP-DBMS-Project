# College ERP DBMS - Attendance Management System

A comprehensive College Enterprise Resource Planning (ERP) system built with Flask and SQLite, focusing on attendance management for students, faculty, and administrators.

## 🚀 Features

### 🔐 User Management
- **Multi-role Authentication**: Admin, Faculty, and Student roles
- **Secure Login System**: Password hashing and session management
- **Profile Management**: Users can change passwords and view account details

### 👨‍🎓 Student Management
- **Student Registration**: Add new students with comprehensive details
- **Student Profiles**: Track student information, department, year, and semester
- **Student Dashboard**: View attendance records and personal information

### 👨‍🏫 Faculty Management
- **Faculty Accounts**: Create and manage faculty member accounts
- **Course Assignment**: Assign courses to faculty members
- **Attendance Tracking**: Mark student attendance for assigned courses

### 📚 Course Management
- **Course Creation**: Add new courses with codes, names, and credits
- **Department Organization**: Organize courses by academic departments
- **Faculty Assignment**: Link courses to specific faculty members

### 📊 Attendance System
- **Real-time Tracking**: Mark attendance as Present, Absent, or Late
- **Date-based Records**: Track attendance by date and course
- **Faculty Interface**: Easy-to-use attendance marking interface

### 📈 Admin Dashboard
- **System Overview**: View total students, courses, and faculty
- **Comprehensive Reports**: Attendance statistics and analytics
- **User Management**: Manage all users and their roles
- **Quick Actions**: Easy access to common administrative tasks

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login for user sessions
- **Frontend**: Bootstrap 5 with Font Awesome icons
- **Security**: Werkzeug password hashing

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Collage-ERP-DBMS-Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the system**
   - Open your browser and go to `http://localhost:5000`
   - Default admin credentials:
     - Username: `admin`
     - Password: `admin123`

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `role`: User role (admin/faculty/student)
- `created_at`: Account creation timestamp

### Students Table
- `id`: Primary key
- `student_id`: Unique student identifier
- `first_name`, `last_name`: Student names
- `email`, `phone`: Contact information
- `department`: Academic department
- `year`, `semester`: Academic progress
- `enrollment_date`: Date of enrollment
- `user_id`: Reference to Users table

### Courses Table
- `id`: Primary key
- `course_code`: Unique course identifier
- `course_name`: Course title
- `credits`: Credit hours
- `department`: Academic department
- `faculty_id`: Reference to assigned faculty

### Attendance Table
- `id`: Primary key
- `student_id`: Reference to Students table
- `course_id`: Reference to Courses table
- `date`: Attendance date
- `status`: Present/Absent/Late
- `marked_by`: Faculty who marked attendance
- `timestamp`: Record creation time

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string (defaults to SQLite)

### Database
The system uses SQLite by default, which is perfect for development and small to medium deployments. For production, consider using PostgreSQL or MySQL.

## 📱 User Interface

### Admin Interface
- **Dashboard**: System overview and quick actions
- **Student Management**: Add, view, and manage students
- **Course Management**: Create and assign courses
- **Faculty Management**: Manage faculty accounts
- **Reports**: Attendance analytics and statistics

### Faculty Interface
- **Dashboard**: Overview of assigned courses
- **Attendance Tracking**: Mark student attendance
- **Course Management**: View assigned courses

### Student Interface
- **Dashboard**: Personal information and attendance records
- **Profile**: Account details and settings

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Flask-Login for secure user sessions
- **Role-based Access Control**: Different interfaces for different user types
- **Input Validation**: Form validation and sanitization

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Using environment variables for configuration
- Implementing proper logging and monitoring

## 📊 API Endpoints

### Authentication
- `POST /login`: User login
- `GET /logout`: User logout

### Admin Routes
- `GET /admin/dashboard`: Admin dashboard
- `GET /admin/students`: Student management
- `GET /admin/courses`: Course management
- `GET /admin/faculty`: Faculty management
- `GET /admin/reports`: Attendance reports

### Faculty Routes
- `GET /faculty/dashboard`: Faculty dashboard
- `GET /faculty/attendance/<course_id>`: Course attendance
- `POST /faculty/mark_attendance`: Mark attendance

### Student Routes
- `GET /student/dashboard`: Student dashboard

### General Routes
- `GET /`: Home page
- `GET /profile`: User profile management

## 🧪 Testing

The system includes basic functionality testing. To run tests:

```bash
# Install testing dependencies
pip install pytest

# Run tests
pytest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- **Mobile App**: React Native or Flutter mobile application
- **Advanced Analytics**: Machine learning for attendance prediction
- **Integration**: LMS integration (Moodle, Canvas)
- **Notifications**: Email and SMS notifications
- **API**: RESTful API for external integrations
- **Multi-language**: Internationalization support
- **Backup**: Automated database backup system
- **Audit Logs**: Comprehensive activity logging

## 📊 System Requirements

### Minimum
- Python 3.7+
- 512MB RAM
- 100MB disk space

### Recommended
- Python 3.9+
- 1GB RAM
- 500MB disk space
- SSD storage for better performance

## 🚀 Quick Start Guide

1. **Install Python and pip**
2. **Clone the repository**
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run the application**: `python app.py`
5. **Access the system**: `http://localhost:5000`
6. **Login as admin**: username: `admin`, password: `admin123`
7. **Start managing your college ERP system!**

---

**Note**: This is a development version. For production use, please ensure proper security measures, database backups, and monitoring are in place.
