import React from 'react';
import { Link } from 'react-router-dom';
import { X, Grid3x3, Users, Calendar, Award, CreditCard, Clock, FileText } from 'lucide-react';
import './Sidebar.css';

export default function Sidebar({ open, onClose }) {
  const menuItems = [
    { label: 'Dashboard', path: '/', icon: Grid3x3 },
    { label: 'Students', path: '/students', icon: Users },
    { label: 'Attendance', path: '/attendance', icon: Calendar },
    { label: 'Marks', path: '/marks', icon: Award },
    { label: 'Fees', path: '/fees', icon: CreditCard },
    { label: 'Timetable', path: '/timetable', icon: Clock },
    { label: 'Reports', path: '/reports', icon: FileText },
  ];

  return (
    <aside className={`sidebar ${open ? 'open' : 'closed'}`}>
      <div className="sidebar-header">
        <h2>EduManage</h2>
        <button className="close-btn" onClick={onClose}>
          <X size={24} />
        </button>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link key={item.path} to={item.path} className="nav-link" onClick={onClose}>
              <Icon size={20} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
