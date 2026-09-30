import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChangePasswordPage.css';

export default function ChangePasswordPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.new_password !== formData.confirm_password) {
      setMessage('Passwords do not match!');
      return;
    }
    console.log('Changing password');
    setMessage('Password changed successfully!');
    setTimeout(() => navigate('/'), 2000);
  };

  return (
    <div className="page-container">
      <h1>Change Password</h1>
      {message && <div className={`alert ${message.includes('success') ? 'alert-success' : 'alert-danger'}`}>{message}</div>}
      <form onSubmit={handleSubmit} className="form-card">
        <div className="form-group">
          <label>Current Password</label>
          <input type="password" name="current_password" value={formData.current_password} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>New Password</label>
          <input type="password" name="new_password" value={formData.new_password} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Confirm Password</label>
          <input type="password" name="confirm_password" value={formData.confirm_password} onChange={handleChange} required />
        </div>
        <div className="form-buttons">
          <button type="submit" className="btn btn-primary">Change Password</button>
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/')}>Cancel</button>
        </div>
      </form>
    </div>
  );
}
