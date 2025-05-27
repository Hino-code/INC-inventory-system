import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';

import Login from './features/auth/Login';
import OwnerDashboard from './features/owner/Dashboard';
import EmployeeDashboard from './features/employee/Dashboard';
import ItemsServicesDashboard from './features/owner/ItemsServicesDashboard';

export default function App() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // On mount, check for token and role in localStorage
  useEffect(() => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    if (token && role) {
      setUser({ role });
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    if (userData.role === 'owner') {
      navigate('/owner/dashboard');
    } else if (userData.role === 'employee') {
      navigate('/employee/dashboard');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    setUser(null);
    navigate('/login');
  };

  if (!user) {
    // Not logged in, only allow login route
    return (
      <Routes>
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    );
  }

  return (
    <Routes>
      {/* Owner routes */}
      {user.role === 'owner' && (
        <>
          <Route
            path="/owner/dashboard"
            element={<OwnerDashboard onLogout={handleLogout} />}
          />
          <Route
            path="/items"
            element={<ItemsServicesDashboard onLogout={handleLogout} />}
          />
        </>
      )}

      {/* Employee routes */}
      {user.role === 'employee' && (
        <Route
          path="/employee/dashboard"
          element={<EmployeeDashboard onLogout={handleLogout} />}
        />
      )}

      {/* Redirect root and unknown to dashboard */}
      <Route
        path="/"
        element={<Navigate to={`/${user.role}/dashboard`} replace />}
      />
      <Route
        path="*"
        element={<Navigate to={`/${user.role}/dashboard`} replace />}
      />
    </Routes>
  );
}
