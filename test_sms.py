import unittest
from datetime import date
from app import create_app
from models import db, User, Student, Department, Subject, Attendance, Marks, FeeRecord, FeePayment, Timetable

class SMSTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def login(self, username='admin', password='admin123'):
        return self.client.post('/login', data={
            'identifier': username,
            'password': password
        }, follow_redirects=True)

    def test_01_login_logout(self):
        # Test protected redirect
        res = self.client.get('/dashboard')
        self.assertEqual(res.status_code, 302)
        
        # Test valid login
        res = self.login('admin', 'admin123')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Arthur Pendelton', res.data)

        # Test logout
        res = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Sign In to Portal', res.data)

    def test_02_dashboard_kpis(self):
        self.login()
        res = self.client.get('/dashboard')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Total Enrolled Students', res.data)
        self.assertIn(b'Faculty & Subjects', res.data)
        self.assertIn(b'Fee Collections', res.data)

        # Test API
        res = self.client.get('/api/dashboard-stats')
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertIn('departments', json_data)
        self.assertIn('attendance', json_data)
        self.assertIn('fees', json_data)

    def test_03_students_crud(self):
        self.login()
        
        # List
        res = self.client.get('/students/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Alex Morgan', res.data)

        # Search
        res = self.client.get('/students/?search=Sophia')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Sophia Chen', res.data)

        # Add new student
        res = self.client.post('/students/add', data={
            'student_id': 'STU9999',
            'first_name': 'Testy',
            'last_name': 'Tester',
            'dob': '2004-06-15',
            'gender': 'Female',
            'phone': '+1 555-9999',
            'email': 'testy.tester@college.edu',
            'address': '99 Test St, QA City',
            'department_id': 1,
            'course': 'B.Tech CSE',
            'year': 1,
            'semester': 1,
            'admission_date': '2026-08-01',
            'parent_name': 'Papa Tester',
            'parent_phone': '+1 555-8888',
            'parent_relation': 'Father',
            'status': 'Active'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Testy Tester', res.data)

        with self.app.app_context():
            stu = Student.query.filter_by(student_id='STU9999').first()
            self.assertIsNotNone(stu)
            stu_id = stu.id

        # View Profile
        res = self.client.get(f'/students/{stu_id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Testy Tester', res.data)

        # Edit
        res = self.client.post(f'/students/{stu_id}/edit', data={
            'first_name': 'TestyUpdated',
            'last_name': 'Tester',
            'gender': 'Female',
            'phone': '+1 555-9999',
            'email': 'testy.tester@college.edu',
            'address': 'Updated address',
            'department_id': 1,
            'course': 'B.Tech CSE',
            'year': 1,
            'semester': 1,
            'parent_name': 'Papa Tester',
            'parent_phone': '+1 555-8888',
            'parent_relation': 'Father',
            'status': 'Active'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'TestyUpdated', res.data)

        # Delete
        res = self.client.post(f'/students/{stu_id}/delete', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        with self.app.app_context():
            self.assertIsNone(Student.query.filter_by(student_id='STU9999').first())

    def test_04_attendance(self):
        self.login()
        # Daily index
        res = self.client.get('/attendance/')
        self.assertEqual(res.status_code, 200)

        # Low attendance
        res = self.client.get('/attendance/low-attendance')
        self.assertEqual(res.status_code, 200)

        # Monthly report
        res = self.client.get('/attendance/report')
        self.assertEqual(res.status_code, 200)

    def test_05_marks(self):
        self.login()
        # Marks index
        res = self.client.get('/marks/')
        self.assertEqual(res.status_code, 200)

        # Grade calculation test
        pct, grade, status = Marks.calculate_grade(95, 100)
        self.assertEqual(grade, 'A+')
        self.assertEqual(status, 'Pass')

        pct, grade, status = Marks.calculate_grade(35, 100)
        self.assertEqual(grade, 'F')
        self.assertEqual(status, 'Fail')

        # Marksheet view
        with self.app.app_context():
            first_stu = Student.query.first()
            s_id = first_stu.id
        res = self.client.get(f'/marks/marksheet/{s_id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Statement of Marks & Grades', res.data)

    def test_06_fees(self):
        self.login()
        # Fees index
        res = self.client.get('/fees/')
        self.assertEqual(res.status_code, 200)

        # Receipt view
        with self.app.app_context():
            pmt = FeePayment.query.first()
            pmt_id = pmt.id
        res = self.client.get(f'/fees/receipt/{pmt_id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Official Fee Payment Receipt', res.data)

    def test_07_timetable(self):
        self.login()
        res = self.client.get('/timetable/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Weekly Schedule', res.data)

    def test_08_reports(self):
        self.login()
        endpoints = [
            '/reports/',
            '/reports/students',
            '/reports/attendance',
            '/reports/marks',
            '/reports/fees',
            '/reports/timetable'
        ]
        for ep in endpoints:
            res = self.client.get(ep)
            self.assertEqual(res.status_code, 200, f"Failed at {ep}")

if __name__ == '__main__':
    unittest.main()
