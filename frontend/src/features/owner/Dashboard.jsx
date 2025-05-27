import React, { useEffect, useState } from "react";
import DashboardLayout from "../../layouts/DashboardLayout";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import "./Dashboard.css";

const currencyFormatter = new Intl.NumberFormat("en-PH", {
  style: "currency",
  currency: "PHP",
  minimumFractionDigits: 2,
});

const SummaryCard = ({ label, value }) => (
  <div className="col-md-6 col-lg-3">
    <div className="card p-3 shadow-sm dashboard-card">
      <small className="text-muted">{label}</small>
      <h5>{value}</h5>
    </div>
  </div>
);

export default function OwnerDashboard({ onLogout }) {
  const [summary, setSummary] = useState({
    net_sales: 0,
    transactions: 0,
    gross_sales: 0,
    average_net_sale: 0,
  });

  const [salesData, setSalesData] = useState([]);

  const [date, setDate] = useState(() => new Date().toISOString().split("T")[0]); // yyyy-mm-dd

  useEffect(() => {
    async function fetchSummary() {
      const token = localStorage.getItem("token");
      try {
        const response = await fetch(`http://localhost:8000/dashboard/summary?date=${date}`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) throw new Error("Failed to fetch summary");
        const data = await response.json();
        setSummary(data);
      } catch (error) {
        console.error(error);
      }
    }

    async function fetchSalesData() {
      const token = localStorage.getItem("token");
      try {
        const response = await fetch(`http://localhost:8000/dashboard/sales-data?date=${date}`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) throw new Error("Failed to fetch sales data");
        const data = await response.json();
        setSalesData(data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchSummary();
    fetchSalesData();
  }, [date]);

  return (
    <DashboardLayout>
      <div>
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h3>Welcome back.</h3>
          <button className="btn btn-outline-secondary" onClick={onLogout}>
            Logout
          </button>
        </div>

        <hr />

        <section className="mb-4">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h4>Performance</h4>
            <input
              type="date"
              className="form-control w-auto"
              value={date}
              max={new Date().toISOString().split("T")[0]}
              onChange={(e) => setDate(e.target.value)}
              aria-label="Select date"
            />
          </div>

          <div className="row g-3 mb-4">
            <SummaryCard label="Net Sales" value={currencyFormatter.format(summary.net_sales)} />
            <SummaryCard label="Transactions" value={summary.transactions} />
            <SummaryCard label="Gross Sales" value={currencyFormatter.format(summary.gross_sales)} />
            <SummaryCard label="Average Net Sale" value={currencyFormatter.format(summary.average_net_sale)} />
          </div>

          <div style={{ width: "100%", height: 300 }}>
            <ResponsiveContainer>
              <LineChart data={salesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis tickFormatter={(value) => currencyFormatter.format(value)} />
                <Tooltip formatter={(value) => currencyFormatter.format(value)} />
                <Line
                  type="monotone"
                  dataKey="net_sales"
                  stroke="#1f77b4"
                  strokeWidth={3}
                  dot={{ r: 5 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* You can add more dashboard sections here */}

      </div>
    </DashboardLayout>
  );
}
