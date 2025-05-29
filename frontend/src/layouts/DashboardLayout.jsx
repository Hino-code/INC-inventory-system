// src/layouts/DashboardLayout.jsx
import React from "react";
import Sidebar from "../components/Sidebar";
import { ownerMenu, employeeMenu } from "../components/menu";

export default function DashboardLayout({ children }) {
  // determine role however you like—localStorage, context, redux, etc.
  const role = localStorage.getItem("role");
  const menuItems = role === "owner" ? ownerMenu : employeeMenu;

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar menuItems={menuItems} />
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
