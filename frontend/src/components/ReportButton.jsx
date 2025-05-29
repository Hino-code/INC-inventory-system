// src/components/ReportButton.jsx
import React from 'react';

/**
 * A button which, when clicked, triggers download of a PDF report.
 * 
 * Props:
 *  - type: string  // e.g. "expired", "refill", "damaged"
 *  - data: array   // the items to include in the report
 */
export default function ReportButton({ type, data }) {
  const handleDownload = () => {
    // For now, just log. Later: generate PDF or call backend endpoint.
    console.log(`Downloading ${type} report for`, data);
    // e.g. using jsPDF or open a /reports/:type/pdf endpoint:
    // window.open(`/api/reports/${type}/pdf`, '_blank');
  };

  // Human-friendly label
  const labels = {
    expired: 'Expired Items',
    refill:  'Refill Alerts',
    damaged: 'Damaged Items'
  };

  return (
    <button className="btn btn-primary" onClick={handleDownload}>
      Download {labels[type] || type} Report
    </button>
  );
}
