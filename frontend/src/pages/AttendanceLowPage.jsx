import React from 'react';
import { Link } from 'react-router-dom';
import './AttendanceLowPage.css';

export default function AttendanceLowPage() {
  const lowAttendance = [
    { id: 1, student_name: 'Robert Johnson', attendance_percentage: 45 },
    { id: 2, student_name: 'Michael Brown', attendance_percentage: 52 },
    { id: 3, student_name: 'Sarah Davis', attendance_percentage: 58 }
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Low Attendance Report</h1>
        <Link to="/attendance" className="btn btn-secondary">Back</Link>
      </div>

      <div className="card">
        <p className="info-text">Students with attendance below 75%:</p>
        <table className="table">
          <thead>
            <tr>
              <th>Student Name</th>
              <th>Attendance %</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {lowAttendance.map(record => (
              <tr key={record.id}>
                <td>{record.student_name}</td>
                <td>{record.attendance_percentage}%</td>
                <td><span className="status status-warning">At Risk</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
