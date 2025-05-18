import React, { useState } from 'react';
import { MessageCircle, X } from 'lucide-react';

const ChatButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  
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
            <div className="bg-gray-100 p-3 rounded-lg rounded-tl-none max-w-[80%] mb-3">
              <p className="text-sm">Hello! How can I help you today?</p>
              <span className="text-xs text-gray-500 mt-1 block">Support • 10:24 AM</span>
            </div>
          </div>
          <div className="border-t p-3">
            <div className="flex items-center">
              <input 
                type="text" 
                placeholder="Type a message..." 
                className="flex-1 border rounded-l-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button className="bg-blue-700 text-white px-4 py-2 rounded-r-lg hover:bg-blue-800 transition-colors">
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