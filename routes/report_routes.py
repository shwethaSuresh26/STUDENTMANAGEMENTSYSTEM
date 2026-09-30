from datetime import datetime, date
from flask import Blueprint, render_template, request
from models import db, Student, Department, Subject, Attendance, Marks, FeeRecord, Timetable
from utils import login_required

report_bp = Blueprint('reports', __name__, url_prefix='/reports')

@report_bp.route('/')
@login_required
def index():
    return render_template('reports/index.html')


@report_bp.route('/students')
@login_required
def student_report():
    dept_id = request.args.get('department_id', type=int)
    year = request.args.get('year', type=int)
    gender = request.args.get('gender', '')
    status = request.args.get('status', '')

    query = Student.query
    if dept_id:
        query = query.filter(Student.department_id == dept_id)
    if year:
        query = query.filter(Student.year == year)
    if gender:
        query = query.filter(Student.gender == gender)
    if status:
        query = query.filter(Student.status == status)

    students = query.order_by(Student.student_id).all()
    departments = Department.query.order_by(Department.name).all()

    return render_template(
        'reports/student_report.html',
        students=students,
        departments=departments,
        selected_dept=dept_id,
        selected_year=year,
        selected_gender=gender,
        selected_status=status,
        generated_date=date.today().strftime('%B %d, %Y')
    )


@report_bp.route('/attendance')
@login_required
def attendance_report():
    dept_id = request.args.get('department_id', type=int)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    stu_query = Student.query.filter_by(status='Active')
    if dept_id:
        stu_query = stu_query.filter_by(department_id=dept_id)
    students = stu_query.order_by(Student.student_id).all()

    report_data = []
    for s in students:
        att_query = Attendance.query.filter_by(student_id=s.id)
        if start_date_str:
            try:
                start_d = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                att_query = att_query.filter(Attendance.date >= start_d)
            except ValueError:
                pass
        if end_date_str:
            try:
                end_d = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                att_query = att_query.filter(Attendance.date <= end_d)
            except ValueError:
                pass
        records = att_query.all()
        total = len(records)
        present = sum(1 for r in records if r.status in ['Present', 'Late'])
        absent = sum(1 for r in records if r.status == 'Absent')
        pct = round((present / total * 100), 1) if total > 0 else 0.0

        report_data.append({
            'student': s,
            'total': total,
            'present': present,
            'absent': absent,
            'percentage': pct
        })

    departments = Department.query.order_by(Department.name).all()

    return render_template(
        'reports/attendance_report.html',
        report_data=report_data,
        departments=departments,
        selected_dept=dept_id,
        start_date=start_date_str,
        end_date=end_date_str,
        generated_date=date.today().strftime('%B %d, %Y')
    )


@report_bp.route('/marks')
@login_required
def marks_report():
    exam_name = request.args.get('exam_name', '')
    semester = request.args.get('semester', type=int)
    dept_id = request.args.get('department_id', type=int)

    query = Marks.query.join(Student)
    if exam_name:
        query = query.filter(Marks.exam_name == exam_name)
    if semester:
        query = query.filter(Marks.semester == semester)
    if dept_id:
        query = query.filter(Student.department_id == dept_id)

    marks = query.order_by(Marks.semester, Marks.exam_name, Student.student_id).all()
    departments = Department.query.order_by(Department.name).all()
    exams = [r[0] for r in db.session.query(Marks.exam_name).distinct().all() if r[0]]

    total_marks_cnt = len(marks)
    pass_cnt = sum(1 for m in marks if m.status == 'Pass')
    fail_cnt = sum(1 for m in marks if m.status == 'Fail')
    pass_rate = round((pass_cnt / total_marks_cnt * 100), 1) if total_marks_cnt > 0 else 0.0

    return render_template(
        'reports/marks_report.html',
        marks=marks,
        departments=departments,
        exams=exams,
        selected_exam=exam_name,
        selected_sem=semester,
        selected_dept=dept_id,
        total_marks_cnt=total_marks_cnt,
        pass_cnt=pass_cnt,
        fail_cnt=fail_cnt,
        pass_rate=pass_rate,
        generated_date=date.today().strftime('%B %d, %Y')
    )


@report_bp.route('/fees')
@login_required
def fee_report():
    dept_id = request.args.get('department_id', type=int)
    status = request.args.get('status', '')
    category = request.args.get('category', '')

    query = FeeRecord.query.join(Student)
    if dept_id:
        query = query.filter(Student.department_id == dept_id)
    if status:
        query = query.filter(FeeRecord.status == status)
    if category:
        query = query.filter(FeeRecord.fee_category == category)

    fees = query.order_by(FeeRecord.due_date.desc()).all()
    departments = Department.query.order_by(Department.name).all()

    total_invoiced = sum(f.total_amount for f in fees)
    total_collected = sum(f.paid_amount for f in fees)
    total_pending = sum(f.balance_amount for f in fees)

    categories = ['Tuition Fee', 'Exam Fee', 'Library Fee', 'Hostel Fee', 'Transport Fee', 'Other Fees']

    return render_template(
        'reports/fee_report.html',
        fees=fees,
        departments=departments,
        categories=categories,
        selected_dept=dept_id,
        selected_status=status,
        selected_category=category,
        total_invoiced=total_invoiced,
        total_collected=total_collected,
        total_pending=total_pending,
        generated_date=date.today().strftime('%B %d, %Y')
    )


@report_bp.route('/timetable')
@login_required
def timetable_report():
    dept_id = request.args.get('department_id', type=int)
    year = request.args.get('year', 1, type=int)
    semester = request.args.get('semester', 1, type=int)

    departments = Department.query.order_by(Department.name).all()
    if not dept_id and departments:
        dept_id = departments[0].id

    slots = Timetable.query.filter_by(
        department_id=dept_id,
        year=year,
        semester=semester
    ).order_by(Timetable.day_of_week, Timetable.period_number).all()

    selected_dept = db.session.get(Department, dept_id) if dept_id else None

    return render_template(
        'reports/timetable_report.html',
        slots=slots,
        departments=departments,
        selected_dept=selected_dept,
        selected_dept_id=dept_id,
        selected_year=year,
        selected_sem=semester,
        generated_date=date.today().strftime('%B %d, %Y')
    )
