import React from 'react';
import { Link } from 'react-router-dom';
import './ReportsIndexPage.css';

export default function ReportsIndexPage() {
  const reports = [
    { id: 1, name: 'Student Report', icon: '👥', link: '/reports/student' },
    { id: 2, name: 'Attendance Report', icon: '📋', link: '/reports/attendance' },
    { id: 3, name: 'Marks Report', icon: '📊', link: '/reports/marks' },
    { id: 4, name: 'Fee Report', icon: '💰', link: '/reports/fee' },
    { id: 5, name: 'Timetable Report', icon: '📅', link: '/reports/timetable' },
  ];

  return (
    <div className="page-container">
      <h1>Reports</h1>
      <div className="reports-grid">
        {reports.map(report => (
          <Link key={report.id} to={report.link} className="report-card">
            <div className="report-icon">{report.icon}</div>
            <div className="report-name">{report.name}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
