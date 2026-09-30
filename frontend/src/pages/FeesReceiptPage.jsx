import React from 'react';
import { Link, useParams } from 'react-router-dom';
import './FeesReceiptPage.css';

export default function FeesReceiptPage() {
  const { id } = useParams();
  const receipt = {
    receipt_id: 'RCP/2026/001',
    student_name: 'John Doe',
    student_id: 'STU202601',
    date: new Date().toISOString().split('T')[0],
    amount: 25000,
    payment_mode: 'Bank Transfer',
    reference: 'TXN123456789',
    description: 'Semester 1 Fee Payment'
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Fee Receipt</h1>
        <Link to="/fees" className="btn btn-secondary">Back</Link>
      </div>

      <div className="receipt-card">
        <div className="receipt-header">
          <h2>EduManage - Fee Receipt</h2>
          <p>Receipt ID: {receipt.receipt_id}</p>
        </div>

        <div className="receipt-body">
          <div className="receipt-section">
            <h3>Student Details</h3>
            <div className="receipt-row">
              <span>Name:</span>
              <span>{receipt.student_name}</span>
            </div>
            <div className="receipt-row">
              <span>ID:</span>
              <span>{receipt.student_id}</span>
            </div>
          </div>

          <div className="receipt-section">
            <h3>Payment Details</h3>
            <div className="receipt-row">
              <span>Date:</span>
              <span>{receipt.date}</span>
            </div>
            <div className="receipt-row">
              <span>Description:</span>
              <span>{receipt.description}</span>
            </div>
            <div className="receipt-row">
              <span>Payment Mode:</span>
              <span>{receipt.payment_mode}</span>
            </div>
            <div className="receipt-row">
              <span>Transaction ID:</span>
              <span>{receipt.reference}</span>
            </div>
          </div>

          <div className="receipt-amount">
            <span>Amount Paid:</span>
            <strong>₹{receipt.amount.toLocaleString()}</strong>
          </div>
        </div>

        <div className="receipt-footer">
          <p>This is a system-generated receipt. No signature required.</p>
          <button onClick={() => window.print()} className="btn btn-primary">Print Receipt</button>
        </div>
      </div>
    </div>
  );
}
