from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Attendance, Student, Subject, Department
from utils import login_required, log_activity

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@attendance_bp.route('/')
@login_required
def index():
    selected_date_str = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    dept_id = request.args.get('department_id', type=int)
    subject_id = request.args.get('subject_id', type=int)

    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()

    query = Attendance.query.filter_by(date=selected_date)

    if dept_id:
        query = query.join(Student).filter(Student.department_id == dept_id)
    if subject_id:
        query = query.filter(Attendance.subject_id == subject_id)

    records = query.order_by(Attendance.created_at.desc()).all()
    departments = Department.query.order_by(Department.name).all()
    subjects = Subject.query.order_by(Subject.name).all()

    # Summary metrics for the selected query
    present_cnt = sum(1 for r in records if r.status in ['Present', 'Late'])
    absent_cnt = sum(1 for r in records if r.status == 'Absent')
    excused_cnt = sum(1 for r in records if r.status == 'Excused')
    total_cnt = len(records)
    rate = round((present_cnt / total_cnt * 100), 1) if total_cnt > 0 else 0.0

    return render_template(
        'attendance/index.html',
        records=records,
        departments=departments,
        subjects=subjects,
        selected_date=selected_date.strftime('%Y-%m-%d'),
        selected_dept=dept_id,
        selected_subject=subject_id,
        present_cnt=present_cnt,
        absent_cnt=absent_cnt,
        excused_cnt=excused_cnt,
        total_cnt=total_cnt,
        rate=rate
    )


@attendance_bp.route('/mark', methods=['GET', 'POST'])
@login_required
def mark():
    departments = Department.query.order_by(Department.name).all()
    subjects = Subject.query.order_by(Subject.name).all()

    dept_id = request.args.get('department_id', type=int)
    subject_id = request.args.get('subject_id', type=int)
    year = request.args.get('year', type=int)
    date_str = request.args.get('date', date.today().strftime('%Y-%m-%d'))

    try:
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        attendance_date = date.today()

    students = []
    existing_attendance = {}

    if dept_id:
        stu_query = Student.query.filter_by(department_id=dept_id, status='Active')
        if year:
            stu_query = stu_query.filter_by(year=year)
        students = stu_query.order_by(Student.student_id).all()

        if subject_id:
            # Check existing attendance for this subject and date
            existing_records = Attendance.query.filter_by(
                subject_id=subject_id,
                date=attendance_date
            ).all()
            existing_attendance = {r.student_id: r.status for r in existing_records}

    if request.method == 'POST':
        post_dept_id = request.form.get('department_id', type=int)
        post_subject_id = request.form.get('subject_id', type=int)
        post_date_str = request.form.get('date')
        
        try:
            post_date = datetime.strptime(post_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            post_date = date.today()

        if not post_dept_id or not post_subject_id:
            flash('Please select department and subject to mark attendance.', 'danger')
            return redirect(url_for('attendance.mark'))

        # Fetch students to mark
        student_ids = request.form.getlist('student_ids')
        saved_count = 0

        for sid in student_ids:
            sid_int = int(sid)
            status = request.form.get(f"status_{sid_int}", 'Present')
            remarks = request.form.get(f"remarks_{sid_int}", '').strip()

            # Find or create record
            rec = Attendance.query.filter_by(
                student_id=sid_int,
                subject_id=post_subject_id,
                date=post_date
            ).first()

            if rec:
                rec.status = status
                rec.remarks = remarks
                rec.recorded_by = request.form.get('recorded_by', 'Admin')
            else:
                rec = Attendance(
                    student_id=sid_int,
                    subject_id=post_subject_id,
                    date=post_date,
                    status=status,
                    remarks=remarks,
                    recorded_by=request.form.get('recorded_by', 'Admin')
                )
                db.session.add(rec)
            saved_count += 1

        db.session.commit()

        sub = db.session.get(Subject, post_subject_id)
        sub_name = sub.name if sub else 'Subject'
        log_activity('Attendance', f"Marked attendance for {saved_count} students in {sub_name} on {post_date}.", 'bi-calendar-check-fill')
        flash(f"Successfully recorded attendance for {saved_count} students!", 'success')
        return redirect(url_for('attendance.index', date=post_date.strftime('%Y-%m-%d'), subject_id=post_subject_id))

    return render_template(
        'attendance/mark.html',
        departments=departments,
        subjects=subjects,
        students=students,
        existing_attendance=existing_attendance,
        selected_dept=dept_id,
        selected_subject=subject_id,
        selected_year=year,
        selected_date=attendance_date.strftime('%Y-%m-%d')
    )


@attendance_bp.route('/low-attendance')
@login_required
def low_attendance():
    threshold = request.args.get('threshold', 75.0, type=float)
    dept_id = request.args.get('department_id', type=int)

    query = Student.query.filter_by(status='Active')
    if dept_id:
        query = query.filter_by(department_id=dept_id)
    students = query.order_by(Student.student_id).all()

    defaulters = []
    for s in students:
        stats = s.attendance_stats
        # Only consider students with at least 1 record
        if stats['total'] > 0 and stats['percentage'] < threshold:
            defaulters.append({
                'student': s,
                'stats': stats,
                'shortage': round(threshold - stats['percentage'], 1)
            })

    departments = Department.query.order_by(Department.name).all()

    return render_template(
        'attendance/low_attendance.html',
        defaulters=defaulters,
        departments=departments,
        selected_dept=dept_id,
        threshold=threshold
    )


@attendance_bp.route('/report')
@login_required
def report():
    dept_id = request.args.get('department_id', type=int)
    subject_id = request.args.get('subject_id', type=int)
    month_str = request.args.get('month', date.today().strftime('%Y-%m'))  # 'YYYY-MM'

    try:
        year_num, month_num = map(int, month_str.split('-'))
    except ValueError:
        today = date.today()
        year_num, month_num = today.year, today.month

    # Get students
    stu_query = Student.query.filter_by(status='Active')
    if dept_id:
        stu_query = stu_query.filter_by(department_id=dept_id)
    students = stu_query.order_by(Student.student_id).all()

    # Per-student summary for this month
    student_summaries = []
    for s in students:
        att_query = Attendance.query.filter_by(student_id=s.id).filter(
            db.extract('year', Attendance.date) == year_num,
            db.extract('month', Attendance.date) == month_num
        )
        if subject_id:
            att_query = att_query.filter_by(subject_id=subject_id)
        month_records = att_query.all()

        total = len(month_records)
        present = sum(1 for a in month_records if a.status in ['Present', 'Late'])
        absent = sum(1 for a in month_records if a.status == 'Absent')
        pct = round((present / total * 100), 1) if total > 0 else 0.0

        student_summaries.append({
            'student': s,
            'total': total,
            'present': present,
            'absent': absent,
            'percentage': pct
        })

    departments = Department.query.order_by(Department.name).all()
    subjects = Subject.query.order_by(Subject.name).all()

    return render_template(
        'attendance/report.html',
        student_summaries=student_summaries,
        departments=departments,
        subjects=subjects,
        selected_dept=dept_id,
        selected_subject=subject_id,
        selected_month=f"{year_num:04d}-{month_num:02d}"
    )


@attendance_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    record = db.get_or_404(Attendance, id)
    db.session.delete(record)
    db.session.commit()
    flash('Attendance record deleted.', 'info')
    return redirect(request.referrer or url_for('attendance.index'))
