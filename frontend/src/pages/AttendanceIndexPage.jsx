import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './AttendanceIndexPage.css';

export default function AttendanceIndexPage() {
  const [attendance] = useState([
    { id: 1, student_name: 'John Doe', date: '2026-01-18', status: 'Present', subject: 'Mathematics' },
    { id: 2, student_name: 'Jane Smith', date: '2026-01-18', status: 'Present', subject: 'Physics' },
    { id: 3, student_name: 'Robert Johnson', date: '2026-01-18', status: 'Absent', subject: 'Chemistry' },
  ]);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Attendance Management</h1>
        <Link to="/attendance/mark" className="btn btn-primary">+ Mark Attendance</Link>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Student</th>
              <th>Date</th>
              <th>Subject</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {attendance.map(record => (
              <tr key={record.id}>
                <td>{record.student_name}</td>
                <td>{record.date}</td>
                <td>{record.subject}</td>
                <td><span className={`status status-${record.status.toLowerCase()}`}>{record.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
