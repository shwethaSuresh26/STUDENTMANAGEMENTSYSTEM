import React, { useState, useContext } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { AuthContext } from '../../App';
import Sidebar from './Sidebar';
import Header from './Header';
import './Layout.css';

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { user, handleLogout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogoutClick = async () => {
    handleLogout();
    navigate('/login');
  };

  return (
    <div className="layout">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="layout-main">
        <Header onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} user={user} onLogout={handleLogoutClick} />
        <main className="layout-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
