import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './StudentAddPage.css';

export default function StudentAddPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    department_id: '1',
    year: '1',
    status: 'Active'
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Adding student:', formData);
    navigate('/students');
  };

  return (
    <div className="page-container">
      <h1>Add New Student</h1>
      <form onSubmit={handleSubmit} className="form-card">
        <div className="form-group">
          <label>First Name</label>
          <input type="text" name="first_name" value={formData.first_name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Last Name</label>
          <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Phone</label>
          <input type="tel" name="phone" value={formData.phone} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Department</label>
          <select name="department_id" value={formData.department_id} onChange={handleChange}>
            <option value="1">CSE</option>
            <option value="2">ECE</option>
            <option value="3">ME</option>
            <option value="4">CE</option>
            <option value="5">EEE</option>
          </select>
        </div>
        <div className="form-group">
          <label>Year</label>
          <select name="year" value={formData.year} onChange={handleChange}>
            <option value="1">First Year</option>
            <option value="2">Second Year</option>
            <option value="3">Third Year</option>
            <option value="4">Fourth Year</option>
          </select>
        </div>
        <div className="form-buttons">
          <button type="submit" className="btn btn-primary">Add Student</button>
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/students')}>Cancel</button>
        </div>
      </form>
    </div>
  );
}
