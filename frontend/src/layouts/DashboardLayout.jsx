import React from "react";
import Sidebar from "../components/Sidebar";

export default function DashboardLayout({ children }) {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar />
      <main
        style={{
          flexGrow: 1,
          padding: "2rem",
          backgroundColor: "#f9fafb",
          minHeight: "100vh",
        }}
      >
        {children}
      </main>
    </div>
  );
}
