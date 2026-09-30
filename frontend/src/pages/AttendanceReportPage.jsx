import React from 'react';
import { Link } from 'react-router-dom';
import './AttendanceReportPage.css';

export default function AttendanceReportPage() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Attendance Report</h1>
        <Link to="/attendance" className="btn btn-secondary">Back</Link>
      </div>

      <div className="report-filters">
        <input type="month" placeholder="Select Month" className="filter-input" />
        <select className="filter-select">
          <option value="">Select Department</option>
          <option value="1">CSE</option>
          <option value="2">ECE</option>
          <option value="3">ME</option>
        </select>
        <button className="btn btn-primary">Generate Report</button>
      </div>

      <div className="card">
        <p className="info-text">Monthly attendance summary will appear here.</p>
      </div>
    </div>
  );
}
