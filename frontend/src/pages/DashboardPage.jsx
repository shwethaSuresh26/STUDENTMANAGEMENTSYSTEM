import React, { useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';
import './DashboardPage.css';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await dashboardAPI.getStats();
        setStats(response.data);
      } catch (err) {
        setError('Failed to load dashboard stats');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="dashboard-container">
      <h1>Dashboard</h1>
      {error && <div className="error-message">{error}</div>}
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Students</h3>
          <p className="stat-value">{stats?.total_students || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Departments</h3>
          <p className="stat-value">{stats?.total_departments || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Today's Attendance</h3>
          <p className="stat-value">{stats?.attendance_rate || 0}%</p>
        </div>
        <div className="stat-card">
          <h3>Fees Collected</h3>
          <p className="stat-value">${stats?.total_fees_collected || 0}</p>
        </div>
      </div>
    </div>
  );
}
