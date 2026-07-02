import { useState } from "react";
import api from "../api/api";

export default function ChatSection() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function sendQuestion(e) {
    e.preventDefault();

    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const res = await api.post("/chat", {
        question,
      });

      setMessages((prev) => [
        ...prev,
        userMessage,
        {
          role: "assistant",
          text: res.data.answer,
        },
      ]);

    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Unable to answer your question.",
        },
      ]);
    }

    setQuestion("");
    setLoading(false);
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">

      <h2 className="text-2xl font-bold mb-5">
        Chat with Data
      </h2>

      <div className="border rounded-lg p-4 h-96 overflow-y-auto bg-gray-50">

        {messages.length === 0 && (
          <p className="text-gray-500">
            Ask a question about your dataset.
          </p>
        )}

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`mb-4 ${
              msg.role === "user"
                ? "text-right"
                : "text-left"
            }`}
          >

            <span
              className={`inline-block px-4 py-2 rounded-lg max-w-[80%] ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-white border"
              }`}
            >
              {msg.text}
            </span>

          </div>

        ))}

      </div>

      <form
        onSubmit={sendQuestion}
        className="flex mt-5 gap-3"
      >

        <input
          type="text"
          placeholder="Ask anything..."
          className="flex-1 border rounded-lg p-3"
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
        />

        <button
          className="bg-blue-600 text-white px-6 rounded-lg"
          disabled={loading}
        >
          {loading ? "..." : "Send"}
        </button>

      </form>

    </div>
  );
}