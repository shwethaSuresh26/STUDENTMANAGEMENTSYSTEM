import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './MarksIndexPage.css';

export default function MarksIndexPage() {
  const [marks] = useState([
    { id: 1, student_name: 'John Doe', subject: 'Mathematics', marks: 85, total: 100 },
    { id: 2, student_name: 'Jane Smith', subject: 'Physics', marks: 92, total: 100 },
    { id: 3, student_name: 'Robert Johnson', subject: 'Chemistry', marks: 78, total: 100 },
  ]);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Marks Management</h1>
        <Link to="/marks/add" className="btn btn-primary">+ Add Marks</Link>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Student</th>
              <th>Subject</th>
              <th>Marks</th>
              <th>Percentage</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {marks.map(mark => (
              <tr key={mark.id}>
                <td>{mark.student_name}</td>
                <td>{mark.subject}</td>
                <td>{mark.marks}/{mark.total}</td>
                <td>{((mark.marks/mark.total)*100).toFixed(1)}%</td>
                <td><Link to={`/marks/${mark.id}/edit`} className="btn btn-sm btn-secondary">Edit</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
