import React, { useEffect, useState } from "react";
import ReportButton from "../../components/ReportButton";

export default function DamagedReport() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch('/api/reports/damaged')
      .then(res => res.json())
      .then(setItems)
      .catch(console.error);
  }, []);

  return (
    <div>
      <h4>Damaged Items Report</h4>
      <ReportButton type="damaged" data={items} />
    </div>
  );
}
