// src/components/Sidebar.jsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

export default function Sidebar({ menuItems }) {
  return (
    <nav className="sidebar p-3 bg-white" style={{ width: '220px', height: '100vh' }}>
      <ul className="nav nav-pills flex-column mb-auto">
        {menuItems.map(({ name, icon, path }) => (
          <li key={name} className="nav-item">
            <NavLink
              to={path}
              className={({ isActive }) =>
                'nav-link d-flex align-items-center ' + (isActive ? 'active' : 'text-dark')
              }
            >
              <i className={`bi ${icon} me-2`} />
              {name}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
