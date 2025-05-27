import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

export default function Sidebar() {
  const menuItems = [
  { name: 'Home', icon: 'bi-house', path: '/owner/dashboard' },
  { name: 'Items & Services', icon: 'bi-box-seam', path: '/items' },
  { name: 'Reports', icon: 'bi-file-bar-graph', path: '/reports' },
  { name: 'Settings', icon: 'bi-gear', path: '/settings' },
];


  return (
    <nav className="d-flex flex-column p-3 bg-white sidebar" style={{ width: '220px', height: '100vh' }}>
      <ul className="nav nav-pills flex-column mb-auto">
        {menuItems.map(({ name, icon, path }) => (
          <li className="nav-item" key={name}>
            <NavLink
              to={path}
              className={({ isActive }) =>
                'nav-link d-flex align-items-center ' + (isActive ? 'active' : 'text-dark')
              }
              {...(path === '/' ? { end: true } : {})}
            >
              <i className={`bi ${icon} me-2`}></i>
              {name}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
