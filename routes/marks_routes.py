from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Marks, Student, Subject, Department
from utils import login_required, log_activity

marks_bp = Blueprint('marks', __name__, url_prefix='/marks')

@marks_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '').strip()
    exam_name = request.args.get('exam_name', '').strip()
    subject_id = request.args.get('subject_id', type=int)
    semester = request.args.get('semester', type=int)
    status = request.args.get('status', '').strip()

    query = Marks.query.join(Student)

    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Student.student_id.ilike(search_fmt)) |
            (Student.first_name.ilike(search_fmt)) |
            (Student.last_name.ilike(search_fmt))
        )
    if exam_name:
        query = query.filter(Marks.exam_name == exam_name)
    if subject_id:
        query = query.filter(Marks.subject_id == subject_id)
    if semester:
        query = query.filter(Marks.semester == semester)
    if status:
        query = query.filter(Marks.status == status)

    records = query.order_by(Marks.exam_date.desc(), Marks.created_at.desc()).all()
    subjects = Subject.query.order_by(Subject.name).all()
    exams = [r[0] for r in db.session.query(Marks.exam_name).distinct().all() if r[0]]

    # Statistics
    total_entries = len(records)
    passed_entries = sum(1 for r in records if r.status == 'Pass')
    failed_entries = sum(1 for r in records if r.status == 'Fail')
    pass_pct = round((passed_entries / total_entries * 100), 1) if total_entries > 0 else 0.0

    return render_template(
        'marks/index.html',
        records=records,
        subjects=subjects,
        exams=exams,
        search=search,
        selected_exam=exam_name,
        selected_subject=subject_id,
        selected_sem=semester,
        selected_status=status,
        total_entries=total_entries,
        passed_entries=passed_entries,
        failed_entries=failed_entries,
        pass_pct=pass_pct
    )


@marks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    departments = Department.query.order_by(Department.name).all()
    subjects = Subject.query.order_by(Subject.name).all()
    students = Student.query.filter_by(status='Active').order_by(Student.student_id).all()

    if request.method == 'POST':
        student_id = request.form.get('student_id', type=int)
        subject_id = request.form.get('subject_id', type=int)
        exam_name = request.form.get('exam_name', '').strip()
        semester = request.form.get('semester', type=int, default=1)
        max_marks = request.form.get('max_marks', type=float, default=100.0)
        marks_obtained = request.form.get('marks_obtained', type=float)
        exam_date_str = request.form.get('exam_date')
        remarks = request.form.get('remarks', '').strip()

        if not student_id or not subject_id or not exam_name or marks_obtained is None:
            flash('Please fill in all mandatory marks fields.', 'danger')
            return render_template('marks/add.html', departments=departments, subjects=subjects, students=students, form_data=request.form)

        if marks_obtained > max_marks:
            flash('Obtained marks cannot exceed Maximum Marks.', 'danger')
            return render_template('marks/add.html', departments=departments, subjects=subjects, students=students, form_data=request.form)

        try:
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date() if exam_date_str else date.today()
        except ValueError:
            exam_date = date.today()

        # Calculate percentage, grade, and pass/fail status
        percentage, grade, status = Marks.calculate_grade(marks_obtained, max_marks)

        # Check existing
        existing = Marks.query.filter_by(
            student_id=student_id,
            subject_id=subject_id,
            exam_name=exam_name,
            semester=semester
        ).first()

        if existing:
            existing.max_marks = max_marks
            existing.marks_obtained = marks_obtained
            existing.percentage = percentage
            existing.grade = grade
            existing.status = status
            existing.exam_date = exam_date
            existing.remarks = remarks
            flash(f"Marks record updated for student!", 'success')
        else:
            mark_entry = Marks(
                student_id=student_id,
                subject_id=subject_id,
                exam_name=exam_name,
                semester=semester,
                max_marks=max_marks,
                marks_obtained=marks_obtained,
                percentage=percentage,
                grade=grade,
                status=status,
                exam_date=exam_date,
                remarks=remarks
            )
            db.session.add(mark_entry)
            flash('Marks entry successfully recorded!', 'success')

        db.session.commit()
        
        stu = db.session.get(Student, student_id)
        stu_name = stu.full_name if stu else 'Student'
        log_activity('Marks', f"Recorded marks ({marks_obtained}/{max_marks} - Grade {grade}) for {stu_name} in {exam_name}.", 'bi-award-fill')
        return redirect(url_for('marks.index'))

    return render_template('marks/add.html', departments=departments, subjects=subjects, students=students)


@marks_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    mark_entry = db.get_or_404(Marks, id)
    subjects = Subject.query.order_by(Subject.name).all()

    if request.method == 'POST':
        subject_id = request.form.get('subject_id', type=int)
        exam_name = request.form.get('exam_name', '').strip()
        semester = request.form.get('semester', type=int)
        max_marks = request.form.get('max_marks', type=float, default=100.0)
        marks_obtained = request.form.get('marks_obtained', type=float)
        remarks = request.form.get('remarks', '').strip()

        if marks_obtained > max_marks:
            flash('Obtained marks cannot exceed Maximum Marks.', 'danger')
            return render_template('marks/edit.html', mark=mark_entry, subjects=subjects)

        percentage, grade, status = Marks.calculate_grade(marks_obtained, max_marks)

        mark_entry.subject_id = subject_id
        mark_entry.exam_name = exam_name
        mark_entry.semester = semester
        mark_entry.max_marks = max_marks
        mark_entry.marks_obtained = marks_obtained
        mark_entry.percentage = percentage
        mark_entry.grade = grade
        mark_entry.status = status
        mark_entry.remarks = remarks

        db.session.commit()
        log_activity('Marks', f"Updated marks for {mark_entry.student.full_name} in {exam_name}.", 'bi-pencil-square')
        flash('Marks record successfully updated.', 'success')
        return redirect(url_for('marks.index'))

    return render_template('marks/edit.html', mark=mark_entry, subjects=subjects)


@marks_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    mark_entry = db.get_or_404(Marks, id)
    db.session.delete(mark_entry)
    db.session.commit()
    flash('Marks entry deleted successfully.', 'info')
    return redirect(url_for('marks.index'))


@marks_bp.route('/marksheet/<int:student_id>')
@login_required
def marksheet(student_id):
    student = db.get_or_404(Student, student_id)
    semester = request.args.get('semester', type=int)
    exam_name = request.args.get('exam_name', '').strip()

    query = Marks.query.filter_by(student_id=student_id)
    if semester:
        query = query.filter_by(semester=semester)
    if exam_name:
        query = query.filter_by(exam_name=exam_name)

    marks = query.order_by(Marks.semester, Marks.exam_name).all()

    total_max = sum(m.max_marks for m in marks)
    total_obtained = sum(m.marks_obtained for m in marks)
    overall_pct = round((total_obtained / total_max * 100), 2) if total_max > 0 else 0.0

    if overall_pct >= 90:
        overall_grade = 'A+'
    elif overall_pct >= 80:
        overall_grade = 'A'
    elif overall_pct >= 70:
        overall_grade = 'B'
    elif overall_pct >= 60:
        overall_grade = 'C'
    elif overall_pct >= 40:
        overall_grade = 'D'
    else:
        overall_grade = 'F'

    all_passed = all(m.status == 'Pass' for m in marks) if marks else False
    final_result = 'PASS' if (all_passed and marks) else ('FAIL' if marks else 'N/A')

    # Available semesters and exams for filter
    all_student_marks = Marks.query.filter_by(student_id=student_id).all()
    available_semesters = sorted(list(set(m.semester for m in all_student_marks)))
    available_exams = sorted(list(set(m.exam_name for m in all_student_marks)))

    return render_template(
        'marks/marksheet.html',
        student=student,
        marks=marks,
        total_max=total_max,
        total_obtained=total_obtained,
        overall_pct=overall_pct,
        overall_grade=overall_grade,
        final_result=final_result,
        selected_sem=semester,
        selected_exam=exam_name,
        available_semesters=available_semesters,
        available_exams=available_exams,
        generated_date=date.today().strftime('%d-%b-%Y')
    )
