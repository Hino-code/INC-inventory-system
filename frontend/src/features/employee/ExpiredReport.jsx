import React, { useEffect, useState } from "react";
import ReportButton from "../../components/ReportButton";

export default function ExpiredReport() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch('/api/reports/expired')
      .then(res => res.json())
      .then(setItems)
      .catch(console.error);
  }, []);

  return (
    <div>
      <h4>Expired Items Report</h4>
      <ReportButton type="expired" data={items} />
    </div>
  );
}
