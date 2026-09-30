from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Timetable, Department, Subject
from utils import login_required, log_activity

timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')

DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
PERIOD_HOURS = [
    (1, '09:00 AM - 10:00 AM'),
    (2, '10:00 AM - 11:00 AM'),
    (3, '11:15 AM - 12:15 PM'),
    (4, '12:15 PM - 01:15 PM'),
    (5, '02:00 PM - 03:00 PM'),
    (6, '03:00 PM - 04:00 PM'),
]

@timetable_bp.route('/')
@login_required
def index():
    departments = Department.query.order_by(Department.name).all()
    dept_id = request.args.get('department_id', type=int)
    course = request.args.get('course', 'B.Tech')
    year = request.args.get('year', 1, type=int)
    semester = request.args.get('semester', 1, type=int)

    if not dept_id and departments:
        dept_id = departments[0].id

    # Fetch slots for selected filter
    slots = Timetable.query.filter_by(
        department_id=dept_id,
        year=year,
        semester=semester
    ).all()

    # Matrix: day -> period -> slot
    timetable_matrix = {day: {} for day in DAYS_OF_WEEK}
    for slot in slots:
        if slot.day_of_week in timetable_matrix:
            timetable_matrix[slot.day_of_week][slot.period_number] = slot

    selected_dept = db.session.get(Department, dept_id) if dept_id else None

    return render_template(
        'timetable/index.html',
        departments=departments,
        days_of_week=DAYS_OF_WEEK,
        period_hours=PERIOD_HOURS,
        timetable_matrix=timetable_matrix,
        selected_dept_id=dept_id,
        selected_dept=selected_dept,
        selected_course=course,
        selected_year=year,
        selected_sem=semester,
        total_slots=len(slots)
    )


@timetable_bp.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    departments = Department.query.order_by(Department.name).all()
    subjects = Subject.query.order_by(Subject.name).all()

    if request.method == 'POST':
        department_id = request.form.get('department_id', type=int)
        course = request.form.get('course', '').strip()
        year = request.form.get('year', type=int, default=1)
        semester = request.form.get('semester', type=int, default=1)
        day_of_week = request.form.get('day_of_week')
        period_number = request.form.get('period_number', type=int)
        subject_id = request.form.get('subject_id', type=int)
        teacher_name = request.form.get('teacher_name', '').strip()
        room_number = request.form.get('room_number', 'Room 101').strip()
        start_time = request.form.get('start_time', '09:00 AM').strip()
        end_time = request.form.get('end_time', '10:00 AM').strip()

        if not department_id or not subject_id or not day_of_week or not period_number:
            flash('Please fill in all required timetable fields.', 'danger')
            return redirect(url_for('timetable.manage'))

        # If teacher not manually provided, use subject's teacher
        if not teacher_name and subject_id:
            sub = db.session.get(Subject, subject_id)
            if sub:
                teacher_name = sub.teacher_name

        # Check existing slot
        existing = Timetable.query.filter_by(
            department_id=department_id,
            year=year,
            semester=semester,
            day_of_week=day_of_week,
            period_number=period_number
        ).first()

        if existing:
            existing.subject_id = subject_id
            existing.teacher_name = teacher_name
            existing.room_number = room_number
            existing.start_time = start_time
            existing.end_time = end_time
            flash(f"Timetable slot for {day_of_week} Period {period_number} updated!", 'success')
        else:
            new_slot = Timetable(
                department_id=department_id,
                course=course or 'B.Tech',
                year=year,
                semester=semester,
                day_of_week=day_of_week,
                period_number=period_number,
                subject_id=subject_id,
                teacher_name=teacher_name,
                room_number=room_number,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(new_slot)
            flash(f"Timetable slot for {day_of_week} Period {period_number} added!", 'success')

        db.session.commit()
        log_activity('Timetable', f"Configured timetable slot for {day_of_week} Period {period_number} in Dept ID {department_id}.", 'bi-clock-history')
        return redirect(url_for('timetable.index', department_id=department_id, year=year, semester=semester))

    all_slots = Timetable.query.order_by(Timetable.day_of_week, Timetable.period_number).all()

    return render_template(
        'timetable/manage.html',
        departments=departments,
        subjects=subjects,
        days_of_week=DAYS_OF_WEEK,
        period_hours=PERIOD_HOURS,
        all_slots=all_slots
    )


@timetable_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    slot = db.get_or_404(Timetable, id)
    dept_id = slot.department_id
    yr = slot.year
    sem = slot.semester
    
    db.session.delete(slot)
    db.session.commit()
    
    flash('Timetable slot removed successfully.', 'info')
    return redirect(url_for('timetable.index', department_id=dept_id, year=yr, semester=sem))
