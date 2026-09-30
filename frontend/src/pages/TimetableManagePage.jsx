import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './TimetableManagePage.css';

export default function TimetableManagePage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    day: 'Monday',
    subject_id: '1',
    time_start: '09:00',
    time_end: '10:00',
    room: '101'
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Adding timetable entry:', formData);
    navigate('/timetable');
  };

  return (
    <div className="page-container">
      <h1>Manage Timetable</h1>
      <form onSubmit={handleSubmit} className="form-card">
        <div className="form-group">
          <label>Day</label>
          <select name="day" value={formData.day} onChange={handleChange}>
            <option value="Monday">Monday</option>
            <option value="Tuesday">Tuesday</option>
            <option value="Wednesday">Wednesday</option>
            <option value="Thursday">Thursday</option>
            <option value="Friday">Friday</option>
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
          <label>Start Time</label>
          <input type="time" name="time_start" value={formData.time_start} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>End Time</label>
          <input type="time" name="time_end" value={formData.time_end} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Room/Classroom</label>
          <input type="text" name="room" value={formData.room} onChange={handleChange} required />
        </div>
        <div className="form-buttons">
          <button type="submit" className="btn btn-primary">Add to Timetable</button>
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/timetable')}>Cancel</button>
        </div>
      </form>
    </div>
  );
}
