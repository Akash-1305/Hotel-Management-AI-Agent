import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { MessageCircle, X } from "lucide-react";

const API_BASE = "http://127.0.0.1:8000";

const ChatButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      text: "Hello! How can I help you today?",
      sender: "AI Assist",
      time: new Date().toLocaleTimeString(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollTop = messagesEndRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      text: input,
      sender: "user",
      time: new Date().toLocaleTimeString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.get(`${API_BASE}/chat-ai`, {
        params: { user_query: input },
      });

      const botText =
        typeof response.data === "string"
          ? response.data
          : response.data.response || "I'm not sure how to respond to that.";

      const botMessage = {
        text: botText,
        sender: "AI Assist",
        time: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = {
        text: "Sorry, something went wrong. Please try again.",
        sender: "support",
        time: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {isOpen && (
        <div
          className="bg-white rounded-lg shadow-xl flex flex-col overflow-hidden fixed mb-4"
          style={{
            width: "40vw",
            height: "75vh",
            bottom: "80px",
            right: "24px",
          }}
        >
          <div className="bg-blue-700 text-white p-4 flex justify-between items-center">
            <h3 className="font-medium">AI Assist</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          <div ref={messagesEndRef} className="flex-1 p-4 overflow-y-auto">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg max-w-[80%] mb-3 ${
                  msg.sender === "user"
                    ? "bg-blue-200 rounded-tr-none ml-auto"
                    : "bg-gray-100 rounded-tl-none"
                }`}
              >
                <p className="text-sm">{msg.text}</p>
                <span className="text-xs text-gray-500 mt-1 block">
                  {msg.time}
                </span>
              </div>
            ))}

            {loading && (
              <div className="p-3 rounded-lg bg-gray-100 max-w-[80%] mb-3 animate-pulse">
                <p className="text-sm">Typing...</p>
              </div>
            )}
          </div>

          <div className="border-t p-3">
            <div className="flex items-center">
              <input
                type="text"
                placeholder="Type a message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") sendMessage();
                }}
                className="flex-1 border rounded-l-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={sendMessage}
                className="bg-blue-700 text-white px-4 py-2 rounded-r-lg hover:bg-blue-800 transition-colors"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}

      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 bg-blue-700 text-white rounded-full p-4 shadow-lg hover:bg-blue-800 transition-colors flex items-center justify-center z-40"
        aria-label="Toggle chat"
      >
        <MessageCircle className="h-6 w-6" />
      </button>
    </>
  );
};

export default ChatButton;
