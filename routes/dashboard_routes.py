from datetime import date, datetime
from flask import Blueprint, render_template, jsonify
from models import db, Student, Department, Subject, Attendance, FeeRecord, ActivityLog, Timetable
from utils import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    today = date.today()
    day_name = today.strftime('%A')
    
    # KPIs
    total_students = Student.query.count()
    total_departments = Department.query.count()
    total_subjects = Subject.query.count()
    
    # Teachers count (distinct teachers)
    teacher_rows = db.session.query(Subject.teacher_name).distinct().all()
    total_teachers = len(teacher_rows)
    
    # Today's Attendance
    today_attendance = Attendance.query.filter_by(date=today).all()
    today_present = sum(1 for a in today_attendance if a.status in ['Present', 'Late'])
    today_absent = sum(1 for a in today_attendance if a.status == 'Absent')
    today_total = len(today_attendance)
    attendance_rate = round((today_present / today_total * 100), 1) if today_total > 0 else 0.0

    # Fee metrics
    all_fees = FeeRecord.query.all()
    total_fees_expected = sum(f.total_amount for f in all_fees)
    total_fees_collected = sum(f.paid_amount for f in all_fees)
    total_fees_pending = sum(f.balance_amount for f in all_fees)

    # Department student distribution
    departments = Department.query.all()
    dept_stats = []
    for d in departments:
        stu_count = Student.query.filter_by(department_id=d.id).count()
        dept_stats.append({
            'name': d.name,
            'code': d.code,
            'count': stu_count
        })

    # Recent activities
    recent_activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(8).all()

    # Today's classes
    today_timetable = Timetable.query.filter_by(day_of_week=day_name).order_by(Timetable.period_number).limit(5).all()

    # Low attendance count (<75%)
    all_students = Student.query.all()
    low_attendance_students = []
    for s in all_students:
        stats = s.attendance_stats
        if stats['total'] >= 3 and stats['percentage'] < 75.0:
            low_attendance_students.append(s)

    # Recent added students
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()

    return render_template(
        'dashboard/index.html',
        total_students=total_students,
        total_teachers=total_teachers,
        total_departments=total_departments,
        total_subjects=total_subjects,
        today_present=today_present,
        today_absent=today_absent,
        today_total=today_total,
        attendance_rate=attendance_rate,
        total_fees_collected=total_fees_collected,
        total_fees_pending=total_fees_pending,
        total_fees_expected=total_fees_expected,
        dept_stats=dept_stats,
        recent_activities=recent_activities,
        today_timetable=today_timetable,
        low_attendance_count=len(low_attendance_students),
        recent_students=recent_students,
        day_name=day_name,
        today_date=today.strftime('%B %d, %Y')
    )


@dashboard_bp.route('/api/dashboard-stats')
@login_required
def dashboard_stats():
    # Helper API for dynamic charts
    departments = Department.query.all()
    dept_labels = [d.code for d in departments]
    dept_data = [Student.query.filter_by(department_id=d.id).count() for d in departments]
    
    # Attendance summary over all records
    present_total = Attendance.query.filter(Attendance.status.in_(['Present', 'Late'])).count()
    absent_total = Attendance.query.filter_by(status='Absent').count()
    excused_total = Attendance.query.filter_by(status='Excused').count()

    # Fee summary
    all_fees = FeeRecord.query.all()
    paid_total = sum(f.paid_amount for f in all_fees)
    pending_total = sum(f.balance_amount for f in all_fees)

    return jsonify({
        'departments': {'labels': dept_labels, 'data': dept_data},
        'attendance': {'present': present_total, 'absent': absent_total, 'excused': excused_total},
        'fees': {'paid': paid_total, 'pending': pending_total}
    })
