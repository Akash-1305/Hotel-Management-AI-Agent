import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import ChatButton from '../ui/ChatButton';

const Layout = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="container mx-auto px-4 py-6">
        <Outlet />
      </div>
      <ChatButton />
    </div>
  );
};

export default Layout;