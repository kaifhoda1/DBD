import HELPLINES from "../data/helplines";

export default function CrisisAlert({ onClose }) {
  return (
    <div className="crisis-overlay">
      <div className="crisis-box">
        <h2>⚠️ We Are Worried About You</h2>
        <p>
          It sounds like you may be going through something very difficult.
          Please reach out to a real person right now. You matter.
        </p>
        {Object.values(HELPLINES).map((region) => (
          <div key={region.label} className="region">
            <h3>{region.label}</h3>
            {region.lines.map((line) => (
              <div key={line.number} className="helpline">
                <strong>{line.name}</strong>
                <span> — {line.number}</span>
                <small> ({line.note})</small>
              </div>
            ))}
          </div>
        ))}
        <button className="btn-primary" onClick={onClose}>
          I am safe — Continue
        </button>
      </div>
    </div>
  );
}