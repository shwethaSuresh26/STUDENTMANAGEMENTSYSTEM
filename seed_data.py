import os
from datetime import datetime, date, timedelta, timezone
from app import create_app
from models import (
    db, User, Department, Subject, Student, 
    Attendance, Marks, FeeRecord, FeePayment, 
    Timetable, ActivityLog
)

app = create_app()

def seed():
    with app.app_context():
        print("Recreating database tables...")
        db.drop_all()
        db.create_all()

        now = datetime.now(timezone.utc)

        # ----------------------------------------------------
        # 1. ADMIN USER
        # ----------------------------------------------------
        admin = User(
            username='admin',
            email='admin@college.edu',
            full_name='Dr. Arthur Pendelton',
            role='Administrator',
            last_login=now
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()

        print("Admin user seeded: admin / admin123")

        # ----------------------------------------------------
        # 2. DEPARTMENTS
        # ----------------------------------------------------
        departments = [
            Department(name='Computer Science & Engineering', code='CSE', description='Department of Computer Science and Software Systems'),
            Department(name='Information Technology', code='IT', description='Department of Information Technology & Cloud Systems'),
            Department(name='Electronics & Communication', code='ECE', description='Department of Microelectronics and Telecom Systems'),
            Department(name='Mechanical Engineering', code='ME', description='Department of Mechanical Design and Thermal Sciences'),
            Department(name='Business Administration', code='BBA', description='School of Business and Management Studies')
        ]
        db.session.add_all(departments)
        db.session.flush()
        print(f"Seeded {len(departments)} departments.")

        # ----------------------------------------------------
        # 3. SUBJECTS
        # ----------------------------------------------------
        cse, it, ece, me, bba = departments[0], departments[1], departments[2], departments[3], departments[4]

        subjects = [
            Subject(name='Data Structures & Algorithms', code='CS101', department_id=cse.id, teacher_name='Dr. Alan Turing', semester=1, credits=4),
            Subject(name='Database Management Systems', code='CS102', department_id=cse.id, teacher_name='Prof. Grace Hopper', semester=1, credits=4),
            Subject(name='Operating Systems & Architecture', code='CS201', department_id=cse.id, teacher_name='Prof. Linus Torvalds', semester=2, credits=3),
            Subject(name='Artificial Intelligence & ML', code='CS301', department_id=cse.id, teacher_name='Prof. Geoffrey Hinton', semester=3, credits=4),
            
            Subject(name='Web Technologies & Cloud Services', code='IT101', department_id=it.id, teacher_name='Prof. Tim Berners-Lee', semester=1, credits=3),
            Subject(name='Network Security & Cryptography', code='IT202', department_id=it.id, teacher_name='Dr. Ada Lovelace', semester=2, credits=4),
            
            Subject(name='Digital Signal Processing', code='EC201', department_id=ece.id, teacher_name='Prof. Claude Shannon', semester=2, credits=4),
            Subject(name='VLSI Circuit Design', code='EC301', department_id=ece.id, teacher_name='Dr. Jack Kilby', semester=3, credits=3),
            
            Subject(name='Thermodynamics & Heat Transfer', code='ME101', department_id=me.id, teacher_name='Prof. James Watt', semester=1, credits=4),
            Subject(name='Fluid Mechanics & Hydraulics', code='ME201', department_id=me.id, teacher_name='Dr. Daniel Bernoulli', semester=2, credits=4),
            
            Subject(name='Financial Accounting & Management', code='BA101', department_id=bba.id, teacher_name='Prof. Warren Buffett', semester=1, credits=3),
            Subject(name='Marketing & Strategic Management', code='BA201', department_id=bba.id, teacher_name='Dr. Philip Kotler', semester=2, credits=3)
        ]
        db.session.add_all(subjects)
        db.session.flush()
        print(f"Seeded {len(subjects)} academic subjects.")

        # ----------------------------------------------------
        # 4. STUDENTS
        # ----------------------------------------------------
        students_data = [
            # CSE Students
            ('STU2026001', 'Alex', 'Morgan', date(2004, 5, 12), 'Male', '+1 555-0101', 'alex.morgan@college.edu', '124 Academic Way, Tech City', cse.id, 'B.Tech CSE', 1, 1, date(2026, 7, 10), 'Robert Morgan', '+1 555-1101', 'Father'),
            ('STU2026002', 'Sophia', 'Chen', date(2004, 8, 22), 'Female', '+1 555-0102', 'sophia.chen@college.edu', '88 Maple Boulevard, Silicon Valley', cse.id, 'B.Tech CSE', 1, 1, date(2026, 7, 10), 'David Chen', '+1 555-1102', 'Father'),
            ('STU2026003', 'Liam', 'Johnson', date(2003, 3, 14), 'Male', '+1 555-0103', 'liam.johnson@college.edu', '45 Pine Ridge, Cambridge', cse.id, 'B.Tech CSE', 2, 2, date(2025, 7, 15), 'Sarah Johnson', '+1 555-1103', 'Mother'),
            ('STU2026004', 'Emily', 'Davis', date(2004, 11, 30), 'Female', '+1 555-0104', 'emily.davis@college.edu', '210 Oak Street, Boston', cse.id, 'B.Tech CSE', 1, 1, date(2026, 7, 12), 'Mark Davis', '+1 555-1104', 'Father'),
            
            # IT Students
            ('STU2026005', 'Daniel', 'Martinez', date(2004, 2, 18), 'Male', '+1 555-0105', 'daniel.martinez@college.edu', '302 Sunset Blvd, Austin', it.id, 'B.Tech IT', 1, 1, date(2026, 7, 15), 'Elena Martinez', '+1 555-1105', 'Mother'),
            ('STU2026006', 'Olivia', 'Taylor', date(2003, 9, 25), 'Female', '+1 555-0106', 'olivia.taylor@college.edu', '67 Cedar Lane, Seattle', it.id, 'B.Tech IT', 2, 2, date(2025, 7, 18), 'James Taylor', '+1 555-1106', 'Father'),
            
            # ECE Students
            ('STU2026007', 'Ethan', 'Brown', date(2004, 7, 19), 'Male', '+1 555-0107', 'ethan.brown@college.edu', '512 Elm Court, Chicago', ece.id, 'B.Tech ECE', 1, 1, date(2026, 7, 20), 'Michael Brown', '+1 555-1107', 'Father'),
            ('STU2026008', 'Ava', 'Wilson', date(2003, 12, 5), 'Female', '+1 555-0108', 'ava.wilson@college.edu', '94 Willow Dr, San Jose', ece.id, 'B.Tech ECE', 2, 2, date(2025, 7, 20), 'Laura Wilson', '+1 555-1108', 'Mother'),
            
            # ME Students
            ('STU2026009', 'Noah', 'Anderson', date(2004, 4, 8), 'Male', '+1 555-0109', 'noah.anderson@college.edu', '118 Birch Way, Detroit', me.id, 'B.Tech ME', 1, 1, date(2026, 7, 22), 'William Anderson', '+1 555-1109', 'Father'),
            ('STU2026010', 'Isabella', 'Thomas', date(2003, 6, 17), 'Female', '+1 555-0110', 'isabella.thomas@college.edu', '77 River Road, Pittsburgh', me.id, 'B.Tech ME', 2, 2, date(2025, 7, 22), 'Susan Thomas', '+1 555-1110', 'Mother'),
            
            # BBA Students
            ('STU2026011', 'Lucas', 'White', date(2004, 10, 11), 'Male', '+1 555-0111', 'lucas.white@college.edu', '800 Wall St, New York', bba.id, 'BBA Business', 1, 1, date(2026, 7, 25), 'Richard White', '+1 555-1111', 'Father'),
            ('STU2026012', 'Mia', 'Harris', date(2004, 1, 29), 'Female', '+1 555-0112', 'mia.harris@college.edu', '430 Market St, Philadelphia', bba.id, 'BBA Business', 1, 1, date(2026, 7, 25), 'Patricia Harris', '+1 555-1112', 'Mother')
        ]

        students = []
        for s_data in students_data:
            stu = Student(
                student_id=s_data[0],
                first_name=s_data[1],
                last_name=s_data[2],
                dob=s_data[3],
                gender=s_data[4],
                phone=s_data[5],
                email=s_data[6],
                address=s_data[7],
                department_id=s_data[8],
                course=s_data[9],
                year=s_data[10],
                semester=s_data[11],
                admission_date=s_data[12],
                parent_name=s_data[13],
                parent_phone=s_data[14],
                parent_relation=s_data[15],
                photo_filename='default-avatar.svg',
                status='Active'
            )
            students.append(stu)
            db.session.add(stu)

        db.session.flush()
        print(f"Seeded {len(students)} students.")

        # ----------------------------------------------------
        # 5. ATTENDANCE RECORDS (Past 7 dates)
        # ----------------------------------------------------
        today = date.today()
        cse_sub1 = subjects[0]  # CS101
        cse_sub2 = subjects[1]  # CS102

        alex, sophia, liam, emily = students[0], students[1], students[2], students[3]
        daniel, olivia = students[4], students[5]
        ethan, ava = students[6], students[7]
        noah, isabella = students[8], students[9]
        lucas, mia = students[10], students[11]

        dates_list = [today - timedelta(days=i) for i in range(7)]

        for d in dates_list:
            # CS101
            db.session.add(Attendance(student_id=alex.id, subject_id=cse_sub1.id, date=d, status='Present', remarks='On time'))
            db.session.add(Attendance(student_id=sophia.id, subject_id=cse_sub1.id, date=d, status='Present', remarks='On time'))
            if d.day % 2 == 0:
                db.session.add(Attendance(student_id=emily.id, subject_id=cse_sub1.id, date=d, status='Present', remarks='Late entry'))
            else:
                db.session.add(Attendance(student_id=emily.id, subject_id=cse_sub1.id, date=d, status='Absent', remarks='Sick leave'))

            # CS102
            db.session.add(Attendance(student_id=alex.id, subject_id=cse_sub2.id, date=d, status='Present'))
            db.session.add(Attendance(student_id=sophia.id, subject_id=cse_sub2.id, date=d, status='Present'))
            db.session.add(Attendance(student_id=emily.id, subject_id=cse_sub2.id, date=d, status='Absent'))

            # IT101 for Daniel
            db.session.add(Attendance(student_id=daniel.id, subject_id=subjects[4].id, date=d, status='Present'))
            
            # ECE for Ethan
            db.session.add(Attendance(student_id=ethan.id, subject_id=subjects[6].id, date=d, status='Absent' if d.day % 3 != 0 else 'Present'))

            # ME for Noah
            db.session.add(Attendance(student_id=noah.id, subject_id=subjects[8].id, date=d, status='Present'))

            # BBA for Lucas & Mia
            db.session.add(Attendance(student_id=lucas.id, subject_id=subjects[10].id, date=d, status='Present'))
            db.session.add(Attendance(student_id=mia.id, subject_id=subjects[10].id, date=d, status='Present'))

        db.session.flush()
        print("Seeded realistic attendance logs.")

        # ----------------------------------------------------
        # 6. MARKS RECORDS
        # ----------------------------------------------------
        marks_entries = [
            # Alex Morgan (CSE)
            (alex.id, subjects[0].id, 'Midterm Exam', 1, 100.0, 92.0, 'A+', 'Pass'),
            (alex.id, subjects[1].id, 'Midterm Exam', 1, 100.0, 88.0, 'A', 'Pass'),
            (alex.id, subjects[0].id, 'Unit Test 1', 1, 50.0, 46.0, 'A+', 'Pass'),
            
            # Sophia Chen (CSE)
            (sophia.id, subjects[0].id, 'Midterm Exam', 1, 100.0, 96.0, 'A+', 'Pass'),
            (sophia.id, subjects[1].id, 'Midterm Exam', 1, 100.0, 94.0, 'A+', 'Pass'),
            (sophia.id, subjects[0].id, 'Unit Test 1', 1, 50.0, 48.0, 'A+', 'Pass'),

            # Emily Davis (CSE)
            (emily.id, subjects[0].id, 'Midterm Exam', 1, 100.0, 54.0, 'D', 'Pass'),
            (emily.id, subjects[1].id, 'Midterm Exam', 1, 100.0, 38.0, 'F', 'Fail'),

            # Daniel Martinez (IT)
            (daniel.id, subjects[4].id, 'Midterm Exam', 1, 100.0, 84.0, 'A', 'Pass'),

            # Ethan Brown (ECE)
            (ethan.id, subjects[6].id, 'Midterm Exam', 1, 100.0, 68.0, 'B', 'Pass'),

            # Noah Anderson (ME)
            (noah.id, subjects[8].id, 'Midterm Exam', 1, 100.0, 78.0, 'B', 'Pass'),

            # Lucas White (BBA)
            (lucas.id, subjects[10].id, 'Midterm Exam', 1, 100.0, 89.0, 'A', 'Pass'),

            # Mia Harris (BBA)
            (mia.id, subjects[10].id, 'Midterm Exam', 1, 100.0, 91.0, 'A+', 'Pass')
        ]

        for m_data in marks_entries:
            pct = round((m_data[5] / m_data[4]) * 100, 1)
            mark = Marks(
                student_id=m_data[0],
                subject_id=m_data[1],
                exam_name=m_data[2],
                semester=m_data[3],
                max_marks=m_data[4],
                marks_obtained=m_data[5],
                percentage=pct,
                grade=m_data[6],
                status=m_data[7],
                exam_date=date.today() - timedelta(days=15),
                remarks='Evaluated'
            )
            db.session.add(mark)

        db.session.flush()
        print("Seeded examination marks and grade entries.")

        # ----------------------------------------------------
        # 7. FEE RECORDS & PAYMENTS
        # ----------------------------------------------------
        fee1 = FeeRecord(
            student_id=alex.id,
            fee_category='Tuition Fee',
            title='Semester 1 Tuition Fee 2026',
            total_amount=3500.0,
            paid_amount=3500.0,
            balance_amount=0.0,
            status='Paid',
            due_date=date.today() + timedelta(days=30)
        )
        db.session.add(fee1)
        db.session.flush()
        db.session.add(FeePayment(
            fee_record_id=fee1.id,
            amount=3500.0,
            payment_method='Online / Card',
            transaction_id='TXN2026071001',
            payment_date=now - timedelta(days=20),
            notes='Paid online via student portal',
            recorded_by='Dr. Arthur Pendelton'
        ))

        fee2 = FeeRecord(
            student_id=sophia.id,
            fee_category='Tuition Fee',
            title='Semester 1 Tuition Fee 2026',
            total_amount=3500.0,
            paid_amount=2000.0,
            balance_amount=1500.0,
            status='Partially Paid',
            due_date=date.today() + timedelta(days=20)
        )
        db.session.add(fee2)
        db.session.flush()
        db.session.add(FeePayment(
            fee_record_id=fee2.id,
            amount=2000.0,
            payment_method='Bank Transfer',
            transaction_id='TXN2026071202',
            payment_date=now - timedelta(days=15),
            notes='First installment paid',
            recorded_by='Dr. Arthur Pendelton'
        ))

        fee3 = FeeRecord(
            student_id=emily.id,
            fee_category='Tuition Fee',
            title='Semester 1 Tuition Fee 2026',
            total_amount=3500.0,
            paid_amount=0.0,
            balance_amount=3500.0,
            status='Pending',
            due_date=date.today() + timedelta(days=10)
        )
        db.session.add(fee3)

        fee4 = FeeRecord(
            student_id=daniel.id,
            fee_category='Hostel Fee',
            title='Annual Campus Hostel Accommodation',
            total_amount=1800.0,
            paid_amount=1800.0,
            balance_amount=0.0,
            status='Paid',
            due_date=date.today() + timedelta(days=45)
        )
        db.session.add(fee4)
        db.session.flush()
        db.session.add(FeePayment(
            fee_record_id=fee4.id,
            amount=1800.0,
            payment_method='UPI',
            transaction_id='UPI992817263',
            payment_date=now - timedelta(days=10),
            notes='Hostel block B accommodation fee',
            recorded_by='Dr. Arthur Pendelton'
        ))

        fee5 = FeeRecord(
            student_id=lucas.id,
            fee_category='Exam Fee',
            title='Semester 1 Midterm Exam Fee',
            total_amount=250.0,
            paid_amount=250.0,
            balance_amount=0.0,
            status='Paid',
            due_date=date.today() + timedelta(days=5)
        )
        db.session.add(fee5)
        db.session.flush()
        db.session.add(FeePayment(
            fee_record_id=fee5.id,
            amount=250.0,
            payment_method='Cash',
            transaction_id='CSH20260801',
            payment_date=now - timedelta(days=5),
            notes='Paid at counter',
            recorded_by='Dr. Arthur Pendelton'
        ))

        db.session.flush()
        print("Seeded fee invoices, payment transactions, and receipts.")

        # ----------------------------------------------------
        # 8. TIMETABLE SLOTS (CSE Year 1 Sem 1 Schedule)
        # ----------------------------------------------------
        timetable_data = [
            # Monday
            (cse.id, 'B.Tech CSE', 1, 1, 'Monday', 1, subjects[0].id, 'Dr. Alan Turing', 'Hall 101', '09:00 AM', '10:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Monday', 2, subjects[1].id, 'Prof. Grace Hopper', 'Lab 2', '10:00 AM', '11:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Monday', 3, subjects[0].id, 'Dr. Alan Turing', 'Hall 101', '11:15 AM', '12:15 PM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Monday', 4, subjects[1].id, 'Prof. Grace Hopper', 'Lab 2', '12:15 PM', '01:15 PM'),

            # Tuesday
            (cse.id, 'B.Tech CSE', 1, 1, 'Tuesday', 1, subjects[1].id, 'Prof. Grace Hopper', 'Lab 2', '09:00 AM', '10:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Tuesday', 2, subjects[0].id, 'Dr. Alan Turing', 'Hall 101', '10:00 AM', '11:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Tuesday', 5, subjects[3].id, 'Prof. Geoffrey Hinton', 'AI Center', '02:00 PM', '03:00 PM'),

            # Wednesday
            (cse.id, 'B.Tech CSE', 1, 1, 'Wednesday', 1, subjects[0].id, 'Dr. Alan Turing', 'Hall 101', '09:00 AM', '10:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Wednesday', 2, subjects[1].id, 'Prof. Grace Hopper', 'Lab 2', '10:00 AM', '11:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Wednesday', 3, subjects[3].id, 'Prof. Geoffrey Hinton', 'Hall 102', '11:15 AM', '12:15 PM'),

            # Thursday
            (cse.id, 'B.Tech CSE', 1, 1, 'Thursday', 1, subjects[1].id, 'Prof. Grace Hopper', 'Lab 2', '09:00 AM', '10:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Thursday', 2, subjects[0].id, 'Dr. Alan Turing', 'Hall 101', '10:00 AM', '11:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Thursday', 6, subjects[3].id, 'Prof. Geoffrey Hinton', 'AI Center', '03:00 PM', '04:00 PM'),

            # Friday
            (cse.id, 'B.Tech CSE', 1, 1, 'Friday', 1, subjects[0].id, 'Dr. Alan Turing', 'Hall 101', '09:00 AM', '10:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Friday', 2, subjects[1].id, 'Prof. Grace Hopper', 'Lab 2', '10:00 AM', '11:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Friday', 4, subjects[3].id, 'Prof. Geoffrey Hinton', 'Hall 102', '12:15 PM', '01:15 PM'),

            # Saturday
            (cse.id, 'B.Tech CSE', 1, 1, 'Saturday', 1, subjects[0].id, 'Dr. Alan Turing', 'Hall 101', '09:00 AM', '10:00 AM'),
            (cse.id, 'B.Tech CSE', 1, 1, 'Saturday', 2, subjects[3].id, 'Prof. Geoffrey Hinton', 'AI Center', '10:00 AM', '11:00 AM')
        ]

        for tt in timetable_data:
            slot = Timetable(
                department_id=tt[0],
                course=tt[1],
                year=tt[2],
                semester=tt[3],
                day_of_week=tt[4],
                period_number=tt[5],
                subject_id=tt[6],
                teacher_name=tt[7],
                room_number=tt[8],
                start_time=tt[9],
                end_time=tt[10]
            )
            db.session.add(slot)

        # ----------------------------------------------------
        # 9. RECENT ACTIVITY LOGS
        # ----------------------------------------------------
        activities = [
            ActivityLog(user_id=admin.id, action_type='Student', description="Enrolled new student 'Alex Morgan' in CSE.", icon_class='bi-person-plus-fill', timestamp=now - timedelta(hours=5)),
            ActivityLog(user_id=admin.id, action_type='Fees', description="Received tuition payment of $3,500.00 from Alex Morgan.", icon_class='bi-cash-coin', timestamp=now - timedelta(hours=4)),
            ActivityLog(user_id=admin.id, action_type='Attendance', description="Marked attendance for CS101 Data Structures class.", icon_class='bi-calendar-check-fill', timestamp=now - timedelta(hours=3)),
            ActivityLog(user_id=admin.id, action_type='Marks', description="Recorded Midterm examination scores for CS101.", icon_class='bi-award-fill', timestamp=now - timedelta(hours=2)),
            ActivityLog(user_id=admin.id, action_type='Timetable', description="Updated weekly schedule matrix for Department of CSE.", icon_class='bi-clock-history', timestamp=now - timedelta(hours=1))
        ]
        db.session.add_all(activities)

        db.session.commit()
        print("--- Database seeding completed successfully! ---")

if __name__ == '__main__':
    seed()
