const API_BASE = "http://localhost:8000"; // Replace with your backend URL

// Helper to validate MongoDB ObjectId string format
export function isValidObjectId(id) {
  return /^[a-fA-F0-9]{24}$/.test(id);
}

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
    const errorText = await res.text();
    console.error("Update failed:", errorText);
    throw new Error("Failed to update product");
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
    const errorText = await res.text();
    console.error("Delete failed:", errorText);
    throw new Error("Failed to delete product");
  }
  // No response JSON expected on delete
}
