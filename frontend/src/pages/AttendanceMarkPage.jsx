import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AttendanceMarkPage.css';

export default function AttendanceMarkPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    subject_id: '1',
    students: [
      { id: 1, name: 'John Doe', status: 'Present' },
      { id: 2, name: 'Jane Smith', status: 'Present' },
      { id: 3, name: 'Robert Johnson', status: 'Absent' }
    ]
  });

  const handleStatusChange = (studentId, status) => {
    const updated = formData.students.map(s => 
      s.id === studentId ? { ...s, status } : s
    );
    setFormData({ ...formData, students: updated });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Marking attendance:', formData);
    navigate('/attendance');
  };

  return (
    <div className="page-container">
      <h1>Mark Attendance</h1>
      <form onSubmit={handleSubmit} className="form-card">
        <div className="form-group">
          <label>Date</label>
          <input type="date" value={formData.date} onChange={(e) => setFormData({ ...formData, date: e.target.value })} required />
        </div>
        <div className="form-group">
          <label>Subject</label>
          <select value={formData.subject_id} onChange={(e) => setFormData({ ...formData, subject_id: e.target.value })}>
            <option value="1">Mathematics</option>
            <option value="2">Physics</option>
            <option value="3">Chemistry</option>
            <option value="4">English</option>
          </select>
        </div>

        <div className="attendance-table">
          <table>
            <thead>
              <tr>
                <th>Student</th>
                <th>Present</th>
                <th>Absent</th>
                <th>Late</th>
                <th>Leave</th>
              </tr>
            </thead>
            <tbody>
              {formData.students.map(student => (
                <tr key={student.id}>
                  <td>{student.name}</td>
                  <td><input type="radio" name={`student_${student.id}`} checked={student.status === 'Present'} onChange={() => handleStatusChange(student.id, 'Present')} /></td>
                  <td><input type="radio" name={`student_${student.id}`} checked={student.status === 'Absent'} onChange={() => handleStatusChange(student.id, 'Absent')} /></td>
                  <td><input type="radio" name={`student_${student.id}`} checked={student.status === 'Late'} onChange={() => handleStatusChange(student.id, 'Late')} /></td>
                  <td><input type="radio" name={`student_${student.id}`} checked={student.status === 'Leave'} onChange={() => handleStatusChange(student.id, 'Leave')} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="form-buttons">
          <button type="submit" className="btn btn-primary">Save Attendance</button>
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/attendance')}>Cancel</button>
        </div>
      </form>
    </div>
  );
}
