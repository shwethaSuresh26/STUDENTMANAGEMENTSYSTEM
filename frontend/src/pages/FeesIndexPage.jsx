import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './FeesIndexPage.css';

export default function FeesIndexPage() {
  const [fees] = useState([
    { id: 1, student_name: 'John Doe', amount: 50000, paid: 35000, pending: 15000, status: 'Partial' },
    { id: 2, student_name: 'Jane Smith', amount: 50000, paid: 50000, pending: 0, status: 'Paid' },
    { id: 3, student_name: 'Robert Johnson', amount: 50000, paid: 0, pending: 50000, status: 'Pending' },
  ]);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Fees Management</h1>
        <Link to="/fees/add" className="btn btn-primary">+ Add Fee Record</Link>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Student</th>
              <th>Total Amount</th>
              <th>Paid</th>
              <th>Pending</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {fees.map(fee => (
              <tr key={fee.id}>
                <td>{fee.student_name}</td>
                <td>₹{fee.amount.toLocaleString()}</td>
                <td>₹{fee.paid.toLocaleString()}</td>
                <td>₹{fee.pending.toLocaleString()}</td>
                <td><span className={`status status-${fee.status.toLowerCase()}`}>{fee.status}</span></td>
                <td><Link to={`/fees/${fee.id}/receipt`} className="btn btn-sm btn-secondary">Receipt</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
