import React, { useState } from "react";
import { updateProduct, deleteProduct } from "../../services/productAPI";

export default function ProductApiTest() {
  const [productId, setProductId] = useState("");
  const [updateName, setUpdateName] = useState("");
  const [updatePrice, setUpdatePrice] = useState("");
  const [updateQuantity, setUpdateQuantity] = useState("");
  const [updateIsActive, setUpdateIsActive] = useState(true);
  const [message, setMessage] = useState("");

  const token = localStorage.getItem("token");

  const handleUpdate = async () => {
    if (!productId) {
      setMessage("Please enter a product ID");
      return;
    }

    const updateData = {
      name: updateName,
      price: parseFloat(updatePrice),
      quantity: parseInt(updateQuantity, 10),
      is_active: updateIsActive,
    };

    try {
      console.log("Testing update with:", productId, updateData);
      await updateProduct(token, productId, updateData);
      setMessage("Update successful!");
    } catch (err) {
      console.error(err);
      setMessage("Update failed: " + err.message);
    }
  };

  const handleDelete = async () => {
    if (!productId) {
      setMessage("Please enter a product ID");
      return;
    }

    try {
      console.log("Testing delete with:", productId);
      await deleteProduct(token, productId);
      setMessage("Delete successful!");
    } catch (err) {
      console.error(err);
      setMessage("Delete failed: " + err.message);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Product API Test</h2>

      <div>
        <label>Product ID (MongoDB ObjectId):</label>
        <input
          type="text"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
          style={{ width: "400px", marginBottom: 10 }}
          placeholder="Enter product ID to update/delete"
        />
      </div>

      <div>
        <label>Update Name:</label>
        <input
          type="text"
          value={updateName}
          onChange={(e) => setUpdateName(e.target.value)}
          style={{ width: "400px", marginBottom: 10 }}
          placeholder="New product name"
        />
      </div>

      <div>
        <label>Update Price:</label>
        <input
          type="number"
          step="0.01"
          value={updatePrice}
          onChange={(e) => setUpdatePrice(e.target.value)}
          style={{ width: "400px", marginBottom: 10 }}
          placeholder="New price"
        />
      </div>

      <div>
        <label>Update Quantity:</label>
        <input
          type="number"
          value={updateQuantity}
          onChange={(e) => setUpdateQuantity(e.target.value)}
          style={{ width: "400px", marginBottom: 10 }}
          placeholder="New quantity"
        />
      </div>

      <div>
        <label>
          Active:
          <input
            type="checkbox"
            checked={updateIsActive}
            onChange={(e) => setUpdateIsActive(e.target.checked)}
            style={{ marginLeft: 10 }}
          />
        </label>
      </div>

      <div style={{ marginTop: 20 }}>
        <button onClick={handleUpdate} style={{ marginRight: 10 }}>
          Test Update
        </button>
        <button onClick={handleDelete}>Test Delete</button>
      </div>

      {message && (
        <p style={{ marginTop: 20, fontWeight: "bold" }}>{message}</p>
      )}
    </div>
  );
}
