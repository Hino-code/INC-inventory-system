// src/config/menu.js
export const ownerMenu = [
  { name: 'Home',          icon: 'bi-house',         path: '/owner/dashboard' },
  { name: 'Items & Services', icon: 'bi-box-seam',   path: '/items' },
  { name: 'Reports',       icon: 'bi-file-bar-graph', path: '/reports' },
];

export const employeeMenu = [
  { name: 'Home',         icon: 'bi-house',            path: '/employee/dashboard' },
  { name: 'Products',     icon: 'bi-box-seam',         path: '/employee/products' },
  { name: 'Expired',      icon: 'bi-clock-history',    path: '/employee/reports/expired' },
  { name: 'Refill Alerts',icon: 'bi-droplet-half',     path: '/employee/reports/refill' },
  { name: 'Damaged',      icon: 'bi-exclamation-triangle', path: '/employee/reports/damaged' },
];
