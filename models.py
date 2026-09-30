from datetime import datetime, date, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utcnow():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(30), default='Admin')  # Admin, Principal, Staff
    created_at = db.Column(db.DateTime, default=utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    students = db.relationship('Student', backref='department', lazy=True)
    subjects = db.relationship('Subject', backref='department', lazy=True, cascade='all, delete-orphan')
    timetable_entries = db.relationship('Timetable', backref='department', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Department {self.code} - {self.name}>'


class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    teacher_name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, default=1)
    credits = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime, default=utcnow)

    attendance_records = db.relationship('Attendance', backref='subject', lazy=True, cascade='all, delete-orphan')
    marks_records = db.relationship('Marks', backref='subject', lazy=True, cascade='all, delete-orphan')
    timetable_slots = db.relationship('Timetable', backref='subject', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Subject {self.code}: {self.name}>'


class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(30), unique=True, nullable=False, index=True)  # e.g., STU2026001
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)  # Male, Female, Other
    phone = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    address = db.Column(db.Text, nullable=False)
    
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    course = db.Column(db.String(100), nullable=False)  # e.g., B.Tech, B.Sc, BCA, MBA
    year = db.Column(db.Integer, nullable=False, default=1)  # 1, 2, 3, 4
    semester = db.Column(db.Integer, nullable=False, default=1)  # 1 to 8
    admission_date = db.Column(db.Date, nullable=False, default=date.today)
    
    # Parent/Guardian Details
    parent_name = db.Column(db.String(100), nullable=False)
    parent_phone = db.Column(db.String(25), nullable=False)
    parent_relation = db.Column(db.String(40), default='Father')  # Father, Mother, Guardian
    
    photo_filename = db.Column(db.String(255), default='default-avatar.svg')
    status = db.Column(db.String(20), default='Active')  # Active, Inactive, Graduated, Suspended
    created_at = db.Column(db.DateTime, default=utcnow)

    # Relationships
    attendance_records = db.relationship('Attendance', backref='student', lazy=True, cascade='all, delete-orphan')
    marks_records = db.relationship('Marks', backref='student', lazy=True, cascade='all, delete-orphan')
    fee_records = db.relationship('FeeRecord', backref='student', lazy=True, cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def attendance_stats(self):
        total = len(self.attendance_records)
        if total == 0:
            return {'total': 0, 'present': 0, 'absent': 0, 'late': 0, 'percentage': 0.0}
        present = sum(1 for a in self.attendance_records if a.status in ['Present', 'Late'])
        absent = sum(1 for a in self.attendance_records if a.status == 'Absent')
        late = sum(1 for a in self.attendance_records if a.status == 'Late')
        pct = round((present / total) * 100, 1)
        return {'total': total, 'present': present, 'absent': absent, 'late': late, 'percentage': pct}

    @property
    def fee_stats(self):
        total = sum(f.total_amount for f in self.fee_records)
        paid = sum(f.paid_amount for f in self.fee_records)
        pending = sum(f.balance_amount for f in self.fee_records)
        return {'total': total, 'paid': paid, 'pending': pending}

    def __repr__(self):
        return f'<Student {self.student_id} - {self.full_name}>'


class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    status = db.Column(db.String(20), nullable=False)  # Present, Absent, Late, Excused
    remarks = db.Column(db.String(200), nullable=True)
    recorded_by = db.Column(db.String(100), default='Admin')
    created_at = db.Column(db.DateTime, default=utcnow)

    # Unique constraint per student, subject, and date
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_id', 'date', name='uq_student_subject_date'),
    )

    def __repr__(self):
        return f'<Attendance Stu:{self.student_id} Sub:{self.subject_id} Date:{self.date} Stat:{self.status}>'


class Marks(db.Model):
    __tablename__ = 'marks'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False, index=True)
    exam_name = db.Column(db.String(100), nullable=False)  # Midterm, Final Exam, Unit Test 1, Practical
    semester = db.Column(db.Integer, nullable=False, default=1)
    max_marks = db.Column(db.Float, nullable=False, default=100.0)
    marks_obtained = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=False)  # A+, A, B, C, D, F
    status = db.Column(db.String(20), nullable=False)  # Pass, Fail
    exam_date = db.Column(db.Date, default=date.today)
    remarks = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_id', 'exam_name', 'semester', name='uq_student_subject_exam'),
    )

    @staticmethod
    def calculate_grade(marks_obtained, max_marks):
        if max_marks <= 0:
            return 0.0, 'F', 'Fail'
        pct = round((marks_obtained / max_marks) * 100, 2)
        if pct >= 90:
            grade = 'A+'
            status = 'Pass'
        elif pct >= 80:
            grade = 'A'
            status = 'Pass'
        elif pct >= 70:
            grade = 'B'
            status = 'Pass'
        elif pct >= 60:
            grade = 'C'
            status = 'Pass'
        elif pct >= 40:
            grade = 'D'
            status = 'Pass'
        else:
            grade = 'F'
            status = 'Fail'
        return pct, grade, status

    def __repr__(self):
        return f'<Marks Stu:{self.student_id} Sub:{self.subject_id} Exam:{self.exam_name} Pct:{self.percentage}%>'


class FeeRecord(db.Model):
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    fee_category = db.Column(db.String(50), nullable=False)  # Tuition Fee, Exam Fee, Library Fee, Hostel Fee, Transport Fee, Other Fees
    title = db.Column(db.String(150), nullable=False)  # e.g., "Semester 1 Tuition Fee 2026"
    total_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, default=0.0)
    balance_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='Pending')  # Paid, Partially Paid, Pending, Overdue
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)

    payments = db.relationship('FeePayment', backref='fee_record', lazy=True, cascade='all, delete-orphan')

    def update_balance_and_status(self):
        self.paid_amount = sum(p.amount for p in self.payments)
        self.balance_amount = max(0.0, self.total_amount - self.paid_amount)
        if self.paid_amount >= self.total_amount:
            self.status = 'Paid'
        elif self.paid_amount > 0:
            self.status = 'Partially Paid'
        else:
            self.status = 'Pending'

    def __repr__(self):
        return f'<FeeRecord Stu:{self.student_id} Cat:{self.fee_category} Bal:{self.balance_amount}>'


class FeePayment(db.Model):
    __tablename__ = 'fee_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    fee_record_id = db.Column(db.Integer, db.ForeignKey('fees.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(40), default='Cash')  # Cash, Online, Bank Transfer, Cheque, UPI
    transaction_id = db.Column(db.String(100), nullable=True)
    payment_date = db.Column(db.DateTime, default=utcnow)
    notes = db.Column(db.String(250), nullable=True)
    recorded_by = db.Column(db.String(100), default='Admin')

    def __repr__(self):
        return f'<FeePayment Ref:{self.id} Rec:{self.fee_record_id} Amt:{self.amount}>'


class Timetable(db.Model):
    __tablename__ = 'timetable'
    
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False, default=1)
    semester = db.Column(db.Integer, nullable=False, default=1)
    
    day_of_week = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, Wednesday, Thursday, Friday, Saturday
    period_number = db.Column(db.Integer, nullable=False)  # 1 to 8
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_name = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(50), nullable=False, default='Hall 101')
    start_time = db.Column(db.String(20), nullable=False)  # e.g., "09:00 AM"
    end_time = db.Column(db.String(20), nullable=False)    # e.g., "10:00 AM"
    created_at = db.Column(db.DateTime, default=utcnow)

    def __repr__(self):
        return f'<Timetable {self.day_of_week} Period {self.period_number} - {self.teacher_name}>'


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action_type = db.Column(db.String(50), nullable=False)  # Student, Attendance, Marks, Fees, Timetable, Auth
    description = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=utcnow, index=True)
    icon_class = db.Column(db.String(50), default='bi-activity')

    def __repr__(self):
        return f'<ActivityLog {self.action_type}: {self.description}>'