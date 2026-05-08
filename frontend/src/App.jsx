import { useState } from "react";
import Agreement from "./components/Agreement";
import LanguageSelect from "./components/LanguageSelect";
import Chat from "./components/Chat";
import "./App.css";

export default function App() {
  const [screen, setScreen] = useState("agreement");
  const [language, setLanguage] = useState("english");

  return (
    <div className="app-container">
      {screen === "agreement" && (
        <Agreement onAgree={() => setScreen("language")} />
      )}
      {screen === "language" && (
        <LanguageSelect
          onSelect={(lang) => {
            setLanguage(lang);
            setScreen("chat");
          }}
        />
      )}
      {screen === "chat" && <Chat language={language} />}
    </div>
  );
}