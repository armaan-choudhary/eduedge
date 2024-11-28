from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import attendance_bp
from models import get_students, add_attendance, get_attendance, update_attendance, get_attendance_by_user

@attendance_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if current_user.role_id != 2:  # Only teachers can access this
        flash('Unauthorized access')
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        user_id = request.form['user_id']
        date = request.form['date']
        status = request.form['status']
        if get_attendance(user_id, date):
            update_attendance(user_id, date, status)
        else:
            add_attendance(user_id, date, status)
        flash('Attendance updated successfully')
    students = get_students()
    return render_template('attendance.html', students=students)

@attendance_bp.route('/view_attendance')
@login_required
def view_student_attendance():
    if current_user.role_id == 1:  # Students can view their own attendance
        attendance_records = get_attendance_by_user(current_user.id)
        return render_template('view_attendance.html', attendance_records=attendance_records)
    elif current_user.role_id == 2:  # Teachers can view attendance of all students
        students = get_students()
        return render_template('view_attendance_teacher.html', students=students, get_attendance_by_user=get_attendance_by_user)
    else:
        flash('Unauthorized access')
        return redirect(url_for('dashboard.dashboard'))