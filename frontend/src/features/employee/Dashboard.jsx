// src/pages/employee/EmployeeDashboard.jsx
import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../layouts/DashboardLayout';
import ProductTable from '../../components/ProductTable';
import {
  fetchProducts,
  fetchSummaryReport,
  downloadExpiredItemsPDF,
  downloadLowStockPDF,
  downloadSummaryPDF
} from '../../services/productAPI';

export default function EmployeeDashboard({ onLogout }) {
  const [products, setProducts] = useState([]);
  const [summary, setSummary]   = useState(null);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setError('No auth token');
      setLoading(false);
      return;
    }

    Promise.all([
      fetchProducts(token),
      fetchSummaryReport(token)
    ])
      .then(([productsData, summaryData]) => {
        setProducts(productsData);
        setSummary(summaryData);
      })
      .catch(err => {
        console.error(err);
        setError('Failed to load dashboard data');
      })
      .finally(() => setLoading(false));
  }, []);

  const downloadReport = async (type) => {
    const token = localStorage.getItem('token');
    if (!token) return alert('No auth token');

    const map = {
      expired: { fn: downloadExpiredItemsPDF, filename: 'expired_products_report.pdf' },
      refill:  { fn: downloadLowStockPDF,       filename: 'low_stock_report.pdf' },
      summary: { fn: downloadSummaryPDF,        filename: 'inventory_summary_report.pdf' }
    }[type];

    try {
      const blob = await map.fn(token);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = map.filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (e) {
      console.error(e);
      alert(`Error downloading ${type} report: ${e.message}`);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <p>Loading…</p>
      </DashboardLayout>
    );
  }
  if (error) {
    return (
      <DashboardLayout>
        <div className="alert alert-danger">{error}</div>
      </DashboardLayout>
    );
  }

  const totalCategories = Object.keys(summary.products_by_category || {}).length;

  return (
    <DashboardLayout>
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h3>Welcome, Employee.</h3>
        <button className="btn btn-outline-secondary" onClick={onLogout}>
          Logout
        </button>
      </div>

      {/* 1. Summary Cards */}
      <div className="row justify-content-center mb-5">
  <div className="col-sm-6 col-md-4 mb-3">
    <div className="card shadow-sm border-0 text-center">
      <div className="card-body">
        <h6 className="text-muted">Expired Items</h6>
        <h2 className="fw-bold" style={{ color: '#dc3545' }}>{summary.total_expired}</h2>
      </div>
    </div>
  </div>
  <div className="col-sm-6 col-md-4 mb-3">
    <div className="card shadow-sm border-0 text-center">
      <div className="card-body">
        <h6 className="text-muted">Low-Stock Items</h6>
        <h2 className="fw-bold" style={{ color: '#ffc107' }}>{summary.total_low_stock}</h2>
      </div>
    </div>
  </div>
  <div className="col-sm-6 col-md-4 mb-3">
    <div className="card shadow-sm border-0 text-center">
      <div className="card-body">
        <h6 className="text-muted">Total Categories</h6>
        <h2 className="fw-bold" style={{ color: '#0dcaf0' }}>{totalCategories}</h2>
      </div>
    </div>
  </div>
</div>

      {/* 2. Product Table */}
      <section className="mb-4">
        <h4>All Products</h4>
        <ProductTable data={products} />
      </section>

      {/* 3. Download Buttons */}
      <section>
        <h4>Download Reports</h4>
        <div className="d-flex gap-2">
          <button
            className="btn btn-warning"
            onClick={() => downloadReport('expired')}
          >
            Download Expired Items PDF
          </button>
          <button
            className="btn btn-info text-white"
            onClick={() => downloadReport('refill')}
          >
            Download Low-Stock PDF
          </button>
          <button
            className="btn btn-primary"
            onClick={() => downloadReport('summary')}
          >
            Download Summary PDF
          </button>
        </div>
      </section>
    </DashboardLayout>
  );
}
