from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Student, Department, Subject, Attendance, Marks, FeeRecord
from utils import login_required, log_activity, save_avatar

student_bp = Blueprint('students', __name__, url_prefix='/students')

@student_bp.route('/')
@login_required
def index():
    query = Student.query
    
    # Filter parameters
    search = request.args.get('search', '').strip()
    dept_id = request.args.get('department_id', type=int)
    year = request.args.get('year', type=int)
    gender = request.args.get('gender', '').strip()
    status = request.args.get('status', '').strip()

    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Student.student_id.ilike(search_fmt)) |
            (Student.first_name.ilike(search_fmt)) |
            (Student.last_name.ilike(search_fmt)) |
            (Student.email.ilike(search_fmt)) |
            (Student.phone.ilike(search_fmt))
        )
    
    if dept_id:
        query = query.filter(Student.department_id == dept_id)
    if year:
        query = query.filter(Student.year == year)
    if gender:
        query = query.filter(Student.gender == gender)
    if status:
        query = query.filter(Student.status == status)

    # Order by ID desc
    students = query.order_by(Student.created_at.desc()).all()
    departments = Department.query.order_by(Department.name).all()

    return render_template(
        'students/index.html',
        students=students,
        departments=departments,
        search=search,
        selected_dept=dept_id,
        selected_year=year,
        selected_gender=gender,
        selected_status=status
    )


@student_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    departments = Department.query.order_by(Department.name).all()

    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip().upper()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        dob_str = request.form.get('dob')
        gender = request.form.get('gender', 'Male')
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip().lower()
        address = request.form.get('address', '').strip()
        department_id = request.form.get('department_id', type=int)
        course = request.form.get('course', '').strip()
        year = request.form.get('year', type=int, default=1)
        semester = request.form.get('semester', type=int, default=1)
        admission_date_str = request.form.get('admission_date')
        
        parent_name = request.form.get('parent_name', '').strip()
        parent_phone = request.form.get('parent_phone', '').strip()
        parent_relation = request.form.get('parent_relation', 'Father')
        status = request.form.get('status', 'Active')

        # Validation
        if not student_id or not first_name or not last_name or not email or not phone or not department_id:
            flash('Please fill in all required fields.', 'danger')
            return render_template('students/add.html', departments=departments, form_data=request.form)

        # Unique checks
        if Student.query.filter_by(student_id=student_id).first():
            flash(f"Student ID '{student_id}' is already registered.", 'danger')
            return render_template('students/add.html', departments=departments, form_data=request.form)

        if Student.query.filter_by(email=email).first():
            flash(f"Email address '{email}' is already registered.", 'danger')
            return render_template('students/add.html', departments=departments, form_data=request.form)

        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else date(2004, 1, 1)
        except ValueError:
            dob = date(2004, 1, 1)

        try:
            admission_date = datetime.strptime(admission_date_str, '%Y-%m-%d').date() if admission_date_str else date.today()
        except ValueError:
            admission_date = date.today()

        # Handle Photo Upload
        photo_file = request.files.get('photo')
        photo_filename = save_avatar(photo_file, student_id)

        student = Student(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            gender=gender,
            phone=phone,
            email=email,
            address=address,
            department_id=department_id,
            course=course,
            year=year,
            semester=semester,
            admission_date=admission_date,
            parent_name=parent_name,
            parent_phone=parent_phone,
            parent_relation=parent_relation,
            photo_filename=photo_filename,
            status=status
        )

        db.session.add(student)
        db.session.commit()

        log_activity('Student', f"Added new student '{student.full_name}' ({student.student_id}).", 'bi-person-plus-fill')
        flash(f"Student '{student.full_name}' successfully added!", 'success')
        return redirect(url_for('students.view_profile', id=student.id))

    # Pre-generate student ID suggestion
    last_student = Student.query.order_by(Student.id.desc()).first()
    next_num = (last_student.id + 1) if last_student else 1
    suggested_id = f"STU{date.today().year}{next_num:03d}"

    return render_template('students/add.html', departments=departments, suggested_id=suggested_id)


@student_bp.route('/<int:id>')
@login_required
def view_profile(id):
    student = db.get_or_404(Student, id)
    
    # Related records
    attendance_records = Attendance.query.filter_by(student_id=id).order_by(Attendance.date.desc()).all()
    marks_records = Marks.query.filter_by(student_id=id).order_by(Marks.semester, Marks.exam_date.desc()).all()
    fee_records = FeeRecord.query.filter_by(student_id=id).order_by(FeeRecord.due_date.desc()).all()

    # Calculate overall GPA/average
    if marks_records:
        total_pct = sum(m.percentage for m in marks_records)
        avg_percentage = round(total_pct / len(marks_records), 1)
    else:
        avg_percentage = 0.0

    return render_template(
        'students/view.html',
        student=student,
        attendance_records=attendance_records,
        marks_records=marks_records,
        fee_records=fee_records,
        avg_percentage=avg_percentage
    )


@student_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    student = db.get_or_404(Student, id)
    departments = Department.query.order_by(Department.name).all()

    if request.method == 'POST':
        student.first_name = request.form.get('first_name', student.first_name).strip()
        student.last_name = request.form.get('last_name', student.last_name).strip()
        student.gender = request.form.get('gender', student.gender)
        student.phone = request.form.get('phone', student.phone).strip()
        new_email = request.form.get('email', student.email).strip().lower()
        student.address = request.form.get('address', student.address).strip()
        student.department_id = request.form.get('department_id', student.department_id, type=int)
        student.course = request.form.get('course', student.course).strip()
        student.year = request.form.get('year', student.year, type=int)
        student.semester = request.form.get('semester', student.semester, type=int)
        student.parent_name = request.form.get('parent_name', student.parent_name).strip()
        student.parent_phone = request.form.get('parent_phone', student.parent_phone).strip()
        student.parent_relation = request.form.get('parent_relation', student.parent_relation)
        student.status = request.form.get('status', student.status)

        # Date parsing
        dob_str = request.form.get('dob')
        if dob_str:
            try:
                student.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        admission_str = request.form.get('admission_date')
        if admission_str:
            try:
                student.admission_date = datetime.strptime(admission_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        # Check email conflict
        if new_email != student.email:
            existing = Student.query.filter_by(email=new_email).first()
            if existing:
                flash(f"Email '{new_email}' is already in use by another student.", 'danger')
                return render_template('students/edit.html', student=student, departments=departments)
            student.email = new_email

        # Handle Photo Upload update
        photo_file = request.files.get('photo')
        if photo_file and photo_file.filename:
            student.photo_filename = save_avatar(photo_file, student.student_id)

        db.session.commit()
        log_activity('Student', f"Updated details for student '{student.full_name}' ({student.student_id}).", 'bi-pencil-square')
        flash(f"Student '{student.full_name}' updated successfully.", 'success')
        return redirect(url_for('students.view_profile', id=student.id))

    return render_template('students/edit.html', student=student, departments=departments)


@student_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    student = db.get_or_404(Student, id)
    student_name = student.full_name
    student_code = student.student_id

    db.session.delete(student)
    db.session.commit()

    log_activity('Student', f"Deleted student '{student_name}' ({student_code}).", 'bi-trash-fill')
    flash(f"Student '{student_name}' has been permanently deleted.", 'info')
    return redirect(url_for('students.index'))
