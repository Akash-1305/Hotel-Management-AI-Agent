import React from "react";
import { NavLink } from "react-router-dom";
import { Search, BellDot, User, Building } from "lucide-react";

const Navbar = () => {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div className="mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <NavLink
              to="/"
              className="flex items-center text-blue-700 font-bold text-xl"
            >
              <Building className="h-6 w-6 mr-2" />
              <span>RoomMaster</span>
            </NavLink>
          </div>
          <div className="flex items-center space-x-8">
            <nav className="hidden md:flex space-x-8">
              <NavLink
                to="/"
                className={({ isActive }) =>
                  `border-b-2 ${
                    isActive
                      ? "border-blue-600 text-blue-600"
                      : "border-transparent text-gray-600 hover:text-blue-600"
                  } px-1 py-5 text-sm font-medium transition-colors`
                }
              >
                Dashboard
              </NavLink>
              <NavLink
                to="/reservations"
                className={({ isActive }) =>
                  `border-b-2 ${
                    isActive
                      ? "border-blue-600 text-blue-600"
                      : "border-transparent text-gray-600 hover:text-blue-600"
                  } px-1 py-5 text-sm font-medium transition-colors`
                }
              >
                Reservations
              </NavLink>
              <NavLink
                to="/rooms"
                className={({ isActive }) =>
                  `border-b-2 ${
                    isActive
                      ? "border-blue-600 text-blue-600"
                      : "border-transparent text-gray-600 hover:text-blue-600"
                  } px-1 py-5 text-sm font-medium transition-colors`
                }
              >
                Rooms
              </NavLink>
              <NavLink
                to="/reports"
                className={({ isActive }) =>
                  `border-b-2 ${
                    isActive
                      ? "border-blue-600 text-blue-600"
                      : "border-transparent text-gray-600 hover:text-blue-600"
                  } px-1 py-5 text-sm font-medium transition-colors`
                }
              >
                Reports
              </NavLink>
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
