import React, { useState, useEffect } from "react";
import DashboardLayout from "../../layouts/DashboardLayout";
import {
  fetchProducts,
  createProduct,
  updateProduct,
  deleteProduct,
} from "../../services/productAPI";

// Modal component for add/edit
function Modal({ visible, onClose, onSave, initialData }) {
  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    quantity: "",
    is_active: true,
  });

  useEffect(() => {
    if (initialData) {
      setForm({
        name: initialData.name || "",
        category: initialData.category || "",
        price: initialData.price ?? "",
        quantity: initialData.quantity ?? "",
        is_active: initialData.is_active ?? true,
      });
    } else {
      setForm({
        name: "",
        category: "",
        price: "",
        quantity: "",
        is_active: true,
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
    const submitData = {
      ...form,
      price: parseFloat(form.price),
      quantity: parseInt(form.quantity, 10),
      is_active: form.is_active,
    };
    onSave(submitData);
  };

  return (
    <div style={backdropStyle}>
      <div style={modalStyle}>
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
              autoFocus
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
            <label>Quantity</label>
            <input
              name="quantity"
              type="number"
              className="form-control"
              value={form.quantity}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-check mb-3">
            <input
              id="is_active"
              name="is_active"
              type="checkbox"
              className="form-check-input"
              checked={form.is_active}
              onChange={handleChange}
            />
            <label htmlFor="is_active" className="form-check-label">
              Active
            </label>
          </div>
          <button type="submit" className="btn btn-primary me-2">
            {initialData ? "Update" : "Add"}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onClose}
          >
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

export default function ItemServicesDashboard({ onLogout }) {
  const [items, setItems] = useState([]);
  const [quickCreateName, setQuickCreateName] = useState("");
  const [quickCreatePrice, setQuickCreatePrice] = useState("");
  const [quickCreateQuantity, setQuickCreateQuantity] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editId, setEditId] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const token = localStorage.getItem("token");

  useEffect(() => {
    loadProducts();
  }, []);

  // Load and normalize products
  const loadProducts = () => {
    setLoading(true);
    setError(null);
    fetchProducts(token)
      .then((data) => {
        const normalized = data.map((item) => ({
          ...item,
          id: item.id || (item._id ? item._id.toString() : undefined),
          quantity: item.quantity ?? 0,
          is_active: item.is_active ?? true,
        }));
        setItems(normalized);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  const handleEditClick = (item) => {
    if (!item.id) {
      alert("Invalid item ID");
      return;
    }
    setEditId(item.id);
    setEditForm({ ...item });
  };

  const handleDeleteClick = async (id) => {
    if (!id) {
      alert("Invalid item ID");
      return;
    }
    if (!window.confirm("Are you sure you want to delete this item?")) return;
    try {
      await deleteProduct(token, id);
      loadProducts();
    } catch (err) {
      alert("Failed to delete item: " + err.message);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setEditForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSave = async () => {
    if (!editId) {
      alert("No item selected for editing");
      return;
    }

    const updateData = {};
    if (editForm.name) updateData.name = editForm.name;
    if (editForm.category) updateData.category = editForm.category;
    if (editForm.price !== "" && editForm.price !== undefined)
      updateData.price = parseFloat(editForm.price);
    if (editForm.quantity !== "" && editForm.quantity !== undefined)
      updateData.quantity = parseInt(editForm.quantity, 10);
    if (editForm.is_active !== undefined) updateData.is_active = editForm.is_active;

    try {
      await updateProduct(token, editId, updateData);
      setEditId(null);
      setEditForm({});
      loadProducts();
    } catch (err) {
      alert("Failed to update item: " + err.message);
    }
  };

  const handleCreateItem = async (item) => {
    try {
      await createProduct(token, item);
      setShowCreateModal(false);
      loadProducts();
    } catch (err) {
      alert("Failed to create item: " + err.message);
    }
  };

  const handleQuickCreate = async () => {
    if (!quickCreateName || !quickCreatePrice) {
      alert("Enter name & price");
      return;
    }
    const newItem = {
      name: quickCreateName,
      category: "Uncategorized",
      price: parseFloat(quickCreatePrice),
      quantity: parseInt(quickCreateQuantity, 10) || 0,
      is_active: true,
    };
    try {
      await createProduct(token, newItem);
      setQuickCreateName("");
      setQuickCreatePrice("");
      setQuickCreateQuantity("");
      loadProducts();
    } catch (err) {
      alert("Failed to add item: " + err.message);
    }
  };

  const handleCancel = () => {
    setEditId(null);
    setEditForm({});
  };

  return (
    <DashboardLayout>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h3>Items & Services</h3>
        <button className="btn btn-outline-secondary" onClick={onLogout}>
          Logout
        </button>
      </div>

      <div className="d-flex flex-wrap gap-2 mb-3 align-items-center">
        <input
          type="search"
          placeholder="Search"
          className="form-control w-auto"
        />
        <input
          type="text"
          placeholder="Category"
          className="form-control w-auto"
        />
        <button className="btn btn-outline-secondary">Status: Active</button>
        <button className="btn btn-outline-secondary">All filters</button>
        <div className="ms-auto d-flex gap-2">
          <button
            className="btn btn-outline-primary"
            onClick={() => alert("Actions dropdown clicked")}
          >
            Actions
          </button>
          <button
            className="btn btn-primary"
            onClick={() => setShowCreateModal(true)}
          >
            Create item
          </button>
        </div>
      </div>

      {loading && <p>Loading products...</p>}
      {error && <p className="text-danger">Error: {error}</p>}

      {!loading && !error && (
        <table className="table align-middle table-borderless">
          <thead>
            <tr>
              <th style={{ width: "40px" }}>
                <input type="checkbox" />
              </th>
              <th>Item</th>
              <th>Reporting category</th>
              <th>Quantity</th>
              <th>Price</th>
              <th style={{ width: "120px" }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr key="quick-create">
              <td>
                <button className="btn btn-outline-secondary btn-sm">+</button>
              </td>
              <td>
                <input
                  type="text"
                  className="form-control form-control-sm"
                  placeholder="Quick create"
                  value={quickCreateName}
                  onChange={(e) => setQuickCreateName(e.target.value)}
                />
              </td>
              <td></td>
              <td>
                <input
                  type="number"
                  className="form-control form-control-sm"
                  placeholder="Quantity"
                  value={quickCreateQuantity}
                  onChange={(e) => setQuickCreateQuantity(e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  className="form-control form-control-sm"
                  placeholder="Price"
                  value={quickCreatePrice}
                  onChange={(e) => setQuickCreatePrice(e.target.value)}
                />
              </td>
              <td>
                <button
                  className="btn btn-primary btn-sm"
                  onClick={handleQuickCreate}
                >
                  Save
                </button>
              </td>
            </tr>

            {items.map((item) =>
              editId === item.id ? (
                <tr key={item.id}>
                  <td>
                    <input type="checkbox" />
                  </td>
                  <td>
                    <input
                      name="name"
                      value={editForm.name}
                      onChange={handleChange}
                      className="form-control form-control-sm"
                    />
                  </td>
                  <td>
                    <input
                      name="category"
                      value={editForm.category}
                      onChange={handleChange}
                      className="form-control form-control-sm"
                    />
                  </td>
                  <td>
                    <input
                      name="quantity"
                      type="number"
                      value={editForm.quantity}
                      onChange={handleChange}
                      className="form-control form-control-sm"
                    />
                  </td>
                  <td>
                    <input
                      name="price"
                      type="number"
                      value={editForm.price}
                      onChange={handleChange}
                      className="form-control form-control-sm"
                    />
                  </td>
                  <td>
                    <button
                      className="btn btn-sm btn-primary me-2"
                      onClick={handleSave}
                    >
                      Save
                    </button>
                    <button
                      className="btn btn-sm btn-secondary"
                      onClick={handleCancel}
                    >
                      Cancel
                    </button>
                  </td>
                </tr>
              ) : (
                <tr key={item.id}>
                  <td>
                    <input type="checkbox" />
                  </td>
                  <td>{item.name}</td>
                  <td>{item.category}</td>
                  <td>{item.quantity}</td>
                  <td>₱{Number(item.price).toFixed(2)}</td>
                  <td>
                    <button
                      className="btn btn-link btn-sm me-2"
                      onClick={() => handleEditClick(item)}
                      title="Edit"
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-link btn-sm text-danger"
                      onClick={() => handleDeleteClick(item.id)}
                      title="Delete"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              )
            )}
          </tbody>
        </table>
      )}

      <Modal
        visible={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSave={handleCreateItem}
        initialData={editId ? editForm : null}
      />
    </DashboardLayout>
  );
}
