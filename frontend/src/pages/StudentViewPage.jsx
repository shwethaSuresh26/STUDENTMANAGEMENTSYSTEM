import React from 'react';
import { useParams, Link } from 'react-router-dom';
import './StudentViewPage.css';

export default function StudentViewPage() {
  const { id } = useParams();
  const student = {
    id: id,
    student_id: 'STU202601',
    first_name: 'John',
    last_name: 'Doe',
    email: 'john@college.edu',
    phone: '9876543210',
    department: 'Computer Science',
    year: 1,
    status: 'Active',
    enrollment_date: '2024-07-15',
    address: '123 Main Street, City'
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Student Profile</h1>
        <Link to="/students" className="btn btn-secondary">Back to List</Link>
      </div>
      
      <div className="profile-card">
        <div className="profile-header">
          <div className="profile-avatar">JD</div>
          <div className="profile-info">
            <h2>{student.first_name} {student.last_name}</h2>
            <p className="student-id">ID: {student.student_id}</p>
          </div>
        </div>

        <div className="profile-section">
          <h3>Contact Information</h3>
          <div className="info-row">
            <span className="label">Email:</span>
            <span className="value">{student.email}</span>
          </div>
          <div className="info-row">
            <span className="label">Phone:</span>
            <span className="value">{student.phone}</span>
          </div>
          <div className="info-row">
            <span className="label">Address:</span>
            <span className="value">{student.address}</span>
          </div>
        </div>

        <div className="profile-section">
          <h3>Academic Information</h3>
          <div className="info-row">
            <span className="label">Department:</span>
            <span className="value">{student.department}</span>
          </div>
          <div className="info-row">
            <span className="label">Year:</span>
            <span className="value">Year {student.year}</span>
          </div>
          <div className="info-row">
            <span className="label">Enrollment Date:</span>
            <span className="value">{student.enrollment_date}</span>
          </div>
          <div className="info-row">
            <span className="label">Status:</span>
            <span className="value"><span className="status status-active">{student.status}</span></span>
          </div>
        </div>

        <div className="profile-actions">
          <Link to={`/students/${id}/edit`} className="btn btn-primary">Edit Profile</Link>
          <button className="btn btn-danger">Delete Student</button>
        </div>
      </div>
    </div>
  );
}
