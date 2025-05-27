import React, { useState, useEffect } from "react";

export default function ItemForm({ visible, onClose, onSubmit, initialData }) {
  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    stock: "",
    isActive: true,
  });

  useEffect(() => {
    if (initialData) {
      setForm({
        name: initialData.name || "",
        category: initialData.category || "",
        price: initialData.price || "",
        stock: initialData.stock || "",
        isActive: initialData.isActive ?? true,
      });
    } else {
      setForm({
        name: "",
        category: "",
        price: "",
        stock: "",
        isActive: true,
      });
    }
  }, [initialData]);

  if (!visible) return null;

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Validate fields here if needed
    onSubmit(form);
  };

  return (
    <div className="modal-backdrop" style={backdropStyle}>
      <div className="modal-content" style={modalStyle}>
        <h4>{initialData ? "Edit Item" : "Add New Item"}</h4>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label>Name</label>
            <input
              name="name"
              type="text"
              className="form-control"
              value={form.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label>Category</label>
            <input
              name="category"
              type="text"
              className="form-control"
              value={form.category}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label>Price</label>
            <input
              name="price"
              type="number"
              step="0.01"
              className="form-control"
              value={form.price}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label>Stock</label>
            <input
              name="stock"
              type="number"
              className="form-control"
              value={form.stock}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-check mb-3">
            <input
              id="isActive"
              name="isActive"
              type="checkbox"
              className="form-check-input"
              checked={form.isActive}
              onChange={handleChange}
            />
            <label htmlFor="isActive" className="form-check-label">
              Active
            </label>
          </div>

          <button type="submit" className="btn btn-primary me-2">
            {initialData ? "Update" : "Add"}
          </button>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
}

const backdropStyle = {
  position: "fixed",
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: "rgba(0,0,0,0.3)",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  zIndex: 1050,
};

const modalStyle = {
  backgroundColor: "white",
  padding: "20px",
  borderRadius: "8px",
  width: "400px",
  maxWidth: "90%",
};
