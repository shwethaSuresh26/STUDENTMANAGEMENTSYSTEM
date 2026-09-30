import React from 'react';
import { Menu, LogOut } from 'lucide-react';
import './Header.css';

export default function Header({ onToggleSidebar, user, onLogout }) {
  return (
    <header className="header">
      <div className="header-left">
        <button className="toggle-btn" onClick={onToggleSidebar} title="Toggle Sidebar">
          <Menu size={24} />
        </button>
        <h1 className="page-title">Student Management System</h1>
      </div>
      <div className="header-right">
        <div className="user-section">
          <span className="user-name">{user?.full_name || 'User'}</span>
          <button className="logout-btn" onClick={onLogout} title="Logout">
            <LogOut size={20} />
          </button>
        </div>
      </div>
    </header>
  );
}
