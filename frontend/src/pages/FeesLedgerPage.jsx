import React from 'react';
import { Link } from 'react-router-dom';
import './FeesLedgerPage.css';

export default function FeesLedgerPage() {
  const ledger = [
    { date: '2026-01-15', description: 'Semester Fee Payment', debit: 50000, credit: 0, balance: 50000 },
    { date: '2026-01-20', description: 'Partial Payment', debit: 0, credit: 25000, balance: 25000 },
    { date: '2026-02-01', description: 'Late Fee', debit: 500, credit: 0, balance: 25500 }
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Fee Ledger</h1>
        <Link to="/fees" className="btn btn-secondary">Back</Link>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Description</th>
              <th>Debit</th>
              <th>Credit</th>
              <th>Balance</th>
            </tr>
          </thead>
          <tbody>
            {ledger.map((entry, idx) => (
              <tr key={idx}>
                <td>{entry.date}</td>
                <td>{entry.description}</td>
                <td className="debit">₹{entry.debit > 0 ? entry.debit.toLocaleString() : '-'}</td>
                <td className="credit">₹{entry.credit > 0 ? entry.credit.toLocaleString() : '-'}</td>
                <td className="balance"><strong>₹{entry.balance.toLocaleString()}</strong></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
