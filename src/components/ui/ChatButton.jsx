import React, { useState } from "react";
import axios from "axios";
import { MessageCircle, X } from "lucide-react";

const ChatButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      text: "Hello! How can I help you today?",
      sender: "support",
      time: new Date().toLocaleTimeString(),
    },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      text: input,
      sender: "user",
      time: new Date().toLocaleTimeString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const response = await axios.get("/chat-ai", {
        params: { user_query: input },
      });
      const botMessage = {
        text: response.data.response,
        sender: "support",
        time: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-20">
      {isOpen && (
        <div className="bg-white rounded-lg shadow-xl mb-4 w-80 h-96 flex flex-col overflow-hidden">
          <div className="bg-blue-700 text-white p-4 flex justify-between items-center">
            <h3 className="font-medium">Chat Support</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          <div className="flex-1 p-4 overflow-y-auto">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg ${
                  msg.sender === "support"
                    ? "bg-gray-100 rounded-tl-none"
                    : "bg-blue-200 rounded-tr-none"
                } max-w-[80%] mb-3`}
              >
                <p className="text-sm">{msg.text}</p>
                <span className="text-xs text-gray-500 mt-1 block">
                  {msg.sender} • {msg.time}
                </span>
              </div>
            ))}
          </div>
          <div className="border-t p-3">
            <div className="flex items-center">
              <input
                type="text"
                placeholder="Type a message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
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
        className="bg-blue-700 text-white rounded-full p-4 shadow-lg hover:bg-blue-800 transition-colors flex items-center justify-center"
      >
        <MessageCircle className="h-6 w-6" />
        <span className="sr-only">Chat</span>
      </button>
    </div>
  );
};

export default ChatButton;
