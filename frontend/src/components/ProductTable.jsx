// src/components/ProductTable.jsx
import React from 'react';

export default function ProductTable({ data }) {
  const now = new Date();

  const getStatusBadges = item => {
    const badges = [];
    const badgeBase = "badge text-center px-2 py-1 me-1";
    const badgeStyle = { minWidth: '75px', display: 'inline-block' };

    // Expired?
    if (item.expiration_date) {
      const expDate = new Date(item.expiration_date);
      if (expDate <= now) {
        badges.push(
          <span
            key="expired"
            className={`${badgeBase} bg-danger`}
            style={badgeStyle}
          >
            Expired
          </span>
        );
      }
    }

    // Low stock?
    if (
      typeof item.quantity === 'number' &&
      typeof item.refill_threshold === 'number' &&
      item.quantity <= item.refill_threshold
    ) {
      badges.push(
        <span
          key="lowstock"
          className={`${badgeBase} bg-warning text-dark`}
          style={badgeStyle}
        >
          Low Stock
        </span>
      );
    }

    // If neither condition, show OK
    if (badges.length === 0) {
      badges.push(
        <span
          key="ok"
          className={`${badgeBase} bg-success`}
          style={badgeStyle}
        >
          OK
        </span>
      );
    }

    return badges;
  };

  if (!Array.isArray(data)) return null;

  return (
    <table className="table align-middle">
      <thead>
        <tr>
          <th>Name</th>
          <th>Price</th>
          <th>Quantity</th>
          <th>Category</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {data.map(item => {
          const key = item._id || item.id || JSON.stringify(item);
          return (
            <tr key={key}>
              <td>{item.name}</td>
              <td>{item.price}</td>
              <td>{item.quantity}</td>
              <td>{item.category}</td>
              <td>{getStatusBadges(item)}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
