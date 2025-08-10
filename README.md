College ERP - Attendance Management System
A comprehensive College Enterprise Resource Planning (ERP) application built with Flask and SQLite, designed to manage attendance for students, faculty, and administrators.
It features role-based access, secure authentication, and an intuitive interface for academic institutions.

Key Features
User Management

Multi-role authentication: Admin, Faculty, Student

Secure login with password hashing and session handling

Profile management for updating personal information

Student Management

Register students with complete academic and personal details

Maintain student profiles including department, year, and semester

Student dashboard to view attendance records

Faculty Management

Create and manage faculty accounts

Assign courses to faculty members

Mark and update student attendance

Course Management

Create and organize courses by department

Assign courses to faculty

Track course-wise attendance

Attendance System

Mark attendance as Present, Absent, or Late

Date-wise and course-wise attendance tracking

Easy-to-use faculty interface

Admin Dashboard

Overview of students, faculty, and courses

Attendance analytics and reports

User and role management

Technology Stack
Backend: Flask (Python)

Database: SQLite with SQLAlchemy ORM

Authentication: Flask-Login

Frontend: Bootstrap 5, Font Awesome

Security: Werkzeug password hashing

Database Overview
Users Table – Stores login details, role, and account information
Students Table – Stores student details linked to user accounts
Courses Table – Stores course details and assigned faculty
Attendance Table – Stores attendance status by student, course, and date

Interfaces
Admin

Manage students, faculty, and courses

View attendance reports and system statistics

Faculty

View assigned courses

Mark and manage attendance records

Student

View attendance history and personal profile

Security
Secure password storage with hashing

Session-based authentication

Role-based access control

Input validation and sanitization

Future Enhancements
Mobile application (React Native / Flutter)

Attendance prediction using machine learning

Integration with LMS platforms

Email and SMS notifications

Multi-language support

Automated database backups

Audit logging

