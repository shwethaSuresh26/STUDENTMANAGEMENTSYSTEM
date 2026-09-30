import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './FeesAddPage.css';

export default function FeesAddPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    student_id: '1',
    amount: '',
    date: new Date().toISOString().split('T')[0],
    payment_mode: 'Cash',
    reference_number: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Recording fee payment:', formData);
    navigate('/fees');
  };

  return (
    <div className="page-container">
      <h1>Record Fee Payment</h1>
      <form onSubmit={handleSubmit} className="form-card">
        <div className="form-group">
          <label>Student</label>
          <select name="student_id" value={formData.student_id} onChange={handleChange}>
            <option value="1">John Doe</option>
            <option value="2">Jane Smith</option>
            <option value="3">Robert Johnson</option>
          </select>
        </div>
        <div className="form-group">
          <label>Amount (₹)</label>
          <input type="number" name="amount" min="0" value={formData.amount} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Payment Date</label>
          <input type="date" name="date" value={formData.date} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Payment Mode</label>
          <select name="payment_mode" value={formData.payment_mode} onChange={handleChange}>
            <option value="Cash">Cash</option>
            <option value="Cheque">Cheque</option>
            <option value="Bank Transfer">Bank Transfer</option>
            <option value="Online">Online</option>
          </select>
        </div>
        <div className="form-group">
          <label>Reference Number</label>
          <input type="text" name="reference_number" value={formData.reference_number} onChange={handleChange} />
        </div>
        <div className="form-buttons">
          <button type="submit" className="btn btn-primary">Record Payment</button>
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/fees')}>Cancel</button>
        </div>
      </form>
    </div>
  );
}
