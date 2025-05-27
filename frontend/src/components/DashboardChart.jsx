  import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

// Define colors for pie chart sections
const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

// Chart component to render line or pie chart
export default function DashboardChart({ data, title, type = "line" }) {
  return (
    <div>
      <h4>{title}</h4>
      <ResponsiveContainer width="100%" height={300}>
        {type === "line" ? (
          // Line chart for time-series (e.g., sales trends over time)
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="net_sales" // The key for the net sales data
              stroke="#1f77b4"
              strokeWidth={3}
              dot={{ r: 5 }} // Add a small circle at each data point
              activeDot={{ r: 7 }} // Increase the size of the active dot
            />
          </LineChart>
        ) : (
          // Pie chart for categorical data (e.g., payment type breakdown)
          <PieChart>
            <Pie
              data={data}
              dataKey="total_amount" // The key for the total amount of each payment type
              nameKey="payment_type" // The label for each slice
              cx="50%" // Center the pie chart
              cy="50%" // Center the pie chart
              outerRadius={80} // Size of the pie chart
              fill="#8884d8"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
