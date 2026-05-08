import { useState, useRef, useEffect } from "react";
import axios from "axios";
import CrisisAlert from "./CrisisAlert";

const GREETINGS = {
  english: "Hi, I'm here to listen. No judgment, no pressure. How are you feeling today?",
  hindi: "Namaste, main yahan hoon sunne ke liye. Koi judgment nahi. Aaj kaisa feel kar rahe hain?",
  hinglish: "Hey, main yahan hoon tumhari baat sunne ke liye. No judgment. Aaj kaisa feel ho raha hai?",
};

export default function Chat({ language }) {
  const [messages, setMessages] = useState([
    { role: "assistant", content: GREETINGS[language] },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [crisis, setCrisis] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage() {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    const newMessages = [...messages, { role: "user", content: userMsg }];
    setMessages(newMessages);
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message: userMsg,
        history: newMessages.slice(0, -1),
        language: language,
      });
      if (res.data.crisis) setCrisis(true);
      setMessages([...newMessages, { role: "assistant", content: res.data.reply }]);
    } catch {
      setMessages([...newMessages, {
        role: "assistant",
        content: "Something went wrong. Please try again.",
      }]);
    }
    setLoading(false);
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="chat-screen">
      {crisis && <CrisisAlert onClose={() => setCrisis(false)} />}
      <div className="chat-header">
        <span className="logo-small">DBD</span>
        <span className="ai-notice">AI Support — Not a therapist</span>
      </div>
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {loading && <div className="message assistant typing">...</div>}
        <div ref={bottomRef} />
      </div>
      <div className="chat-input-area">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Type how you feel..."
          rows={2}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}