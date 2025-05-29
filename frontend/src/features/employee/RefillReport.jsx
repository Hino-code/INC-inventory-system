import React, { useEffect, useState } from "react";
import ReportButton from "../../components/ReportButton";

export default function RefillReport() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch('/api/reports/refill')
      .then(res => res.json())
      .then(setAlerts)
      .catch(console.error);
  }, []);

  return (
    <div>
      <h4>Refill Alerts Report</h4>
      <ReportButton type="refill" data={alerts} />
    </div>
  );
}
