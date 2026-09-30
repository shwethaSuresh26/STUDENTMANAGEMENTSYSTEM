import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './MarksEditPage.css';

export default function MarksEditPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [formData, setFormData] = useState({
    student_id: '1',
    subject_id: '1',
    marks: '85',
    total: '100'
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Updating marks:', id, formData);
    navigate('/marks');
  };

  return (
    <div className="page-container">
      <h1>Edit Marks (ID: {id})</h1>
      <form onSubmit={handleSubmit} className="form-card">
        <div className="form-group">
          <label>Student</label>
          <select name="student_id" value={formData.student_id} onChange={handleChange}>
            <option value="1">John Doe</option>
            <option value="2">Jane Smith</option>
          </select>
        </div>
        <div className="form-group">
          <label>Subject</label>
          <select name="subject_id" value={formData.subject_id} onChange={handleChange}>
            <option value="1">Mathematics</option>
            <option value="2">Physics</option>
            <option value="3">Chemistry</option>
          </select>
        </div>
        <div className="form-group">
          <label>Marks</label>
          <input type="number" name="marks" min="0" max="100" value={formData.marks} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Total</label>
          <input type="number" name="total" value={formData.total} onChange={handleChange} />
        </div>
        <div className="form-buttons">
          <button type="submit" className="btn btn-primary">Update Marks</button>
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/marks')}>Cancel</button>
        </div>
      </form>
    </div>
  );
}
