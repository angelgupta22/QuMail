import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8002/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Backend not reachable" });
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h2>QuMail – Quantum-Inspired Secure Messaging</h2>

      <textarea
        rows="4"
        cols="60"
        placeholder="Enter message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <br /><br />

      <button onClick={sendMessage} disabled={loading}>
        {loading ? "Encrypting..." : "Encrypt & Send"}
      </button>

      {result && (
        <pre style={{ marginTop: "20px", background: "#f4f4f4", padding: "15px" }}>
{JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;
