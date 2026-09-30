import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './StudentReportPage.css';

export default function StudentReportPage() {
  const [students] = useState([
    { id: 1, name: 'John Doe', department: 'CSE', year: 1, status: 'Active' },
    { id: 2, name: 'Jane Smith', department: 'ECE', year: 1, status: 'Active' },
    { id: 3, name: 'Robert Johnson', department: 'ME', year: 2, status: 'Active' }
  ]);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Student Report</h1>
        <Link to="/reports" className="btn btn-secondary">Back</Link>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Department</th>
              <th>Year</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {students.map(student => (
              <tr key={student.id}>
                <td>{student.name}</td>
                <td>{student.department}</td>
                <td>Year {student.year}</td>
                <td><span className="status status-active">{student.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
