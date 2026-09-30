import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { studentAPI } from '../services/api';
import './StudentListPage.css';

export default function StudentListPage() {
  const [students, setStudents] = useState([
    {
      id: 1,
      student_id: 'STU202601',
      first_name: 'John',
      last_name: 'Doe',
      email: 'john@college.edu',
      phone: '9876543210',
      department_id: 1,
      year: 1,
      status: 'Active'
    },
    {
      id: 2,
      student_id: 'STU202602',
      first_name: 'Jane',
      last_name: 'Smith',
      email: 'jane@college.edu',
      phone: '9876543211',
      department_id: 1,
      year: 1,
      status: 'Active'
    },
    {
      id: 3,
      student_id: 'STU202603',
      first_name: 'Robert',
      last_name: 'Johnson',
      email: 'robert@college.edu',
      phone: '9876543212',
      department_id: 2,
      year: 2,
      status: 'Active'
    }
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');

  const handleSearch = (e) => {
    const term = e.target.value.toLowerCase();
    setSearch(term);
  };

  const filteredStudents = students.filter(s => 
    s.student_id.toLowerCase().includes(search) ||
    s.first_name.toLowerCase().includes(search) ||
    s.last_name.toLowerCase().includes(search) ||
    s.email.toLowerCase().includes(search) ||
    s.phone.includes(search)
  );

  const handleDelete = (id) => {
    if (confirm('Are you sure you want to delete this student?')) {
      setStudents(students.filter(s => s.id !== id));
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Student Management</h1>
        <Link to="/students/add" className="btn btn-primary">
          + Add Student
        </Link>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card">
        <div className="card-body">
          <input
            type="text"
            placeholder="Search by name, ID, email, or phone..."
            value={search}
            onChange={handleSearch}
            className="search-input"
          />
        </div>
      </div>

      <div className="card">
        {filteredStudents.length === 0 ? (
          <div className="empty-state">
            <p>No students found. <Link to="/students/add">Add a new student</Link></p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Student ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Year</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredStudents.map(student => (
                <tr key={student.id}>
                  <td>{student.student_id}</td>
                  <td>{student.first_name} {student.last_name}</td>
                  <td>{student.email}</td>
                  <td>{student.phone}</td>
                  <td>{student.year}</td>
                  <td>
                    <span className={`status status-${student.status.toLowerCase()}`}>
                      {student.status}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <Link to={`/students/${student.id}`} className="btn btn-sm btn-secondary">
                        View
                      </Link>
                      <Link to={`/students/${student.id}/edit`} className="btn btn-sm btn-secondary">
                        Edit
                      </Link>
                      <button
                        onClick={() => handleDelete(student.id)}
                        className="btn btn-sm btn-danger"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
