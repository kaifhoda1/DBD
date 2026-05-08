export default function LanguageSelect({ onSelect }) {
  return (
    <div className="screen">
      <h1 className="logo">DBD</h1>
      <p className="tagline">Choose your language</p>
      <div className="lang-buttons">
        <button className="btn-lang" onClick={() => onSelect("english")}>
          English
        </button>
        <button className="btn-lang" onClick={() => onSelect("hindi")}>
          हिंदी
        </button>
        <button className="btn-lang" onClick={() => onSelect("hinglish")}>
          Hinglish
        </button>
      </div>
    </div>
  );
}