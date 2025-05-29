function AlertModal({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="modal show fade" tabIndex="-1" style={{ display: "block", backgroundColor: "rgba(0,0,0,0.3)" }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content shadow">
          <div className="modal-header">
            <h5 className="modal-title">Validation Error</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <div className="modal-body">
            <p className="text-danger">{message}</p>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-danger" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
