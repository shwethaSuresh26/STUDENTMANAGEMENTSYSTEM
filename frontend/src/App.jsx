import React, { useState, useEffect, createContext } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { authAPI } from './services/api';
import './App.css';

// Layout
import Layout from './components/common/Layout';

// Pages
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import StudentListPage from './pages/StudentListPage';
import StudentAddPage from './pages/StudentAddPage';
import StudentEditPage from './pages/StudentEditPage';
import StudentViewPage from './pages/StudentViewPage';
import AttendanceIndexPage from './pages/AttendanceIndexPage';
import AttendanceMarkPage from './pages/AttendanceMarkPage';
import AttendanceLowPage from './pages/AttendanceLowPage';
import AttendanceReportPage from './pages/AttendanceReportPage';
import MarksIndexPage from './pages/MarksIndexPage';
import MarksAddPage from './pages/MarksAddPage';
import MarksEditPage from './pages/MarksEditPage';
import MarksMarksheetPage from './pages/MarksMarksheetPage';
import FeesIndexPage from './pages/FeesIndexPage';
import FeesAddPage from './pages/FeesAddPage';
import FeesReceiptPage from './pages/FeesReceiptPage';
import FeesLedgerPage from './pages/FeesLedgerPage';
import TimetableIndexPage from './pages/TimetableIndexPage';
import TimetableManagePage from './pages/TimetableManagePage';
import ReportsIndexPage from './pages/ReportsIndexPage';
import StudentReportPage from './pages/StudentReportPage';
import ChangePasswordPage from './pages/ChangePasswordPage';

// Create auth context
export const AuthContext = createContext();

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  useEffect(() => {
    // Check if user is logged in on app load
    const checkAuth = async () => {
      try {
        const response = await authAPI.getCurrentUser();
        setUser(response.data);
      } catch (error) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setAuthError(null);
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ user, handleLogin, handleLogout }}>
      <BrowserRouter>
        <Routes>
          {!user ? (
            <>
              <Route path="/login" element={<LoginPage />} />
              <Route path="*" element={<Navigate to="/login" />} />
            </>
          ) : (
            <Route element={<Layout />}>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/dashboard" element={<DashboardPage />} />
              
              {/* Student Routes */}
              <Route path="/students" element={<StudentListPage />} />
              <Route path="/students/add" element={<StudentAddPage />} />
              <Route path="/students/:id" element={<StudentViewPage />} />
              <Route path="/students/:id/edit" element={<StudentEditPage />} />

              {/* Attendance Routes */}
              <Route path="/attendance" element={<AttendanceIndexPage />} />
              <Route path="/attendance/mark" element={<AttendanceMarkPage />} />
              <Route path="/attendance/low-attendance" element={<AttendanceLowPage />} />
              <Route path="/attendance/report" element={<AttendanceReportPage />} />

              {/* Marks Routes */}
              <Route path="/marks" element={<MarksIndexPage />} />
              <Route path="/marks/add" element={<MarksAddPage />} />
              <Route path="/marks/edit/:id" element={<MarksEditPage />} />
              <Route path="/marks/marksheet/:studentId" element={<MarksMarksheetPage />} />

              {/* Fees Routes */}
              <Route path="/fees" element={<FeesIndexPage />} />
              <Route path="/fees/add" element={<FeesAddPage />} />
              <Route path="/fees/receipt/:paymentId" element={<FeesReceiptPage />} />
              <Route path="/fees/student/:studentId" element={<FeesLedgerPage />} />

              {/* Timetable Routes */}
              <Route path="/timetable" element={<TimetableIndexPage />} />
              <Route path="/timetable/manage" element={<TimetableManagePage />} />

              {/* Reports Routes */}
              <Route path="/reports" element={<ReportsIndexPage />} />
              <Route path="/reports/students" element={<StudentReportPage />} />

              {/* Account Routes */}
              <Route path="/change-password" element={<ChangePasswordPage />} />
            </Route>
          )}
        </Routes>
      </BrowserRouter>
    </AuthContext.Provider>
  );
}

export default App;
