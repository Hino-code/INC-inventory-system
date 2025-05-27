import React, { useState, useEffect, useRef } from 'react';
import DashboardLayout from "../../layouts/DashboardLayout";
import "./employeeDashboard.css"

export default function EmployeeDashboard({ onLogout }) {
  const [date, setDate] = useState('');
  const dateInputRef = useRef(null);

  // Set today's date on mount
  useEffect(() => {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    setDate(`${yyyy}-${mm}-${dd}`);
  }, []);

  // When the formatted date is clicked, show the native date picker
  const handleDateClick = () => {
    if (dateInputRef.current) {
      dateInputRef.current.showPicker?.() || dateInputRef.current.click();
    }
  };

  // Format date to something like "May 26"
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const options = { month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <DashboardLayout>
      <div>
        {/* Header with logout */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h3>Welcome, Employee.</h3>
          <button className="btn btn-outline-secondary" onClick={onLogout}>
            Logout
          </button>
        </div>

        <hr />

        {/* Performance Section */}
        <section className="mb-4">
  <div className="mb-2">
    <h4>Performance</h4>
  </div>

  {/* Hidden date input */}
  <input
    ref={dateInputRef}
    type="date"
    className="form-control w-auto visually-hidden"
    value={date}
    onChange={(e) => setDate(e.target.value)}
    max={new Date().toISOString().split("T")[0]}
  />

  {/* Clickable formatted date box (now below heading) */}
  <div
    className="border rounded px-3 py-1 d-inline-block mb-3"
    style={{ cursor: 'pointer', userSelect: 'none' }}
    onClick={handleDateClick}
    title="Click to change date"
  >
    <div className='Date'>
      <span className="label">Date</span>
      <span className="value">{formatDate(date)}</span>
    </div>
  </div>

  {/* Summary content */}
  <p>Summary data for {formatDate(date)} will appear here.</p>
</section>

      </div>
    </DashboardLayout>
  );
}
