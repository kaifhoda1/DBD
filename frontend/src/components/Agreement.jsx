const AGREEMENT = [
  "This is an AI chatbot. It is NOT a licensed psychologist or medical professional.",
  "It cannot diagnose any condition or prescribe medication.",
  "It is NOT a substitute for professional mental health care.",
  "In a mental health emergency, call a crisis helpline immediately.",
  "The chatbot may make errors. Do not rely on it for medical decisions.",
  "Conversations may be processed by AI APIs. Do not share personal ID details.",
  "This tool is for emotional support and listening only.",
  "Creators of this app are not liable for decisions made based on conversations.",
  "If you are under 18, use this with awareness of a trusted adult.",
  "By continuing you confirm you understand and accept these terms.",
];

export default function Agreement({ onAgree }) {
  return (
    <div className="screen">
      <h1 className="logo">DBD</h1>
      <p className="tagline">Don't Be Depressed — You are not alone</p>
      <div className="agreement-box">
        <h2>Before You Begin</h2>
        <ol>
          {AGREEMENT.map((point, i) => (
            <li key={i}>{point}</li>
          ))}
        </ol>
      </div>
      <button className="btn-primary" onClick={onAgree}>
        I Understand — Let's Talk
      </button>
    </div>
  );
}