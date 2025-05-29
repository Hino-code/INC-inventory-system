// src/api/productAPI.js

const API_BASE = "http://localhost:8000"; // ← change if backend URL differs

// Helper to validate MongoDB ObjectId string format
export function isValidObjectId(id) {
  return /^[a-fA-F0-9]{24}$/.test(id);
}

// ——— CRUD Operations ———

export async function fetchProducts(token) {
  const res = await fetch(`${API_BASE}/products`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch products");
  return res.json();
}

export async function createProduct(token, product) {
  const res = await fetch(`${API_BASE}/products`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(product),
  });
  if (!res.ok) throw new Error("Failed to create product");
  return res.json();
}

export async function updateProduct(token, id, product) {
  if (!isValidObjectId(id)) {
    throw new Error("Invalid product ID");
  }
  const res = await fetch(`${API_BASE}/products/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(product),
  });
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Failed to update product: ${errText}`);
  }
  return res.json();
}

export async function deleteProduct(token, id) {
  if (!isValidObjectId(id)) {
    throw new Error("Invalid product ID");
  }
  const res = await fetch(`${API_BASE}/products/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Failed to delete product: ${errText}`);
  }
}

// ——— JSON Report Fetchers ———

export async function fetchExpiredItems(token) {
  const res = await fetch(`${API_BASE}/reports/expired-items`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch expired items");
  const { expired_items } = await res.json();
  return expired_items;
}

export async function fetchLowStockItems(token) {
  const res = await fetch(`${API_BASE}/reports/low-stock`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch low-stock items");
  const { low_stock_items } = await res.json();
  return low_stock_items;
}

export async function fetchSummaryReport(token) {
  const res = await fetch(`${API_BASE}/reports/summary`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch summary report");
  return res.json();
}

// ——— PDF Download Helpers ———

// Internal util to fetch a PDF and return as Blob
async function fetchReportPDF(path, token) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Report download failed: ${errText}`);
  }
  return res.blob();
}

// Exposed download functions
export function downloadExpiredItemsPDF(token) {
  return fetchReportPDF("/reports/expired-items/pdf", token);
}

export function downloadLowStockPDF(token) {
  return fetchReportPDF("/reports/low-stock/pdf", token);
}

export function downloadSummaryPDF(token) {
  return fetchReportPDF("/reports/summary/pdf", token);
}
