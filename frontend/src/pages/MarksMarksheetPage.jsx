import React from 'react';
import { Link } from 'react-router-dom';
import './MarksMarksheetPage.css';

export default function MarksMarksheetPage() {
  const marksheet = [
    { subject: 'Mathematics', marks: 85, total: 100, percentage: 85 },
    { subject: 'Physics', marks: 92, total: 100, percentage: 92 },
    { subject: 'Chemistry', marks: 78, total: 100, percentage: 78 },
    { subject: 'English', marks: 88, total: 100, percentage: 88 },
    { subject: 'History', marks: 90, total: 100, percentage: 90 }
  ];

  const total_marks = marksheet.reduce((sum, m) => sum + m.marks, 0);
  const total_possible = marksheet.reduce((sum, m) => sum + m.total, 0);
  const overall_percentage = (total_marks / total_possible * 100).toFixed(2);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Marksheet - Semester 1</h1>
        <Link to="/marks" className="btn btn-secondary">Back</Link>
      </div>

      <div className="marksheet-card">
        <div className="marksheet-header">
          <h2>John Doe - CSE</h2>
          <p>Student ID: STU202601</p>
        </div>

        <table className="marksheet-table">
          <thead>
            <tr>
              <th>Subject</th>
              <th>Marks Obtained</th>
              <th>Total Marks</th>
              <th>Percentage</th>
              <th>Grade</th>
            </tr>
          </thead>
          <tbody>
            {marksheet.map((item, idx) => {
              let grade = 'F';
              if (item.percentage >= 90) grade = 'A+';
              else if (item.percentage >= 80) grade = 'A';
              else if (item.percentage >= 70) grade = 'B';
              else if (item.percentage >= 60) grade = 'C';
              else if (item.percentage >= 50) grade = 'D';
              return (
                <tr key={idx}>
                  <td>{item.subject}</td>
                  <td>{item.marks}</td>
                  <td>{item.total}</td>
                  <td>{item.percentage}%</td>
                  <td><strong>{grade}</strong></td>
                </tr>
              );
            })}
          </tbody>
        </table>

        <div className="marksheet-summary">
          <div className="summary-row">
            <span>Total Marks:</span>
            <strong>{total_marks}/{total_possible}</strong>
          </div>
          <div className="summary-row">
            <span>Overall Percentage:</span>
            <strong>{overall_percentage}%</strong>
          </div>
          <div className="summary-row">
            <span>Overall Grade:</span>
            <strong>{overall_percentage >= 90 ? 'A+' : overall_percentage >= 80 ? 'A' : overall_percentage >= 70 ? 'B' : 'C'}</strong>
          </div>
        </div>

        <div className="print-button">
          <button onClick={() => window.print()} className="btn btn-primary">Print Marksheet</button>
        </div>
      </div>
    </div>
  );
}
