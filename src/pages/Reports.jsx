import React from 'react';
import { BarChart, FileDown, Filter, Calendar } from 'lucide-react';

const Reports = () => {
  return (
    <div>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Reports</h1>
        <div className="flex space-x-3 mt-4 md:mt-0">
          <button className="flex items-center px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
            <Calendar className="h-4 w-4 mr-2" />
            <span>Date Range</span>
          </button>
          <button className="flex items-center px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
            <Filter className="h-4 w-4 mr-2" />
            <span>Filter</span>
          </button>
          <button className="flex items-center px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition-colors">
            <FileDown className="h-4 w-4 mr-2" />
            <span>Export</span>
          </button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Revenue</h2>
            <BarChart className="text-gray-400 h-5 w-5" />
          </div>
          <div className="h-64 flex items-center justify-center border rounded-lg">
            <p className="text-gray-500">Revenue chart visualization would appear here</p>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-sm text-gray-500">Total Revenue</p>
              <p className="text-lg font-semibold text-gray-900">$12,450</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Average Daily</p>
              <p className="text-lg font-semibold text-gray-900">$415</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Projected</p>
              <p className="text-lg font-semibold text-gray-900">$15,200</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Occupancy Rate</h2>
            <BarChart className="text-gray-400 h-5 w-5" />
          </div>
          <div className="h-64 flex items-center justify-center border rounded-lg">
            <p className="text-gray-500">Occupancy rate visualization would appear here</p>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-sm text-gray-500">Average Rate</p>
              <p className="text-lg font-semibold text-gray-900">68%</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Peak Day</p>
              <p className="text-lg font-semibold text-gray-900">Saturday</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Lowest Day</p>
              <p className="text-lg font-semibold text-gray-900">Monday</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm p-4">
        <h2 className="text-lg font-semibold mb-4">Common Reports</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { title: 'Daily Revenue', icon: <BarChart className="h-5 w-5" /> },
            { title: 'Monthly Occupancy', icon: <BarChart className="h-5 w-5" /> },
            { title: 'Guest Statistics', icon: <BarChart className="h-5 w-5" /> },
            { title: 'Room Performance', icon: <BarChart className="h-5 w-5" /> },
            { title: 'Booking Sources', icon: <BarChart className="h-5 w-5" /> },
            { title: 'Seasonal Trends', icon: <BarChart className="h-5 w-5" /> }
          ].map((report, index) => (
            <div 
              key={index}
              className="border rounded-lg p-4 hover:shadow-md transition-shadow flex items-center justify-between"
            >
              <div>
                <h3 className="font-medium">{report.title}</h3>
                <p className="text-sm text-gray-500 mt-1">Last generated: Today</p>
              </div>
              <div className="text-gray-400">
                {report.icon}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Reports;