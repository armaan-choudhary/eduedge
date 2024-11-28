from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import dashboard_bp
from graphing import plot_attendance

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role_id == 1:  # Assuming 1 is the role_id for students
        return render_template('student_dashboard.html', username=current_user.firstname)
    elif current_user.role_id == 2:  # Assuming 2 is the role_id for teachers
        return render_template('teacher_dashboard.html', username=current_user.firstname)
    else:
        flash('Unauthorized access')
        return redirect(url_for('auth.login'))

@dashboard_bp.route('/attendance_graph', methods=['GET', 'POST'])
@login_required
def attendance_graph():
    if current_user.role_id != 2:  # Ensure only teachers can access this
        flash('Unauthorized access')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        date = request.form['date']
        plot_url = plot_attendance(date)
        return render_template('attendance_graph.html', plot_url=plot_url, date=date)
    return render_template('attendance_graph.html', plot_url=None)