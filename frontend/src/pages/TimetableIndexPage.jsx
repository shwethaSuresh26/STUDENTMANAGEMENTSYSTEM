import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './TimetableIndexPage.css';

export default function TimetableIndexPage() {
  const [timetable] = useState([
    { id: 1, day: 'Monday', subject: 'Mathematics', room: '101', time: '09:00-10:00' },
    { id: 2, day: 'Monday', subject: 'Physics', room: '102', time: '10:15-11:15' },
    { id: 3, day: 'Tuesday', subject: 'Chemistry', room: '103', time: '09:00-10:00' },
    { id: 4, day: 'Tuesday', subject: 'English', room: '104', time: '10:15-11:15' },
    { id: 5, day: 'Wednesday', subject: 'History', room: '105', time: '09:00-10:00' },
  ]);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Timetable Management</h1>
        <Link to="/timetable/manage" className="btn btn-primary">+ Manage Timetable</Link>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Day</th>
              <th>Subject</th>
              <th>Time</th>
              <th>Room</th>
            </tr>
          </thead>
          <tbody>
            {timetable.map(slot => (
              <tr key={slot.id}>
                <td>{slot.day}</td>
                <td>{slot.subject}</td>
                <td>{slot.time}</td>
                <td>{slot.room}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
